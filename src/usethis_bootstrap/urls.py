# import sys
# print("path: " + str(sys.path))
from django.conf.urls import patterns, url
from usethis_bootstrap import views

urlpatterns = patterns(
    '',
    url(r'theme/(?P<theme>\w*)/$', views.theme,
        name='usethis-bootstrap-theme'),
)
