# dynamic-dns-updater
Update the IP address of a given domain using the [cPanel API 2](https://documentation.cpanel.net/display/SDK/Guide+to+cPanel+API+2).

## Basic Usage
```bash
updater.py -u <username> -p <password> <domain> <sub-domain list> <cpanel url>
```

__Example:__
```bash
updater.py -u username -p password mydomain.com sub1 sub2 https://my.cpanel.org:2083
```

## Installation Prerequisites
* [Python](https://www.python.org) v2.7+
* [Requests: HTTP for Humans](http://docs.python-requests.org/en/latest/) v2.9.1+

## Installation on Raspberry Pi

#### Install the latest Requests module in Python
TODO: update these instructions to use `pipenv` instead
```
sudo pip install requests
```

#### Install Code to `root` User's Home Folder
Create a bin folder in `root` user's home directory:
```
sudo mkdir /root/bin
```

Copy code to the bin directory:
```
sudo cp updater.py /root/bin
```

Make the file executable for the root user:
```
sudo chmod u+x /root/bin/updater.py
```

Create a parameters file:
```
sudo touch /root/bin/params
```

Only root user can read parameters file:
```
sudo chmod go-r /root/bin/params
```

Edit the parameters file to contain the account details for your cPanel account:
```
 -u username -p password example.com sub1 sub2 https://my.cpanel.org:2083
```

#### Run Updater Every 15 Minutes using CRON

Append the following 2 lines to your /etc/crontab file:

```
0,15,30,45 * * * * root cd /root/bin && cat params | xargs ./updater.py
@reboot            root cd /root/bin && cat params | xargs ./updater.py
```

