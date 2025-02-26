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
    parser.add_argument('domains', metavar='DOMAIN', type=str, nargs='+',
                        help='Domain names to check')
    parser.add_argument('--days', type=int, default=14,
                        help='Warn if certificate expiration is within specified days')
    args = parser.parse_args()

    for domain in args.domains:
        expires = ssl_expiry_datetime(domain)
        remaining = expires - datetime.now()
        if remaining < timedelta(days=args.days):
            print(f'{domain} SSL certificate will expire in {remaining.days} days')
        else:
            print(f'{domain} SSL certificate is up to date')




