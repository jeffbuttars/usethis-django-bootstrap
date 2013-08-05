#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='usethis-django-bootstrap',
      version='1.0.1-2.3.2',
      description="Bootstrap for Django with themes and theme chooser.",
      author="Jeff Buttars",
      author_email="jeffbuttars@gmail.com",
      packages=['usethis_bootstrap'],
      url='https://github.com/jeffbuttars/usethis-django-bootstrap',
      download_url='https://github.com/jeffbuttars/usethis-django-bootstrap/releases/download/1.0/usethis-django-bootstrap-1.0.0-2.3.2.tar.gz',
      package_dir={'usethis_bootstrap': 'usethis_bootstrap'},
      package_data={'usethis_bootstrap': 
                    ['static/css/bsthemes/*/*.css',
                     'static/bootstrap/css/*.css',
                     'static/bootstrap/img/*.png',
                     'static/bootstrap/js/*.js',
                     'templates/*.html',
                    ]}
)
