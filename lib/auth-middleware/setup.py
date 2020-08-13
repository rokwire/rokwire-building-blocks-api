#  Copyright 2020 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import setup

setup(
    name='auth-middleware',
    version='0.1.0',
    author='Frank Henard',
    author_email='fhena2@illinois.edu',
    packages=['auth_middleware'],
    # scripts=['bin/script1','bin/script2'],
    url='https://github.com/rokwire/rokwire-auth-middleware/',
    # license='LICENSE.txt',
    description='Rokwire Platform Auth Middleware',
    # long_description=open('README.txt').read(),
    install_requires=[
        'PyJWT>=1.7.1',
        'requests>=2.22.0',
        'cryptography>=2.7',
        # I would require flask here, but I want to use the version that the
        # "calling" app uses, and I don't see a way to guarantee that pip
        # installs the dependency in the correct order (eg. "calling app" first
        # then this module)
    ],
)
