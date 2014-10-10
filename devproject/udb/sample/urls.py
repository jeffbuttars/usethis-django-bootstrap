
from django.conf.urls import patterns, include, url

import usethis_bootstrap.urls
import sample.views as s_views
import sample.urls
from sample.forms import BSAuthenticationForm


urlpatterns = patterns(
    '',
    url(r'^$', s_views.Index.as_view(), name='home'),
)
