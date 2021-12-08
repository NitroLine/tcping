import sys
import socket
import time
import signal
from timeit import default_timer as timer
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("host", type=str, help="Host for tcp ping",
                    metavar="HOST")
parser.add_argument("port", type=int, help="Port for tcp ping (default=80)", default=80,
                    metavar="PORT")
parser.add_argument("-c", "--count", type=int, default=10000,
                    metavar='MAX_COUNT', required=False,
                    help="max count of ping request")
args = parser.parse_args()
host = args.host
port = args.port
maxCount = args.count
count = 0
passed = 0
failed = 0


def signal_handler(signal, frame):
    getResults()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def getResults():
    lRate = 0
    if failed != 0:
        lRate = failed / (count) * 100
        lRate = "%.2f" % lRate
    print(f"\nTCP Ping Results: [{count}/{passed}/{failed}] Total/Pass/Fail (Failed: {lRate}%)")


while count < maxCount:
    count += 1
    success = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s_start = timer()
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
        success = True
    except socket.timeout:
        print("Connection timed out!")
        failed += 1
    except OSError as e:
        print("OS Error:", e)
        failed += 1
    s_stop = timer()
    s_runtime = "%.2f" % (1000 * (s_stop - s_start))
    if success:
        print(f"Connected to {host}:{port} tcp_seq={count - 1} time={s_runtime}ms")
        passed += 1
    if count < maxCount:
        time.sleep(1)

getResults()
