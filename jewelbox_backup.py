#!/usr/bin/env python3
import os
import re
import sys
import getpass
from urllib.request import Request, urlopen, URLopener
from urllib.parse import urlencode, urlparse
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

    folder_tree_pattern = re.compile('insFld\(.+?, gFld\(".+?", "file_list.php\?dir_id=(\d+?)", "\w"\)\);')
    file_url_pattern = re.compile('<td colspan=3 nowrap>\s+?<a href="(http.+?)"')
    for i in folder_tree_pattern.finditer(html):
        dir_id = i.group(1)
        r = Request('http://www.loxa.edu.tw/jewelbox/file_list.php?dir_id={0}'.format(dir_id),
                    headers={'cookie': cookie})
        with urlopen(r) as response:
            html = response.read().decode('big5')

            for i in file_url_pattern.finditer(html):
                url = i.group(1)
                url_data = urlparse(url)
                file_path = url_data.path.lstrip('/')
                dir_name, base_name = os.path.split(file_path)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                url_opener = URLopener()
                url_opener.addheader('cookie', cookie)
                print('Download: {0} -> {1}'.format(url, file_path))
                url_opener.retrieve(url, file_path)


if __name__ == '__main__':
    main()
