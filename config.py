# Discord Webhook (notifications)
discord_enabled = 'no' # yes/no
discord_webhook = 'https://discord.com/api/webhooks/webhookId/webhookToken'
discord_id = '' # optional Discord user id to @mention, leave empty for no mention

# Webhook JSON
if discord_enabled == 'yes':
    ntfy = {'avatar_url':'https://www.shareicon.net/download/128x128//2015/09/17/102426_freebsd_512x512.png', 'content':''}
    if discord_id != '':
        discord_id = '<@' + discord_id + '>'

# Heartbeat (optional, e.g. a healthchecks.io ping URL; pinged after every completed run)
heartbeat_url = ''

# Delegate Names
# Leave only the networks and delegates that you use!
delegates = {
    'Ark':['name'],
    'DArk':['name1','name2']
}

# Don't change the rest unless you know what you're doing!

# Network APIs
nodes = {
    'Ark':'https://api.ark.io/api',
    'DArk':'https://dapi.ark.io/api'
}

# Network Settings [delegates, blocktime]
db = {
    'Ark':[51, 8],
    'DArk':[53, 8]
}
