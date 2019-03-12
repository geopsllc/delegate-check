# DPoS Monitoring Tool for Multiple Delegates Across Multiple Networks

## Installation

Basic install:
```sh
git clone https://github.com/geopsllc/delegate-check
cd delegate-check
bash install.sh
nano config.py
```
- change config.py to your liking
- test the script in cli mode by running ```python3 delcheck.py```

Frontend setup:
- add a crontab entry (```crontab -e```) to run the script every minute:
```* * * * * cd $HOME/delegate-check && python3 delcheck.py > /dev/null 2>&1```
- install and setup a webserver (apache/nginx) to serve folder web

## General

This is a DPoS Monitoring Tool for Multiple Delegates Across Multiple Networks.
- You can use it in cli mode or bring up a web interface that refreshes every minute. 
- You can enable AWS SNS intergration to send a SMS meesage when a delegate misses a block.
- [Sample Website](http://dashboard.geops.net)

## Changelog

### 0.1

- initial release

## Security

If you discover a security vulnerability within this package, please open an issue. All security vulnerabilities will be promptly addressed.

## Credits

- [All Contributors](../../contributors)
- [Georgi Stoyanov](https://github.com/geopsllc)

## License

[MIT](LICENSE) © [geopsllc](https://github.com/geopsllc)

