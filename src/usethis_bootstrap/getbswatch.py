#!/usr/bin/env python
# encoding: utf-8


import os
import sys
import requests

this_dir = os.path.realpath(os.path.dirname(__file__))
THEME_META_FILE = "bootswatch_meta.json"


def main():
    bs_version = os.getenv('BS_VERSION', '3.3.5')
    bsw_api_version = os.getenv('BSW_API_VERSION', '3')

    outdir = os.getenv('BSW_OUTDIR', "{}/static/bootstrap-{}".format(
        this_dir, bs_version,
    ))
    theme_meta_file = os.path.join(this_dir, outdir, THEME_META_FILE)

    url = "http://api.bootswatch.com/{}/".format(bsw_api_version)

    resp = requests.get(url)
    if resp.status_code != 200:
        print("Got a bad status: %s" % resp.status_code)
        sys.exit(resp.status_code)

    # Save the response body
    with open(theme_meta_file, 'w') as fd:
        fd.write(str(resp.content, 'utf-8'))

    data = resp.json()
    # print(data)
    # ver = data['version']
    themes = data['themes']
    for theme in themes:
        for ct in ('css', 'cssMin'):
            print("Downloading {} {}".format(theme['name'], theme[ct]))
            resp = requests.get(theme[ct])
            if resp.status_code == 200:
                # print("Downloaded {name}".format(**theme))
                theme_dir = os.path.join(
                    outdir,
                    "{}_css".format(theme['name'].lower()))
                if not os.path.exists(theme_dir):
                    os.makedirs(theme_dir)
                outfile = os.path.join(theme_dir, os.path.basename(theme[ct]))

                with open(outfile, 'w') as fd:
                    fd.write(str(resp.content, 'utf-8'))
                    # print("Wrote {}\n".format(outfile))

if __name__ == '__main__':
    main()
