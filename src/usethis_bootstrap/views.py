from django.shortcuts import redirect


def theme(req, theme='bootstrap'):
    ref = req.META.get('HTTP_REFERER', '/')
    req.session['bootstrap_theme'] = theme
    return redirect(ref)
