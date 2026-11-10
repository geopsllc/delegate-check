#!/usr/bin/env python3

# Imports
from config import *
import os
import sys
import json
import time
import asyncio
import aiohttp

# Settings
ERROR_ALERT_AFTER = 3 # consecutive failed runs before an API error alert is sent
API_ATTEMPTS = 3 # tries per API request before giving up
API_TIMEOUT = 10 # seconds per attempt
API_RETRY_DELAY = 2 # seconds to wait before the 2nd attempt, doubled before the 3rd (waits grow with each retry)
heartbeat_url = globals().get('heartbeat_url', '') # optional, set in config.py

# Functions
async def notifications(msg):

    # Returns True when Discord accepted the message so callers only mark a
    # delegate as notified after a successful delivery (failed ones retry next run)
    payload = dict(ntfy)
    payload['content'] = (msg + ' ' + discord_id).strip()

    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(discord_webhook, json=payload) as resp:
                if resp.status in (200, 204):
                    return True
                print('Discord webhook failed: HTTP ' + str(resp.status), file=sys.stderr)

    except Exception as e:
        print('Discord webhook failed: ' + type(e).__name__, file=sys.stderr)

    return False

async def heartbeat():

    # Optional dead man's switch (healthchecks.io style): pinged after every completed run
    if heartbeat_url == '':
        return

    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(heartbeat_url) as resp:
                if resp.status >= 400:
                    print('Heartbeat failed: HTTP ' + str(resp.status), file=sys.stderr)

    except Exception as e:
        print('Heartbeat failed: ' + type(e).__name__, file=sys.stderr)

async def api_get(url):

    # Retries transient failures (timeouts, connection errors, 5xx, 429, bad JSON) with a growing delay.
    # Returns the parsed JSON, or a short reason string once every attempt has failed.
    reason = 'error'

    for attempt in range(API_ATTEMPTS):
        if attempt:
            await asyncio.sleep(API_RETRY_DELAY * attempt)

        try:
            timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    reason = 'HTTP ' + str(resp.status)
                    if resp.status < 500 and resp.status != 429:
                        return reason # other client errors (e.g. 404) won't fix themselves

        except asyncio.TimeoutError:
            reason = 'timeout'

        except Exception:
            reason = 'error'

    return reason

def write_json(path,data):

    # Write to a temp file and swap it in, so readers never see a partial file
    tmp = path + '.tmp'
    with open(tmp, 'w') as file:
        json.dump(data, file)
    os.replace(tmp, path)

def get_round(height,network):

    data = divmod(height,db[network][0])

    if data[1] == 0:
        result = data[0]
    else:
        result = data[0] + 1

    return result

def ago(timestamp):

    mins = max(0, round((time.time() - timestamp)/60))

    if mins >= 1440:
        value, unit = mins // 1440, 'day'
    elif mins >= 60:
        value, unit = mins // 60, 'hour'
    else:
        value, unit = mins, 'minute'

    return str(value) + ' ' + unit + ('' if value == 1 else 's') + ' ago'

def new_record(network,delegate):

    # Raw values only - the dashboard formats them (ages are computed live in the browser)
    return {'network': network, 'delegate': delegate, 'rank': None, 'forging': None, 'last_block': None, 'state': 'error', 'yield': None}

def log_failure(network,delegate,reason):

    print('Network: ' + network + ' | Delegate: ' + delegate + ' | State: error | ' + reason, file=sys.stderr)

def calc_yield(del_blocks,total_rounds,net_round,network):

    # Percentage of the last total_rounds rounds in which the delegate forged a block
    missed = 0
    forged = 0
    cur_round = get_round(del_blocks['data'][0]['height'],network)

    if net_round > cur_round + 1:
        missed += net_round - cur_round - 1
    else:
        forged += 1

    if missed >= total_rounds:
        missed = total_rounds
    else:
        for i in range(0, total_rounds - 1):
            cur_round = get_round(del_blocks['data'][i]['height'],network)
            prev_round = get_round(del_blocks['data'][i + 1]['height'],network)
            if prev_round < cur_round - 1:
                if cur_round - prev_round - 1 >= total_rounds - missed - forged:
                    missed = total_rounds - forged
                    break
                else:
                    missed += cur_round - prev_round - 1
            else:
                forged += 1
                if forged >= total_rounds - missed:
                    forged = total_rounds - missed
                    break

    if forged + missed == 0:
        return 0

    return round((forged * 100)/(forged + missed))

async def del_check(network,delegate,net_status):

    record = new_record(network,delegate)

    if isinstance(net_status, str):
        log_failure(network,delegate,'node status request failed (' + net_status + ')')
        return record

    del_info, del_blocks = await asyncio.gather(
        api_get(nodes[network] + '/delegates/' + delegate),
        api_get(nodes[network] + '/delegates/' + delegate + '/blocks'))

    if isinstance(del_info, str):
        log_failure(network,delegate,'delegate info request failed (' + del_info + ')')
        return record

    if isinstance(del_blocks, str):
        log_failure(network,delegate,'blocks request failed (' + del_blocks + ')')
        return record

    total_rounds = del_blocks['meta']['count']

    if total_rounds < 2:
        print('Network: ' + network + ' | Delegate: ' + delegate + ' | State: unknown | not enough blocks forged yet to calculate yield', file=sys.stderr)
        record['state'] = 'unknown'
        return record

    rank = del_info['data']['rank']
    forging = rank <= db[network][0]
    last_block = del_blocks['data'][0]['timestamp']['unix']
    net_round = get_round(net_status['data']['now'],network)
    cur_round = get_round(del_blocks['data'][0]['height'],network)

    if not forging:
        state = 'out'
    elif net_round <= cur_round + 1:
        state = 'healthy'
    else:
        state = 'missing'

    record['rank'] = rank
    record['forging'] = forging
    record['last_block'] = last_block
    record['state'] = state
    record['yield'] = calc_yield(del_blocks,total_rounds,net_round,network)

    print('Network: ' + network + ' | Delegate: ' + delegate + ' | Rank: ' + str(rank) + ' | Forging: ' + ('yes' if forging else 'no') + ' | Last Block: ' + ago(last_block) + ' | State: ' + state + ' | Yield: ' + str(record['yield']) + '%')

    return record

async def safe_check(network,delegate,net_status):

    # One malformed response must not take down the checks for every other delegate
    try:
        return await del_check(network,delegate,net_status)
    except Exception as e:
        log_failure(network,delegate,'unexpected ' + type(e).__name__ + ': ' + str(e))
        return new_record(network,delegate)

async def update_alerts(network,delegate,state):

    # savedState: 'clean' = no open alert, 'dirty' = alert sent and not yet recovered
    key = network + '|' + delegate
    failures[key] = failures.get(key, 0) + 1 if state == 'error' else 0
    current = savedState[network][delegate]
    prefix = network + ' delegate ' + delegate + ' '

    if state == 'healthy':
        if current == 'dirty' and (discord_enabled != 'yes' or await notifications(prefix + 'recovered!')):
            savedState[network][delegate] = 'clean'
        return

    if state == 'out':
        msg = 'not forging!'
    elif state == 'missing':
        msg = 'missed a block!'
    elif state == 'error' and failures[key] >= ERROR_ALERT_AFTER:
        msg = 'API check failing!'
    else:
        return

    if discord_enabled == 'yes' and current == 'clean' and await notifications(prefix + msg):
        savedState[network][delegate] = 'dirty'

async def main():

    # The node status is per network, so fetch it once instead of once per delegate
    networks = list(delegates)
    statuses = await asyncio.gather(*(api_get(nodes[network] + '/node/status') for network in networks))
    net_status = dict(zip(networks, statuses))

    results = await asyncio.gather(*(safe_check(network,delegate,net_status[network]) for network in networks for delegate in delegates[network]))
    results = sorted(results, key=lambda r: (r['network'], r['delegate']))

    for record in results:
        await update_alerts(record['network'],record['delegate'],record['state'])

    write_json('web/status.json', {'updated_at': int(time.time()), 'delegates': results})
    write_json('state.json', savedState)

    await heartbeat()

# Load JSON state file
savedState = {}

if os.path.exists('state.json'):
    try:
        with open('state.json', 'r') as file:
            savedState = json.load(file)
    except (OSError, ValueError) as e:
        print('Could not read state.json, starting fresh: ' + type(e).__name__, file=sys.stderr)

# Fill in the state
failures = savedState.setdefault('_failures', {})

for network in delegates:
    if network not in savedState:
        savedState[network] = {}
    for delegate in delegates[network]:
        if delegate not in savedState[network]:
            savedState[network][delegate] = 'clean'

# Async Loop
asyncio.run(main())
