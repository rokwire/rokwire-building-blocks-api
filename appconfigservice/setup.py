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

from setuptools import find_namespace_packages, setup

setup(
    name='appconfig',
    version='1.0.0',
    description='The app config building block',
    package_dir={'': 'api'},
    packages=find_namespace_packages(where='api'),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', ],
    extras_require={
        'test': ['pytest', 'coverage', ],
    },
)
