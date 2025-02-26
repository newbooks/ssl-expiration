# ssl-expiration

This is a script to detect the expiration date of a web site.

It takes in the website from command line with the option to:
- report the only sites whose expiration date is within certain days

Examples:
1. Query a single site
```
./ssl-expiration.py google.com
google.com SSL certificate will expire in 60 days
```

2. Query multiple sites
```
./ssl-expiration.py google.com apple.com netflix.com
google.com SSL certificate will expire in 60 days
apple.com SSL certificate will expire in 49 days
netflix.com SSL certificate will expire in 210 days
```

3. Query multiple sites specified in file
sample-sites.txt:
```
google.com
apple.com
youtube.com
amazon.com
```
Command:
```
./ssl-expiration.py $(cat sample-sites.txt)
google.com SSL certificate will expire in 60 days
apple.com SSL certificate will expire in 49 days
youtube.com SSL certificate will expire in 60 days
amazon.com SSL certificate will expire in 151 days
```

4. Only report sites that will expire within 50 days
```
./ssl-expiration.py --days 50 $(cat sample-sites.txt)
apple.com SSL certificate will expire in 49 days
```
