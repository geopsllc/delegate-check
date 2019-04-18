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
    'Ripa':['name1','name2']
}

# Don't change the rest unless you know what you're doing!

# Network APIs
nodes = {
    'Ark':'https://explorer.ark.io/api/v2',
    'DArk':'https://dexplorer.ark.io/api/v2',
    'Qredit':'https://qredit.cloud/api/v2',
    'Phantom':'https://explorer.phantom.org:8443/api/v2',
    'Ripa':'https://api.ripaex.io/api/v2'
}

# Network Settings [delegates, blocktime]
db = {
    'Ark':[51, 8],
    'DArk':[51, 8],
    'Qredit':[51, 8],
    'Phantom':[51, 8],
    'Ripa':[101, 8]
}
