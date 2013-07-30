#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='usethis-django-bootstrap',
      version='1.0.0-2.3.2',
      description="Bootstrap for Django with themes",
      author="Jeff Buttars",
      author_email="jeffbuttars@gmail.com",
      packages=['usethis_bootstrap'],
      url='https://github.com/jeffbuttars/usethis-django-bootstrap',
      # data_files=[('static/bootstrap/img', 'static/bootstrap/img/*.png')],
      package_dir={'usethis_bootstrap': 'usethis_bootstrap'},
      package_data={'usethis_bootstrap': 
                    ['static/css/bsthemes/*/*.css',
                     'static/bootstrap/css/*.css',
                     'static/bootstrap/img/*.png',
                     'static/bootstrap/js/*.js',
                     'templates/*.html',
                    ]}
)
