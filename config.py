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
    'Solar':['name'],
    'TSolar':['name1','name2']
}

# Don't change the rest unless you know what you're doing!

# Network APIs
nodes = {
    'Ark':'https://api.ark.io/api',
    'DArk':'https://dapi.ark.io/api',
    'Solar':'https://sxp.mainnet.sh/api',
    'TSolar':'https://sxp.testnet.sh/api'
}

# Network Settings [delegates, blocktime]
db = {
    'Ark':[51, 8],
    'DArk':[51, 8],
    'Solar':[53, 8],
    'TSolar':[53, 8]
}
