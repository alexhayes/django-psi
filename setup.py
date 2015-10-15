import os
from setuptools import setup, find_packages

VERSION = __import__('psi').__version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-psi',
      version=VERSION,
      description='Google Pagespeed Insights for your Django project.',
      author='Kevin Fricovsky',
      author_email='kevin@montylounge.com',
      url='https://github.com/montylounge/django-psi/',
      packages=find_packages(),
      install_requires=['Django>=1.4', 'google-api-python-client==1.4.2', 'six>=1.2', 'django-appconf>=0.6', 'pillow>=2.6.1', 'jsonfield'],
      tests_require=['Django>=1.4', 'google-api-python-client==1.4.2', 'six>=1.2', 'django-appconf>=0.6', 'pillow>=2.6.1', 'jsonfield'],
      test_suite='run_tests.main',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   ],
)
