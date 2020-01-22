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
