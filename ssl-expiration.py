#!/usr/bin/env python
import ssl
import socket
from datetime import datetime
from datetime import timedelta
import argparse

def ssl_expiry_datetime(domain):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    hostname = domain[0]
    port = domain[1]

    context = ssl.create_default_context()
    try:
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname,
        )
        # 3 second timeout because Lambda has runtime limitations
        conn.settimeout(3.0)
    except (ssl.SSLError, socket.timeout, socket.gaierror) as e:
        return f"Error connecting to {hostname}: {e}"

    try:
        conn.connect((hostname, port))
        ssl_info = conn.getpeercert()
    except (ssl.SSLError, socket.timeout, socket.gaierror) as e:
        return f"Error connecting to {hostname}: {e}"

    # parse the string from the certificate into a Python datetime object
    return datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

if __name__ == '__main__':
    helpmsg = "Check SSL certificate expiration for given domains"
    parser = argparse.ArgumentParser(description=helpmsg)
    parser.add_argument('domains', metavar='domain[:port]', type=str, nargs='*', default=[],
                        help='Domain names to check (optional)')
    parser.add_argument('-d', '--days', metavar='days', type=int, default=9999,
                        help='Warn if certificate expiration is within specified days')
    parser.add_argument('-l', '--load', metavar='file', type=str, default=None,
                        help='Load domains from file')
    args = parser.parse_args()

    # Load domains from file
    if args.load:
        domains = []
        with open(args.load) as f:
            for line in f:
                url = line.split("#")[0].strip()
                if url:
                    fields = url.split(":")
                    if len(fields) == 2:
                        domain = fields[0]
                        port = int(fields[1])
                    else:
                        domain = url
                        port = 443
                    domains.append((domain, port))
    else:
        domains = []
        for url in args.domains:
            fields = url.split(":")
            if len(fields) == 2:
                domain = fields[0]
                port = int(fields[1])
            else:
                domain = url
                port = 443
            domains.append((domain, port))
    
    for domain in domains:
        expires = ssl_expiry_datetime(domain)
        if isinstance(expires, str):
            print(expires)
        else:
            remaining = expires - datetime.now()
            if remaining < timedelta(days=args.days):
                print(f'{domain[0]:20s} expires in {remaining.days:4d} days')
