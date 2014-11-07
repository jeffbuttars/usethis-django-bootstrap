import os
import os.path
import json
from django.conf import settings  # import the settingsfile

# import logging
# logger = logging.getLogger('django.debug')

STATIC_URL = getattr(settings, 'STATIC_URL')
BSVER = '3.2.0'
BOOTSWATCH_META_FILE = "bootswatch_meta.json"


# Our default settings.
BOOTSTRAP_SETTINGS = {
    'enable_themes': True,
    'theme': 'bootstrap',
    'use_cdn': True,
    'css_cdn': '//maxcdn.bootstrapcdn.com/bootstrap/{bsver}/css/bootstrap.min.css',
    'js_cdn': '//maxcdn.bootstrapcdn.com/bootstrap/{bsver}/js/bootstrap.min.js',
    'bootswatch_cdn': '//maxcdn.bootstrapcdn.com/bootswatch/{bsver}/{theme}/bootstrap.min.css'
}

_THEMES_SCANNED = False
_THEMES_CACHED = {}
_URLS_CACHED = None
_THEME_LIST = []
_BS_BASE = {}

# There are bootstrap settings in the project settings,
# override the defaults with them.
if hasattr(settings, 'BOOTSTRAP_SETTINGS'):
    BOOTSTRAP_SETTINGS.update(settings.BOOTSTRAP_SETTINGS)

BOOTSTRAP_SETTINGS['js_cdn'] = BOOTSTRAP_SETTINGS['js_cdn'].format(bsver=BSVER)
BOOTSTRAP_SETTINGS['theme_dir'] = 'bootstrap-{bsver}'.format(bsver=BSVER)


def scan_themes():
    global _THEMES_CACHED
    global _THEMES_SCANNED
    global _THEME_LIST
    global _BS_BASE

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

    # Read in the bootswatch meta data
    bsw_meta = {}
    with open(os.path.join(ftdir, BOOTSWATCH_META_FILE), 'r') as fd:
        bsw_meta = json.loads(fd.read())

    # Fill in the default bs theme
    _THEMES_CACHED['bootstrap'] = {
        'name': 'Bootstrap',
        'css': os.path.join(static_base, "css/bootstrap-theme.css"),
        'cssMin': os.path.join(static_base, "css/bootstrap-theme.min.css"),
        'description': 'Default Bootstrap',
        'thumbnail': '',
        'less': '',
        'cssCdn': BOOTSTRAP_SETTINGS.get('css_cdn').format(bsver=BSVER),
        'lessVariables': '',
        'preview': '',
        'cssMin': '',
    }

    # Bootstrap base css
    _BS_BASE = {
        'css': os.path.join(static_base, "css/bootstrap.css"),
        'cssMin': os.path.join(static_base, "css/bootstrap.min.css"),
        'cssCdn': BOOTSTRAP_SETTINGS.get('css_cdn').format(bsver=BSVER),
    }

    # Create the theme data from the meta data
    for t in bsw_meta['themes']:
        t_name = t['name'].lower()
        _THEMES_CACHED[t_name] = t
        _THEMES_CACHED[t_name].update(
            {
                'css': "{}/{}_css/bootstrap.css".format(static_base, t_name),
                'cssMin': "{}/{}_css/bootstrap.min.css".format(static_base, t_name),
            }
        )

    _THEME_LIST = sorted(_THEMES_CACHED.keys())
    _THEMES_SCANNED = True
    return _THEMES_CACHED


def bootstrap_urls(context):

    global _URLS_CACHED
    debug = settings.DEBUG

    # Find all available themes
    themes = scan_themes()

    theme = BOOTSTRAP_SETTINGS['theme']
    if hasattr(context, 'session'):
        theme = context.session.get("bootstrap_theme", BOOTSTRAP_SETTINGS['theme'])

    if theme not in themes:
        theme = 'bootstrap'

    # If we're not in DEBUG mode and the urls have already been
    # processed, don't process them again unless we have too.
    if not debug and _URLS_CACHED:
        # If they haven't changed the theme, don't process any more
        if theme == _URLS_CACHED['BOOTSTRAP_CUR_THEME']:
            return _URLS_CACHED

    pre = '<link rel="stylesheet"'
    css_fmt = '{} href="{}" {extras}>'
    static_base = "{}bootstrap-{}".format(STATIC_URL, BSVER)

    titem = themes.get(theme, {})
    extras = "media=\"screen\""
    resp = {'BOOTSTRAP_THEMES': _THEME_LIST}

    url_key = 'cssMin'

    if debug:
        url_key = 'css'
    elif BOOTSTRAP_SETTINGS['use_cdn']:
        url_key = 'cssCdn'

    # Build the bootstrap url starting with the base theme/css
    resp['BOOTSTRAP_CSS'] = css_fmt.format(pre, _BS_BASE[url_key], extras=extras)

    # Build the bootstrap JS url
    if debug:
        js_url = '{}/js/bootstrap.js'.format(static_base)
    elif BOOTSTRAP_SETTINGS.get('use_cdn'):
        js_url = BOOTSTRAP_SETTINGS.get('js_cdn')
    else:
        js_url = '{}/js/bootstrap.min.js'.format(static_base)

    resp['BOOTSTRAP_JS'] = '<script src="{}"></script>'.format(js_url)

    # If themes are enable, add the theme file tag
    if BOOTSTRAP_SETTINGS.get('enable_themes') and theme:
        resp['BOOTSTRAP_CSS'] += '\n' + css_fmt.format(pre, titem[url_key], extras="")
        resp['BOOTSTRAP_CUR_THEME'] = theme or 'bootstrap'
        resp['BOOTSTRAP_CUR_THEME_META'] = titem

    _URLS_CACHED = resp
    return resp

# Scan on startup/import
scan_themes()
