import argparse
import signal
import socket
import sys
import time
from timeit import default_timer as timer

parser = argparse.ArgumentParser()
parser.add_argument("host", type=str, help="Host for tcp ping",
                    metavar="HOST")
parser.add_argument("ports", type=int, help="Port for tcp ping (default=80)", default=[80],
                    metavar="PORT", nargs='+')
parser.add_argument("-c", "--count", type=int, default=10000,
                    metavar='MAX_COUNT', required=False,
                    help="max count of ping request (default=10000)")
parser.add_argument("-6", "--ipv6", action="store_true",
                    help="flag for use IPv6 address")
parser.add_argument("-t", "--timeout", type=float, default=1, metavar='TIME', required=False,
                    help="ping timeout in seconds (default=1)")
args = parser.parse_args()
host = args.host
ports = args.ports
maxCount = args.count
count = 0

ports_status = dict()
for port in ports:
    ports_status[port] = {'count': 0, 'passed': 0, 'failed': 0}


def signal_handler(signal, frame):
    get_results()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def get_results():
    for port, status in ports_status.items():
        lRate = 0
        if status['failed'] != 0:
            lRate = status['failed'] / (status['count']) * 100
            lRate = "%.2f" % lRate
        print(f"\nTCP Ping Results for {port} port: [{status['count']}"
              f"/{status['passed']}/{status['failed']}] "
              f"Total/Pass/Fail (Failed: {lRate}%)")


while count < maxCount:
    count += 1
    for port in ports_status:
        ports_status[port]['count'] += 1
        success = False
        if not args.ip6:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        s.settimeout(args.timeout)
        s_start = timer()
        try:
            s.connect((host, port))
            s.shutdown(socket.SHUT_RD)
            success = True
        except socket.timeout:
            print(f"{port} port: Connection timed out!")
            ports_status[port]['failed'] += 1
        except OSError as e:
            print(f"{port} port - OS Error: {e}")
            ports_status[port]['failed'] += 1
        s_stop = timer()
        s_runtime = "%.2f" % (1000 * (s_stop - s_start))
        if success:
            print(f"Connected to {host}:{port} tcp_seq={count - 1} time={s_runtime}ms")
            ports_status[port]['passed'] += 1
    if count < maxCount:
        time.sleep(1)
get_results()
