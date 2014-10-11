import os
import os.path
import glob
from django.conf import settings  # import the settingsfile

import logging
logger = logging.getLogger('django.debug')

STATIC_URL = getattr(settings, 'STATIC_URL')
BSVER = '3.2.0'


# Our default settings.
BOOTSTRAP_SETTINGS = {
    'enable_themes': True,
    'theme': 'default',
    'use_cdn': True,
    'css_cdn': '//maxcdn.bootstrapcdn.com/bootstrap/{bsver}/css/bootstrap.min.css',
    'js_cdn': '//maxcdn.bootstrapcdn.com/bootstrap/{bsver}/js/bootstrap.min.js'
}

_THEMES_SCANNED = False
_THEMES_CACHED = {'default': None, 'bootstrap': None}
_URLS_CACHED = None

# There are bootstrap settings in the project settings,
# override the defaults with them.
if hasattr(settings, 'BOOTSTRAP_SETTINGS'):
    BOOTSTRAP_SETTINGS.update(settings.BOOTSTRAP_SETTINGS)

BOOTSTRAP_SETTINGS['css_cdn'] = BOOTSTRAP_SETTINGS['css_cdn'].format(bsver=BSVER)
BOOTSTRAP_SETTINGS['js_cdn'] = BOOTSTRAP_SETTINGS['js_cdn'].format(bsver=BSVER)
BOOTSTRAP_SETTINGS['theme_dir'] = 'bootstrap-{bsver}'.format(bsver=BSVER)


def scan_themes():
    global _THEMES_CACHED
    global _THEMES_SCANNED

    # If we're in DEBUG, scan every time. Otherwise, just scan on import
    if not settings.DEBUG and _THEMES_SCANNED:
        return _THEMES_CACHED

    sroot = os.path.dirname(os.path.realpath(__file__))
    static_base = "{}bootstrap-{}".format(STATIC_URL, BSVER)

    if not sroot:
        return _THEMES_CACHED

    tdir = BOOTSTRAP_SETTINGS.get('theme_dir')
    ftdir = os.path.join(sroot, 'static', tdir)

    if not os.path.exists(ftdir):
        return _THEMES_CACHED

    # Fill in the default bs theme
    _THEMES_CACHED['bootstrap'] = {
        'css': "{}/css/bootstrap-theme.css".format(ftdir, BSVER),
        'css_min': "{}/css/bootstrap-theme.min.css".format(ftdir, BSVER),
        'css_url': os.path.join(static_base, "css/bootstrap-theme.css"),
        'css_min_url': os.path.join(static_base, "css/bootstrap-theme.min.css"),
    }

    dlist = glob.glob(ftdir + "/*_css")
    for d in dlist:
        dp = os.path.join(ftdir, d)

        db = os.path.basename(d)

        if os.path.isdir(dp):
            cssf = os.path.join(d, 'bootstrap.css')
            cssf_min = os.path.join(d, 'bootstrap.min.css')

            if not os.path.exists(cssf):
                cssf = None
            else:
                cssf = os.path.join(tdir, db, 'bootstrap.css')
                cssf = 'bootstrap.css'

            if not os.path.exists(cssf_min):
                cssf_min = None
            else:
                cssf_min = os.path.join(tdir, db, 'bootstrap.min.css')
                cssf_min = 'bootstrap.min.css'

            db = db.split('_css', -1)[0]
            if cssf or cssf_min:
                _THEMES_CACHED[db] = {
                    'css': cssf,
                    'css_min': cssf_min,
                    'css_url': "{}/{}_css/bootstrap.css".format(static_base, db),
                    'css_min_url': "{}/{}_css/bootstrap.min.css".format(static_base, db),
                }

    _THEMES_SCANNED = True

    return _THEMES_CACHED


def bootstrap_urls(context):

    global _URLS_CACHED
    debug = settings.DEBUG

    # Find all available themes
    themes = scan_themes()

    logger.debug("themes %s", themes)

    theme = BOOTSTRAP_SETTINGS['theme']
    if hasattr(context, 'session'):
        theme = context.session.get("bootstrap_theme", BOOTSTRAP_SETTINGS['theme'])

    # If we're not in DEBUG mode and the urls have already been
    # processed, don't process them again unless we have too.
    # XXX
    # If something funny happens??? Not sure what to do yet.
    if not debug and _URLS_CACHED:
        # If they haven't changed the theme, don't process any more
        if theme == _URLS_CACHED['BOOTSTRAP_CUR_THEME']:
            logger.debug("CTX: %s", _URLS_CACHED)
            return _URLS_CACHED

    pre = '<link rel="stylesheet"'
    css_fmt = '{} href="{}" {extras}>'
    suffix = '.min'
    theme_css_url = None
    static_base = "{}bootstrap-{}".format(STATIC_URL, BSVER)

    if debug:
        suffix = ''

    if theme in themes:
        if theme != 'default':
            titem = themes[theme]
            theme_css_url = titem['css_min_url'] or titem['css_url']

            if debug and titem['css_url']:
                theme_css_url = titem['css_url']

    js_url = '{}/js/bootstrap{}.js'.format(static_base, suffix)

    resp = {}
    if BOOTSTRAP_SETTINGS.get('use_cdn'):
        resp['BOOTSTRAP_CSS'] = BOOTSTRAP_SETTINGS.get('css_cdn')
        resp['BOOTSTRAP_JS]'] = BOOTSTRAP_SETTINGS.get('js_cdn')
    else:
        resp['BOOTSTRAP_CSS'] = css_fmt.format(
                pre,
                '{}/css/bootstrap{}.css'.format(static_base, suffix),
                extras="media=\"screen\"")
        resp['BOOTSTRAP_JS'] = '<script src="{}"></script>'.format(js_url)

    if BOOTSTRAP_SETTINGS['enable_themes'] and themes:
        if theme_css_url:
            resp['BOOTSTRAP_CSS'] += '\n' + css_fmt.format(pre, theme_css_url, extras="")

        tl = themes.keys()
        resp['BOOTSTRAP_THEMES'] = sorted(tl)

        resp['BOOTSTRAP_CUR_THEME'] = theme or 'default'

    _URLS_CACHED = resp
    logger.debug("CTX: %s", resp)
    return resp

# Scan on startup/import
scan_themes()
