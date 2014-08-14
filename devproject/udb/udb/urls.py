from django.conf.urls import patterns, include, url

import usethis_bootstrap.urls
import sample.views as s_views


urlpatterns = patterns(
    '',
    url(r'', include(usethis_bootstrap.urls)),
    url(r'^$', s_views.Index.as_view(), name='home'),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
