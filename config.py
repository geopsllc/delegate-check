# SNS config (send SMS)
sns_enabled = 'no' # yes/no
aws_key_id = 'keyId'
aws_secret_key = 'secretKey'
aws_region = 'us-east-1' # not all regions support SNS
phone = '+xxxxxxxxxxx'

# Delegate Names
# Leave only the networks and delegates that you use!
delegates = {
    'Ark':['name'],
    'DArk':['name'],
    'Qredit':['name'],
    'Phantom':['name'],
    'Persona':['name'],
    'Ripa':['name1','name2'],
    'Swapblocks':['name1','name2','name3'],
    'Blockpool':['name1','name2','name3','name4']
}

# Don't change the rest unless you know what you're doing!

# Network APIs
nodes = {
    'Ark':'https://explorer.ark.io/api/v2',
    'DArk':'https://dexplorer.ark.io/api/v2',
    'Qredit':'https://qredit.cloud/api/v2',
    'Phantom':'https://explorer.phantom.org:8443/api/v2',
    'Persona':'https://persona-api.geops.net/api',
    'Ripa':'http://209.97.137.11:5500/api',
    'Swapblocks':'https://api.swapblocks.io/api',
    'Blockpool':'http://s01.mc.blockpool.io:9030/api'
}


# Network Settings [delegates, blocktime, core version]
db = {
    'Ark':[51, 8, 'v2'],
    'DArk':[51, 8, 'v2'],
    'Qredit':[51, 8, 'v2'],
    'Phantom':[51, 8, 'v2'],
    'Persona':[51, 8, 'v1'],
    'Ripa':[101, 8, 'v1'],
    'Swapblocks':[51, 8, 'v1'],
    'Blockpool':[201, 15, 'v1']
}

# Network EPOCHs [YYYY, MM, DD, HH, MM, SS] (v1 only)
epoch = {
    'Persona':[2018, 2, 1, 0, 0, 0],
    'Ripa':[2017, 3, 21, 13, 0, 0],
    'Swapblocks':[2017, 3, 21, 13, 0, 0],
    'Blockpool':[2017, 3, 21, 13, 0, 0]
}
