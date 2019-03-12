#!/usr/bin/env python3

# Imports
from config import *
import asyncio
import aiohttp
import aioboto3
from datetime import datetime
from datetime import timedelta
from shutil import copy2

# Functions
async def notifications(msg):
    async with aioboto3.client("sns",
        aws_access_key_id=aws_key_id,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region) as client:
        await client.publish(
            PhoneNumber=phone,
            Message=msg)

async def api_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def v2(network,delegate):
    result = await api_get(nodes[network] + '/delegates/' + delegate)
    rank = str(result['data']['rank'])
    if result['data']['rank'] <= db[network][0]:
        active = 'yes'
        activehtml = "<span class=\"badge badge-pill badge-success\">yes</span>"
    else:
        active = 'no'
        activehtml = "<span class=\"badge badge-pill badge-danger\">no</span>"
    rank = rank + '/' + str(db[network][0])
    timestamp = result['data']['blocks']['last']['timestamp']['unix']
    utc_remote = datetime.utcfromtimestamp(timestamp)
    utc_local = datetime.utcnow().replace(microsecond=0)
    delta = int((utc_local - utc_remote).total_seconds())
    lb = str(int(round(delta/60)))
    tworounds = 2 * db[network][0] * db[network][1]
    if delta > tworounds:
        miss = 'yes'
        misshtml = "<span class=\"badge badge-pill badge-danger\">yes</span>"
        if sns_enabled == 'yes' and delta < 2 * tworounds:
            await notifications(network + ' delegate missed a block!')
            print('Sent SMS!')
    else:
        miss = 'no'
        misshtml = "<span class=\"badge badge-pill badge-success\">no</span>"
    print('Network: ' + network + ' | Delegate: ' + delegate + ' | Rank: ' + rank + ' | Active: ' + active + ' | Last Block: ' + lb + ' min ago | Missed Block: ' + miss)
    csv.write(network + ',' + delegate + ',' + rank + ',' + activehtml + ',' + lb + ' min ago,' + misshtml + '\n')

async def v1(network,delegate):
    result = await api_get(nodes[network] + '/delegates/get?username=' + delegate)
    rank = str(result['delegate']['rate'])
    if result['delegate']['rate'] <= db[network][0]:
        active = 'yes'
        activehtml = "<span class=\"badge badge-pill badge-success\">yes</span>"
    else:
        active = 'no'
        activehtml = "<span class=\"badge badge-pill badge-danger\">no</span>"
    rank = rank + '/' + str(db[network][0])
    pubkey = str(result['delegate']['publicKey'])
    result = await api_get(nodes[network] + '/blocks?generatorPublicKey=' + pubkey + '&limit=1')
    timestamp = result['blocks'][0]['timestamp']
    utc_remote = datetime(epoch[network][0], epoch[network][1], epoch[network][2], epoch[network][3], epoch[network][4], epoch[network][5]) + timedelta(seconds=timestamp)
    utc_local = datetime.utcnow().replace(microsecond=0)
    delta = int((utc_local - utc_remote).total_seconds())
    lb = str(int(round(delta/60)))
    tworounds = 2 * db[network][0] * db[network][1]
    if delta > tworounds:
        miss = 'yes'
        misshtml = "<span class=\"badge badge-pill badge-danger\">yes</span>"
        if sns_enabled == 'yes' and delta < 2 * tworounds:
            await notifications(network + ' delegate missed a block!')
            print('Sent SMS!')
    else:
        miss = 'no'
        misshtml = "<span class=\"badge badge-pill badge-success\">no</span>"
    print('Network: ' + network + ' | Delegate: ' + delegate + ' | Rank: ' + rank + ' | Active: ' + active + ' | Last Block: ' + lb + ' min ago | Missed Block: ' + miss)
    csv.write(network + ',' + delegate + ',' + rank + ',' + activehtml + ',' + lb + ' min ago,' + misshtml + '\n')

# Build Tasks List
tasks = []
function_map = {
    'v1':v1,
    'v2':v2
}
for network in delegates:
    for delegate in delegates[network]:
        tasks.append(asyncio.ensure_future(function_map[db[network][2]](network,delegate)))

# Initiate CSV
csv = open('state.csv','w+')
csv.write("Network,Delegate,Rank,Active,Last Block,Missed Block\n")

# Async Loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(asyncio.wait(tasks))
finally:
    loop.close()

# Close and Copy CSV to web/
csv.close()
copy2('state.csv','web/')
