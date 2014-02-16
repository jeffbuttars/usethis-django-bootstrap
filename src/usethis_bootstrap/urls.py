from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'theme/(?P<theme>\w*)/$', views.theme,
                           name='usethis-bootstrap-theme'),
                      )
