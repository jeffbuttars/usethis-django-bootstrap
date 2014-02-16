from django.shortcuts import redirect

def theme(req, theme='default'):
    print("SETTING THEME TO %s" % theme)

    ref = req.META.get('HTTP_REFERER', '/')

    req.session['bootstrap_theme'] = theme
    print("THEME: %s" % theme)

    return redirect(ref)
#theme()
