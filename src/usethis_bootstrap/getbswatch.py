#!/usr/bin/env python
# encoding: utf-8


import os
import sys
import shutil
import requests

this_dir = os.path.realpath(os.path.dirname(__file__))

def main():
    bs_version = os.getenv('BS_VERSION', '3.1.1')
    bsw_api_version = os.getenv('BSW_API_VERSION', '3')

    outdir = os.getenv('BSW_OUTDIR', "{}/static/bootstrap-{}".format(
        this_dir, bs_version,
    ))

    url = "http://api.bootswatch.com/{}/".format(bsw_api_version)

    resp = requests.get(url)
    if resp.status_code != 200:
        print("Got a bad status: %s" % resp.status_code)
        sys.exit(resp.status_code)

    data = resp.json()
    ver = data['version']
    themes = data['themes']
    for theme in themes:
        #print("%s : %s" % (theme['name'], theme['description']))
        # print("{name} {cssMin}".format(**theme))
        print("Downloading {name} {cssMin}".format(**theme))
        resp = requests.get(theme['cssMin'])
        if resp.status_code == 200:
            print("Downloaded {name}".format(**theme))
            theme_dir = os.path.join(
                outdir,
                "{}_css".format(theme['name'].lower()))
            if os.path.exists(theme_dir):
                shutil.rmtree(theme_dir)
            os.makedirs(theme_dir)
            outfile = os.path.join(theme_dir, 'bootstrap.min.css')
            fd = open(outfile, 'w')
            # print(dir(resp))
            fd.write(resp.content)
            print("Wrote {}\n".format(outfile))

    # end for theme in themes
# main()

if __name__ == '__main__':
    main()