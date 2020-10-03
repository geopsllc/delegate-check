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
    'Blockpool':['name1','name2'],
    'Phantom':['name1','name2'],
    'Ripa':['name1','name2'],
    'Kapu':['name1','name2'],
    'Hydra':['name1','name2'],
    'Compendia-M':['name1','name2'],
    'Compendia-D':['name1','name2']
}

# Don't change the rest unless you know what you're doing!

# Network APIs
nodes = {
    'Ark':'https://explorer.ark.io/api',
    'DArk':'https://dexplorer.ark.io/api',
    'Qredit':'https://qredit.cloud/api',
    'Blockpool':'http://api.mainnet.blockpool.io:9031/api',
    'Phantom':'https://explorer.phantom.org:8443/api/v2',
    'Ripa':'https://api.ripaex.io/api/v2',
    'Kapu':'https://api.kapunode.net/api/v2',
    'Hydra':'http://35.195.150.223:4703/api/v2',
    'Compendia-M':'https://api.compendia.org/api',
    'Compendia-D':'https://api.nos.dev/api'
}

# Network Settings [delegates, blocktime]
db = {
    'Ark':[51, 8],
    'DArk':[51, 8],
    'Qredit':[51, 8],
    'Blockpool':[201, 15],
    'Phantom':[51, 8],
    'Ripa':[101, 8],
    'Kapu':[51, 8]
    'Hydra':[53, 8],
    'Compendia-M':[47, 6],
    'Compendia-D':[47, 6],
}
