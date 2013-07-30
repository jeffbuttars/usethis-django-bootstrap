#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='usethis-django-bootstrap',
      version='1.0.0-3.0.0-rc1',
      description="Bootstrap for Django with themes and theme chooser.",
      author="Jeff Buttars",
      author_email="jeffbuttars@gmail.com",
      packages=['usethis_bootstrap'],
      url='https://github.com/jeffbuttars/usethis-django-bootstrap',
      package_dir={'usethis_bootstrap': 'usethis_bootstrap'},
      package_data={'usethis_bootstrap': 
                    ['static/css/bsthemes/*/*.css',
                     'static/bootstrap/css/*.css',
                     'static/bootstrap/img/*.png',
                     'static/bootstrap/js/*.js',
                     'templates/*.html',
                    ]}
)
