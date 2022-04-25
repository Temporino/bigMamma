from setuptools import find_packages, setup

setup(
    name='sales',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'configparser',
        'flask',
        'google-api-core',
        'google-api-python-client',
        'google-auth',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'googleapis-common-protos',
        'requests',
        'httplib2',
        'Jinja2',
        'pytest'
    ],
)