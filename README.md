usethis-django-bootstrap
========================

# Version 3.3.4

My own Django app for easily including Bootstrap and Bootswatch into a Django project.

This is a drop in app that includes Bootstrap and Bootswatch sources and
minimized sources. This app provides context variables for templates that make
is easy to use Bootstrap in your Django project. There is also CDN support that
is enabled by default and will use a CDN when `DEBUG` is not enabled.


Also included is Bootswatch and a theme swicther drop down so you can easily try out
different styles and the click of a button.

## Installation

I highly recommend the use of [virtualenv](https://pypi.python.org/pypi/virtualenv)

The easiest and probably best way to install is with pip. Simply issue the
command:

    pip install usethis-django-bootstrap

## Configuration

Configure the app in your settings.py. Simply add `usethis_bootstrap` to your
`INSTALLED_APPS` and set some variables.

At a minimum you must add `'usethis_bootstrap.context_processor.bootstrap_urls'`
to your context processors. An example:

    from django.conf import global_settings

    TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        'usethis_bootstrap.context_processor.bootstrap_urls',
    )

Add the usethis-django-bootstrap package urls to yours:

```python
import usethis_bootstrap.urls


urlpatterns += [
        url(r'', include(usethis_bootstrap.urls)),
    ]
```

You can change settings with the `BOOTSTRAP_SETTINGS` dictionary in your
project `settings.py` file.

For example, to enable CDN usage when DEBUG is off and to set the default
theme/style to 'readable':

Here are the settings show with defaults.

```python
BOOTSTRAP_SETTINGS = {
    # enable theme selection
    'enable_themes': True,

    # Use a CDN when DEBUG is disabled
    'use_cdn': True,

    # Default theme name
    'theme': 'bootstrap',

    # CDN URL format for Boostrap CSS
    'css_cdn': '//maxcdn.bootstrapcdn.com/bootstrap/{bsver}/css/bootstrap.min.css',

    # CDN URL format for Boostrap JS
    'js_cdn': '//maxcdn.bootstrapcdn.com/bootstrap/{bsver}/js/bootstrap.min.js',

    # CDN URL format for Boostswatch CSS
    'bootswatch_cdn': '//maxcdn.bootstrapcdn.com/bootswatch/{bsver}/{theme}/bootstrap.min.css'
}
```

## Context Variables

The context variables made available:

* `BOOTSTRAP_CSS` The style tag for including bootstrap css
* `BOOTSTRAP_JS` The style tag for including bootstrap javascript
* `BOOTSTRAP_THEMES` A list of all available themes
* `BOOTSTRAP_CUR_THEME` The currently selected theme.

An example base template may look like the following template. 
You'll need to run the the variables through
the `|safe` filter for them to work.

At the end of the body is where the `BOOTSTRAP_JS` is used. Be sure to put your
Jquery JS tag ahead of the `BOOTSTRAP_JS` tag.

There is an example of including the theme chooser, `{% include
"bootstrap_theme_dropdown.html" %}`, in the nav bar.


```html
<!DOCTYPE HTML>
<html>
    <head>
    {% block page_head %}
        <title>{% block page_title %}Usethis Django Bootstrap{% endblock %}</title>

        {% block page_style_links %}
            {{ BOOTSTRAP_CSS|safe }}
            {{ BOOTSTRAP_THEME_CSS|safe }}

        {% endblock %}{# page_style_links #}

    {% endblock %}{# page_head #}
    </head>
    <body>
        {% block page_body %}
        {% block page_body_navbar %}
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">

                <a class="brand" href="/">Usethis Django Bootstrap</a>

                <div class="nav-collapse collapse">
                    <ul class="nav">
                    {% block page_body_navbar_items %}
                    {% if not user.is_anonymous %}

                    <li{% if request.path == "/" %} class="active"{% endif %}
                    ><a href="/">Home</a></li>

                    <li{% if request.path == "/account/user/" %} class="active"{% endif %}
                    ><a href="/account/user/">Account</a></li>
                    {% endif %}

                    {% if user.is_superuser %}
                        <li><a href="/admin">Site Admin</a></li>
                    {% endif %}

                    {% if user.is_anonymous %}
                        <li><a href="/account/login">Login</a></li>
                    {% else %}
                        <li><a href="/account/logout">Logout</a></li>
                    {% endif %}

                    {% endblock %}{# page_body_navbar_items #}
                    </ul>

                    {# Include the theme chooser, pulled to the right side of the nav bar #}
                    <div style="display: inline-block;" class="pull-right">
                        <ul class="nav pull-right">
                        {% include "bootstrap_theme_dropdown.html" %}
                        </ul>
                    </div>
                </div><!--/.nav-collapse -->
                </div>
            </div>
        </div>
        {% endblock %} {# page_body_navbar #}

        {% block page_body_container %}
        <div class="container">
            {% block page_body_container_inner %}
            {% endblock %}{# page_body_container_inner #}

            <div class="row">
                <div class="span12">
                <hr />
                <footer>
                {% block page_footer %}
                    <p>
                        &copy; Usethis Django Bootstrap 2013
                    </p>
                {% endblock %} {# page_footer #}
                </footer>
                </div>
            </div>
        </div> <!-- /container -->

        {% endblock %}{# page_body_container #}
        {% endblock %} {# page_body #}

        {% block page_bottom_js_links %}
            {# Include you jquery here, before bootstrap #}
            {{ BOOTSTRAP_JS|safe }}

        {% endblock %}{# page_bottom_js_links #}
        <script type="text/javascript" charset="utf-8">
        {% block page_bottom_js %}
        {% endblock %}{# page_bottom_js #}
        </script>
    </body>
</html>
```



## Using the Style Chooser

Included a simple template to help make adding a style chooser easy.
