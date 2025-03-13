#!/usr/bin/env python
import ssl
import socket
from datetime import datetime, timedelta
import argparse

def ssl_expiry_datetime(hostname, port=443):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    try:
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname) as conn:
            conn.settimeout(3.0)
            conn.connect((hostname, port))
            ssl_info = conn.getpeercert()
            return datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    except (ssl.SSLError, socket.timeout, socket.gaierror) as e:
        return f"Error connecting to {hostname}: {e}"

def load_domains(file):
    with open(file) as f:
        return [(line.split("#")[0].strip().split(":")[0], int(line.split("#")[0].strip().split(":")[1]) if ":" in line else 443) for line in f if line.split("#")[0].strip()]

def parse_domains(domains):
    return [(domain.split(":")[0], int(domain.split(":")[1]) if ":" in domain else 443) for domain in domains]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check SSL certificate expiration for given domains")
    parser.add_argument('domains', metavar='domain[:port]', type=str, nargs='*', default=[], help='Domain names to check (optional)')
    parser.add_argument('-d', '--days', metavar='days', type=int, default=9999, help='Warn if certificate expiration is within specified days')
    parser.add_argument('-l', '--load', metavar='file', type=str, help='Load domains from file')
    args = parser.parse_args()

    domains = load_domains(args.load) if args.load else parse_domains(args.domains)
    print(domains)
    for hostname, port in domains:
        expires = ssl_expiry_datetime(hostname, port)
        if isinstance(expires, str):
            print(expires)
        else:
            remaining = expires - datetime.now()
            if remaining < timedelta(days=args.days):
                print(f'{hostname:20s} expires in {remaining.days:4d} days')
