#!/usr/bin/env python3

# Imports
from config import *
import os
import sys
import json
import asyncio
import aiohttp
import aioboto3
import pandas
from datetime import datetime, timezone
from shutil import copy2

# Functions
async def notifications(msg):

    session = aioboto3.Session(
        aws_access_key_id=aws_key_id,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region)

    async with session.client('sns') as client:
        await client.publish(PhoneNumber=phone,Message=msg)

async def api_get(url):

    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                return await resp.json()

    except asyncio.TimeoutError:
        return 'timeout'

    except Exception:
        return 'error'

def get_round(height,network):

    data = divmod(height,db[network][0])

    if data[1] == 0:
        result = data[0]
    else:
        result = data[0] + 1

    return result

def report(network,delegate,state,reason):

    # Keep the delegate visible in the CSV/dashboard and log why the check failed
    print('Network: ' + network + ' | Delegate: ' + delegate + ' | State: ' + state + ' | ' + reason, file=sys.stderr)
    csv.write(network + ',' + delegate + ',-,-,-,' + state + ',-\n')

async def del_check(network,delegate):

    del_info = await api_get(nodes[network] + '/delegates/' + delegate)
    if isinstance(del_info, str):
        report(network,delegate,'error','delegate info request failed (' + del_info + ')')
        return

    del_blocks = await api_get(nodes[network] + '/delegates/' + delegate + '/blocks')
    if isinstance(del_blocks, str):
        report(network,delegate,'error','blocks request failed (' + del_blocks + ')')
        return

    net_height = await api_get(nodes[network] + '/node/status')
    if isinstance(net_height, str):
        report(network,delegate,'error','node status request failed (' + net_height + ')')
        return

    total_rounds = del_blocks['meta']['count']

    if total_rounds < 2:
        report(network,delegate,'unknown','not enough blocks forged yet to calculate yield')
        return

    if del_info['data']['rank'] <= db[network][0]:
        forging = 'yes'
    else:
        forging = 'no'

    missed = 0
    forged = 0
    rank = str(del_info['data']['rank'])
    timestamp = del_blocks['data'][0]['timestamp']['unix']
    utc_remote = datetime.fromtimestamp(timestamp, timezone.utc)
    utc_local = datetime.now(timezone.utc).replace(microsecond=0)
    delta = str(round(int((utc_local - utc_remote).total_seconds())/60))
    net_round = get_round(net_height['data']['now'],network)
    cur_round = get_round(del_blocks['data'][0]['height'],network)

    if forging == 'no':
        state = 'out'
        if sns_enabled == 'yes' and savedState[network][delegate] == 'clean':
            await notifications(network + ' delegate ' + delegate + '  not forging!')
            savedState[network][delegate] = 'dirty'
    elif net_round <= cur_round + 1:
        state = 'healthy'
        savedState[network][delegate] = 'clean'
    else:
        state = 'missing'
        if sns_enabled == 'yes' and savedState[network][delegate] == 'clean':
            await notifications(network + ' delegate ' + delegate + '  missed a block!')
            savedState[network][delegate] = 'dirty'

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
        prod = '0'
    else:
        prod = str(round((forged * 100)/(forged + missed)))

    print('Network: ' + network + ' | Delegate: ' + delegate + ' | Rank: ' + rank + ' | Forging: ' + forging + ' | Last Block: ' + delta + ' min ago | State: ' + state + ' | Yield: ' + prod + '%')
    csv.write(network + ',' + delegate + ',' + rank + ',' + forging + ',' + delta + ' min ago,' + state + ',' + prod + '%\n')

async def safe_check(network,delegate):

    # One malformed response must not take down the checks for every other delegate
    try:
        await del_check(network,delegate)
    except Exception as e:
        report(network,delegate,'error','unexpected ' + type(e).__name__ + ': ' + str(e))

async def main():

    await asyncio.gather(*(safe_check(network,delegate) for network in delegates for delegate in delegates[network]))

# Initialize State
savedState = {}

# Initialize CSV
csv = open('state.csv','w+')
csv.write('Network,Delegate,Rank,Forging,Last Block,State,Yield\n')

# Load JSON state file
if os.path.exists('state.json'):
    with open('state.json', 'r') as file:
      savedState = json.load(file)

# Fill in the state
for network in delegates:
    if network not in savedState:
        savedState[network] = {}
    for delegate in delegates[network]:
        if delegate not in savedState[network]:
            savedState[network][delegate] = 'clean'

# Async Loop
try:
    asyncio.run(main())

finally:
    csv.close()

# Sort & Cleanup
csvData = pandas.read_csv("state.csv")

csvData.sort_values(["Network", "Delegate"],
                    axis=0,
                    inplace=True)

csvData.to_csv('state.csv', index=False)

copy2('state.csv','web/')

with open('state.json', 'w+') as file:
  json.dump(savedState, file)
