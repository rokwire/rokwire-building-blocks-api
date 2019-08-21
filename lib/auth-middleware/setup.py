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
