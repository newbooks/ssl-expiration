#!/usr/bin/env python
import ssl
import socket
from datetime import datetime
from datetime import timedelta
import argparse

def ssl_expiry_datetime(hostname: str) -> datetime:
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

if __name__ == '__main__':
    helpmsg = "Check SSL certificate expiration for given domains"
    parser = argparse.ArgumentParser(description=helpmsg)
    parser.add_argument('domains', metavar='domain', type=str, default=[], nargs='+',
                        help='Domain names to check')
    parser.add_argument('-d', '--days', metavar='days', type=int, default=9999,
                        help='Warn if certificate expiration is within specified days')
    parser.add_argument('-l', '--load', metavar='file', type=str, default=None,
                        help='Load domains from file')
    args = parser.parse_args()

    # Load domains from file
    if args.load:
        with open(args.load) as f:
            domains = args.domains + f.read().splitlines()
    else:
        domains = args.domains

    for domain in domains:
        expires = ssl_expiry_datetime(domain)
        remaining = expires - datetime.now()
        if remaining < timedelta(days=args.days):
            print(f'{domain:20s} expires in {remaining.days:4d} days')
