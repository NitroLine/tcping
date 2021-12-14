# tcping
tcp ping on python3

## Usage

```
usage: tcpping.py [-h] [-c MAX_COUNT] [-6] [-t TIME] HOST PORT [PORT ...]

positional arguments:
  HOST                  Host for tcp ping
  PORT                  Port for tcp ping (default=80)

optional arguments:
  -h, --help            show this help message and exit
  -c MAX_COUNT, --count MAX_COUNT
                        max count of ping request
  -6, --ipv6            flag for use IPv6 address
  -t TIME, --timeout TIME
                        ping timeout in seconds (default=1)
```

### Examples
```python3 tcping.py 8.8.8.8 53 443 80 ```

```python3 tcping.py -6 fe80::24d4:1fee:fa42:9d2d 5566 -t 5```