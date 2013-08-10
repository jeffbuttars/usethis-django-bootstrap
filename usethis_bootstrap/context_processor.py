import os
import os.path
import glob
import re
from collections import OrderedDict
import copy
from django.conf import settings  # import the settingsfile

STATIC_URL = getattr(settings, 'STATIC_URL')


# Our default settings.
BOOTSTRAP_SETTINGS = {
    'enable_themes': True,
    'theme': 'default',
    'theme_dir': 'bootstrap',
    # 'version': '2.3.2',
}

_THEMES_SCANNED = False
_THEMES_CACHED = {'default': None}
bs_css_regex = re.compile('bootstrap(\.min)?.css')

# There are bootstrap settings in the project settings,
# override the defaults with them.
if hasattr(settings, 'BOOTSTRAP_SETTINGS'):
    BOOTSTRAP_SETTINGS.update(settings.BOOTSTRAP_SETTINGS)

def scan_themes():
    global _THEMES_CACHED
    global _THEMES_SCANNED
    sroot = os.path.dirname(os.path.realpath(__file__))

    # If we're in DEBUG, scan every time. Otherwise, just scan on import
    if not settings.DEBUG and _THEMES_SCANNED:
        print("Using cached themes")
        return _THEMES_CACHED
        # _THEMES_SCANNED = True
            
    if not sroot:
        print("No static root")
        return _THEMES_CACHED    

    tdir = BOOTSTRAP_SETTINGS.get('theme_dir', 'bootstrap')

    ftdir = os.path.join(sroot, 'static', tdir)
    if not os.path.exists(ftdir):
        print("Can't find theme dir %s" % ftdir)
        return _THEMES_CACHED    

    dlist = glob.glob(ftdir + "/*_css")
    print("ftdir: %s, dlist %s" % (ftdir, dlist))
    _THEMES_CACHED = {'default': None}
    for d in dlist:
        print("d: %s" % d)
        dp = os.path.join(ftdir, d)

        print("Checking %s:%s, %s" % (d, os.path.isdir(dp), dp))
        print("Checking %s:%s" % (os.path.join(dp, 'bootstrap.css'),
                                  os.path.exists(
                                      os.path.join(dp, 'bootstrap.css'))))
        print("Checking %s:%s" % (os.path.join(dp, 'bootstrap.min.css'),
                                  os.path.exists(
                                      os.path.join(dp, 'bootstrap.min.css'))))

        db = os.path.basename(d)
        print("db: %s" % db)

        if os.path.isdir(dp):
            cssf = os.path.join(dp, 'bootstrap.css')
            cssf_min = os.path.join(dp, 'bootstrap.min.css')
            print("cssf: %s, cssf_min: %s" % (cssf, cssf_min))

            if not os.path.exists(cssf):
                cssf = None
            else:
                cssf = os.path.join(tdir, db, 'bootstrap.css')

            if not os.path.exists(cssf_min):
                cssf_min = None
            else:
                cssf_min = os.path.join(tdir, db, 'bootstrap.min.css')

            print("tdir: %s, cssf: %s, cssf_min: %s" % (tdir, cssf, cssf_min))

            db = db.split('_css', -1)[0]
            if cssf or cssf_min:
                _THEMES_CACHED[db] = { 
                    'css': cssf,
                    'css_min': cssf_min,
                }
    # end for d in dlist
    

    _THEMES_SCANNED = True

    print("Found themes: %s" % _THEMES_CACHED)
    return _THEMES_CACHED
#scan_themes()


def bootstrap_urls(context):

    pre = '<link rel="stylesheet"'
    css_fmt = '{} href="{}" />'
    suffix = '.min'
    theme_dir = BOOTSTRAP_SETTINGS['theme_dir']
    css_dir = 'bootstrap/css'

    if settings.DEBUG:
        suffix = ''

    # Find all available themes
    themes = scan_themes()

    theme = context.session.get("bootstrap_theme", BOOTSTRAP_SETTINGS['theme'])
    # print("THEME: %s" % theme)
    if theme and theme != 'default' and theme in themes:

        titem = themes[theme]
        css_url = titem['css_min'] or titem['css']

        if settings.DEBUG and titem['css']:
            css_url = titem['css']

        css_url = '{}{}'.format(
            STATIC_URL, css_url)
    else:
        css_url = '{}{}/bootstrap{}.css'.format(
            STATIC_URL, css_dir, suffix)

    resp_url = '{}bootstrap/css/bootstrap-responsive{}.css'.format(
        STATIC_URL, suffix)

    js_url =  '{}bootstrap/js/bootstrap{}.js'.format(STATIC_URL, suffix)

    resp = {
        'BOOTSTRAP_CSS': css_fmt.format(pre, css_url),
        'BOOTSTRAP_RESPONSIVE_CSS': css_fmt.format(pre, resp_url),
        'BOOTSTRAP_JS': '<script src="{}"></script>'.format(js_url),
    }

    if BOOTSTRAP_SETTINGS['enable_themes'] and themes:
        resp['BOOTSTRAP_THEMES'] = OrderedDict(
            sorted(themes.items(), key=lambda t: t[0]))
        resp['BOOTSTRAP_CUR_THEME'] = theme or 'default'
            
    resp['BOOTSTRAP_COMBINED_CSS'] = '{}\n{}'.format(
        resp['BOOTSTRAP_CSS'], resp['BOOTSTRAP_RESPONSIVE_CSS']
    )

    return resp
