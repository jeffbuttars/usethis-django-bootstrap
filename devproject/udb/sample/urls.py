
from django.conf.urls import url
import sample.views as s_views


urlpatterns = [
    url(r'^$', s_views.Index.as_view(), name='home'),
    url(r'^bases/$', s_views.Bases.as_view(), name='bases_index'),
    url(r'^bases/starter/$', s_views.BasesStarter.as_view(), name='bases_starter'),
    url(r'^bases/jumbotron/$', s_views.BasesJumbotron.as_view(), name='bases_jumbotron'),
    url(r'^bases/narrow-jumbotron/$', s_views.BasesNarrowJumbotron.as_view(), name='bases_narrow_jumbotron'),
]
