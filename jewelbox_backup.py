#!/usr/bin/env python3
import sys
import json
import getpass
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError


def main():
    username = input('username: ')
    password = getpass.getpass('password: ')

    r = Request('http://www.loxa.edu.tw/index.php')
    with urlopen(r) as response:
        phpsessid = response.getheader('set-cookie').split('; ')[0].split('=')[1]

    cookie = 'PHPSESSID={0}; Cookie_Allow=1'.format(phpsessid)
    data = {
        'loginname': username,
        'loginpswd': password
    }
    r = Request('http://www.loxa.edu.tw/check.php',
                data=urlencode(data).encode('utf8'),
                headers={'cookie': cookie},
                method='POST')
    try:
        response = urlopen(r)
    except HTTPError:
        sys.exit('Invalid username or password.')

    r = Request('http://www.loxa.edu.tw/index.php?login=1&show_msg=Y',
                headers={'cookie': cookie})
    response = urlopen(r)

    r = Request('http://www.loxa.edu.tw/jewelbox/foldertree.php',
                headers={'cookie': cookie})
    with urlopen(r) as response:
        html = response.read().decode('big5')

    # TODO: get file list and download data


if __name__ == '__main__':
    main()
