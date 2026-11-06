# Discord Webhook (notifications)
discord_enabled = 'no' # yes/no
discord_webhook = 'https://discord.com/api/webhooks/webhookId/webhookToken'
discord_id = '' # optional Discord user id to @mention, leave empty for no mention

# Webhook JSON
if discord_enabled == 'yes':
    ntfy = {'avatar_url':'https://www.shareicon.net/download/128x128//2015/09/17/102426_freebsd_512x512.png', 'content':''}
    if discord_id != '':
        discord_id = '<@' + discord_id + '>'

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
