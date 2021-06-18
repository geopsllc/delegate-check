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
    'Qredit':['name1','name2']
}

# Don't change the rest unless you know what you're doing!

# Network APIs
nodes = {
    'Ark':'https://api.ark.io/api',
    'DArk':'https://dapi.ark.io/api',
    'Qredit':'https://qredit.cloud/api'
}

# Network Settings [delegates, blocktime]
db = {
    'Ark':[51, 8],
    'DArk':[51, 8],
    'Qredit':[51, 8]
}
