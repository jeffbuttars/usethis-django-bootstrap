#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

BSVERSION = '3.2.0'

setup(name='usethis-django-bootstrap',
      version='3.2.1',
      description="Bootstrap 3.2.0 for Django with themes and theme chooser.",
      author="Jeff Buttars",
      author_email="jeffbuttars@gmail.com",
      packages=['usethis_bootstrap'],
      url='https://github.com/jeffbuttars/usethis-django-bootstrap',
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Browsers',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      package_dir={'usethis_bootstrap': 'usethis_bootstrap'},
      package_data={'usethis_bootstrap':
                    ['static/bootstrap-%s/css/*' % BSVERSION,
                     'static/bootstrap-%s/fonts/*' % BSVERSION,
                     'static/bootstrap-%s/js/*.js' % BSVERSION,
                     'static/bootstrap-%s/*_css/*' % BSVERSION,
                     'templates/*.html',
                     ]}
      )
