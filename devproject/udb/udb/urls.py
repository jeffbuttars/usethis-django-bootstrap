from django.conf.urls import patterns, include, url
from django.contrib import admin

import usethis_bootstrap.urls
import sample.urls
from sample.forms import BSAuthenticationForm
from django.contrib.auth.views import login as login_view, logout as logout_view


urlpatterns = patterns(
    '',
    url(r'^login/$',
        login_view,
        {'template_name': 'sample_login.html',
         "authentication_form": BSAuthenticationForm
        },
       name='login'
       ),
    url(r'^logout/$',
        logout_view,
        {'next_page': '/'},
       name='logout'
       ),
    url(r'^', include(sample.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(usethis_bootstrap.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
