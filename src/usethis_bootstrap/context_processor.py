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
    'theme_dir': 'bootstrap-%s' % BSVER,
}

_THEMES_SCANNED = False
_THEMES_CACHED = {'default': None, 'bootstrap': None}
_URLS_CACHED = None

# There are bootstrap settings in the project settings,
# override the defaults with them.
if hasattr(settings, 'BOOTSTRAP_SETTINGS'):
    BOOTSTRAP_SETTINGS.update(settings.BOOTSTRAP_SETTINGS)


def scan_themes():
    global _THEMES_CACHED
    global _THEMES_SCANNED

    # If we're in DEBUG, scan every time. Otherwise, just scan on import
    if not settings.DEBUG and _THEMES_SCANNED:
        # logger.debug("Using cached themes")
        return _THEMES_CACHED
        # _THEMES_SCANNED = True

    sroot = os.path.dirname(os.path.realpath(__file__))
    static_base = "{}bootstrap-{}".format(STATIC_URL, BSVER)

    if not sroot:
        # logger.debug("No static root")
        return _THEMES_CACHED

    tdir = BOOTSTRAP_SETTINGS.get('theme_dir', 'bootstrap-%s' % BSVER)
    ftdir = os.path.join(sroot, 'static', tdir)

    if not os.path.exists(ftdir):
        # logger.debug("Can't find theme dir %s", ftdir)
        return _THEMES_CACHED

    # Fill in the default bs theme
    _THEMES_CACHED['bootstrap'] = {
        'css': "{}/css/bootstrap-theme.css".format(ftdir, BSVER),
        'css_min': "{}/css/bootstrap-theme.min.css".format(ftdir, BSVER),
        'css_url': os.path.join(static_base, "css/bootstrap-theme.css"),
        'css_min_url': os.path.join(static_base, "css/bootstrap-theme.min.css"),
    }

    dlist = glob.glob(ftdir + "/*_css")
    # logger.debug("ftdir: %s, dlist %s", ftdir, dlist)
    for d in dlist:
        # logger.debug("d: %s", d)
        dp = os.path.join(ftdir, d)

        # logger.debug("Checking %s:%s, %s", d, os.path.isdir(dp), dp)
        # logger.debug("Checking %s:%s", os.path.join(dp, 'bootstrap.css'),
        #              os.path.exists(
        #                  os.path.join(dp, 'bootstrap.css')))
        # logger.debug("Checking %s:%s", os.path.join(dp, 'bootstrap.min.css'),
        #              os.path.exists(
        #                  os.path.join(dp, 'bootstrap.min.css')))

        db = os.path.basename(d)
        # logger.debug("db: %s", db)

        if os.path.isdir(dp):
            cssf = os.path.join(d, 'bootstrap.css')
            cssf_min = os.path.join(d, 'bootstrap.min.css')
            # logger.debug("cssf: %s, cssf_min: %s", cssf, cssf_min)

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

            # logger.debug("tdir: %s, cssf: %s, cssf_min: %s", tdir, cssf, cssf_min)

            db = db.split('_css', -1)[0]
            if cssf or cssf_min:
                _THEMES_CACHED[db] = {
                    'css': cssf,
                    'css_min': cssf_min,
                    'css_url': "{}/{}_css/bootstrap.css".format(static_base, db),
                    'css_min_url': "{}/{}_css/bootstrap.min.css".format(static_base, db),
                }
    # end for d in dlist

    _THEMES_SCANNED = True

    # logger.debug("Found themes: %s", _THEMES_CACHED)
    return _THEMES_CACHED
# scan_themes()


def bootstrap_urls(context):

    global _URLS_CACHED
    debug = settings.DEBUG

    # Find all available themes
    themes = scan_themes()
    theme = context.session.get("bootstrap_theme", BOOTSTRAP_SETTINGS['theme'])

    # If we're not in DEBUG mode and the urls have already been
    # processed, don't process them again unless we have too.

    # XXX
    # If something funny happens??? Not sure what to do yet.
    if not debug and _URLS_CACHED:
        # logger.info("Using cached urls")
        # If they haven't changed the theme, don't process any more
        if theme == _URLS_CACHED['BOOTSTRAP3_CUR_THEME']:
            return _URLS_CACHED

    # logger.info("Generating Bootstrap URLs")

    pre = '<link rel="stylesheet"'
    css_fmt = '{} href="{}" {extras}>'
    suffix = '.min'
    theme_css_url = None
    static_base = "{}bootstrap-{}".format(STATIC_URL, BSVER)

    if debug:
        suffix = ''

    # logger.debug("THEME: %s", theme)
    if theme in themes:
        if theme != 'default':
            titem = themes[theme]
            theme_css_url = titem['css_min_url'] or titem['css_url']

            if debug and titem['css_url']:
                theme_css_url = titem['css_url']

    js_url = '{}/js/bootstrap{}.js'.format(static_base, suffix)
    # phone_js_url = '{}bootstrap/js/bootstrap-phone-hack{}.js'.format(
    #     STATIC_URL, suffix)

    resp = {
        'BOOTSTRAP3_CSS': css_fmt.format(
            pre,
            '{}/css/bootstrap{}.css'.format(static_base, suffix),
            extras="media=\"screen\""),
        'BOOTSTRAP3_JS': '<script src="{}"></script>'.format(js_url),
        # 'BOOTSTRAP_PHONEHACK_JS': '<script src="{}"></script>'.format(phone_js_url),
    }

    if BOOTSTRAP_SETTINGS['enable_themes'] and themes:
        if theme_css_url:
            resp['BOOTSTRAP3_CSS'] += '\n' + css_fmt.format(pre, theme_css_url, extras="")

        tl = themes.keys()
        resp['BOOTSTRAP3_THEMES'] = sorted(tl)

        resp['BOOTSTRAP3_CUR_THEME'] = theme or 'default'

    _URLS_CACHED = resp
    # logger.debug("bootstrap URLS contexts: %s", resp)
    return resp

# Scan on startup
scan_themes()
