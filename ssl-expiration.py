#!/usr/bin/env python
import ssl
import socket
from datetime import datetime

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
    #hostname = 'math.levich.net'
    hostname = 'www.google.com'
    print(ssl_expiry_datetime(hostname))
