#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='usethis-django-bootstrap',
      version='2.3.2.0',
      description="Bootstrap for Django with themes and theme chooser.",
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
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      package_dir={'usethis_bootstrap': 'usethis_bootstrap'},
      package_data={'usethis_bootstrap': 
                    ['static/bootstrap/css/*.css',
                     'static/bootstrap/img/*.png',
                     'static/bootstrap/js/*.js',
                     'static/bootstrap/*_css/*.css',
                     'templates/*.html',
                    ]}
)
