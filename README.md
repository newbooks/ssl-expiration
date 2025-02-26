# ssl-expiration

This is a script to detect the expiration date of a web site.

It takes in the website from command line with the option to:
- report the only sites whose expiration date is within certain days

Examples:
1. Query a single site
```
ssl-expiration.py example.com
```

2. Query multiple sites
```
ssl-expiration.py example1.com example1.com example2.com example3.com
```

3. Query multiple sites specified in file
sites.txt:
```
example1.com
example2.com
example3.com
```
Command:
```
ssl-expiration.py < sitest.txt
```

4. Only report sites that will expire within 14 days
```
ssl-expiration.py -e 14 < sitest.txt
```
