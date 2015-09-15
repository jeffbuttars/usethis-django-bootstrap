from django.conf.urls import url
from usethis_bootstrap import views

urlpatterns = [
    url(r'theme/(?P<theme>\w*)/$', views.theme,
        name='usethis-bootstrap-theme'),
]
