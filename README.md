# DPoS Monitoring Tool for Delegates Across Multiple Chains

## Installation

Basic install:
```sh
git clone https://github.com/geopsllc/delegate-check
cd delegate-check
bash install.sh
nano config.py
```
- `install.sh` installs the dependencies and creates `config.py` from `config.example.py`
- change config.py to your liking
- `config.py` and `web/local.js` are git-ignored, so `git pull` never touches your settings; new options show up in `config.example.py`
- optional: copy `web/local.example.js` to `web/local.js` to set a CoinGecko API key for the dashboard
- test the script in cli mode by running ```python3 delcheck.py```

Frontend setup:
- add a crontab entry (```crontab -e```) to run the script every minute:
```* * * * * cd $HOME/delegate-check && python3 delcheck.py > /dev/null 2>&1```
- install and setup a webserver (apache/nginx) to serve folder web

## General

This is a DPoS Monitoring Tool for Multiple Delegates Across Multiple Networks.
- Supports Core v2+.
- Requires Python 3.7 or above - native on Ubuntu 20.04.
- The backend is async coded so most api calls are made almost simultaneously.
- You can use it in cli mode or bring up a web interface that refreshes every 30 seconds. The backend writes `web/status.json` with raw values; the dashboard formats them (for example, "last block" ages are computed live in the browser) and warns when the data stops updating.
- You can enable Discord webhook notifications (with an optional @mention) when a delegate misses a block, stops forging, or its API checks keep failing, plus a message when it recovers.
- You can set `heartbeat_url` in config.py (e.g. a healthchecks.io ping URL) to get alerted when the script itself stops running.

## Changelog
### 1.5

- `config.py` is no longer tracked: copy `config.example.py` to `config.py` (`install.sh` does it); the CoinGecko key moved from `web/index.html` to the optional, git-ignored `web/local.js` (see `web/local.example.js`); a `.gitignore` covers both plus the generated files
- upgrading from 1.4 or earlier: back up your `config.py` (and your CoinGecko key if you added it to `web/index.html`), run `git checkout -- config.py web/index.html`, `git pull`, then restore `config.py` and put the key in `web/local.js`

### 1.4

- API requests are retried (3 attempts, 10 second timeout each, 2 and 4 second waits in between) on timeouts, connection errors, 5xx/429 responses and invalid JSON; the settings are at the top of `delcheck.py`
- failure reasons are more specific (e.g. `HTTP 502`, `timeout`), and non-retryable HTTP errors such as 404 are reported as failed requests instead of an `unexpected KeyError`

### 1.3

- the backend now writes `web/status.json` (raw values, including the yield and an `updated_at` timestamp) instead of `state.csv`; the dashboard formats everything, computes "X min(s) ago" live and shows a warning when the data is stale
- optional `heartbeat_url` ping after every completed run
- `status.json` and `state.json` are written atomically, and a corrupt `state.json` no longer stops the script
- the node status is requested once per network instead of once per delegate, and a delegate's requests run concurrently
- Discord alerts: recovery message when a delegate is healthy again, and an alert after 3 consecutive failed runs of the API checks
- removed the pandas dependency (only python3-aiohttp is needed now)

### 1.2

- replaced AWS SNS SMS alerts with Discord webhook notifications (aioboto3 is no longer required)
- a delegate is only marked as notified after Discord accepts the message, so failed notifications are retried on the next run

### 1.1

- compatibility with current Python versions (asyncio.run, timezone-aware datetimes)
- delegates whose API calls fail now show up with an error state instead of disappearing; failures are logged to stderr
- fixed a possible division by zero in the yield calculation

### 1.0

- official release

### 0.2

- added productivity column

### 0.1

- initial release

## Security

If you discover a security vulnerability within this package, please open an issue. All security vulnerabilities will be promptly addressed.

## Credits

- [All Contributors](../../contributors)
- [galperins4](https://github.com/galperins4)
- [Georgi Stoyanov](https://github.com/geopsllc)

## License

- [MIT](LICENSE) © [galperins4](https://github.com/galperins4)
- [MIT](LICENSE) © [geopsllc](https://github.com/geopsllc)
