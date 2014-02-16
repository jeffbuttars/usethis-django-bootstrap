#!/usr/bin/env python
# encoding: utf-8


import requests
import sys


def main():
    url = "http://api.bootswatch.com/3/"

    resp = requests.get(url)
    if resp.status_code != 200:
        print("Got a bad status: %s" % resp.status_code)
        sys.exit(resp.status_code)

    data = resp.json()
    ver = data['version']
    themes = data['themes']
    for theme in themes:

        print("%s: %s" % (theme['name'], theme['description']))
    # end for theme in themes
# main()

if __name__ == '__main__':
    main()
