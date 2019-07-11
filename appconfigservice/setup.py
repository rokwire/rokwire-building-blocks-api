import io

from setuptools import find_packages, setup

setup(
    name='appconfig',
    version='1.0.0',
    maintainer='Xiaoxia Liao',
    maintainer_email='xialiao@illinois.edu',
    description='The app config building block',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)