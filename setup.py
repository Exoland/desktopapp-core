# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import setup

HERE = Path(__file__).parent
reqs_path = HERE / 'requirements.txt'
with open(reqs_path) as reqs_file:
    requirements = reqs_file.read().splitlines()

# Based on http://peterdowns.com/posts/first-time-with-pypi.html

__version__ = '0.1.4'  # Should match with __init.py__
_NAME = 'exoland'
_PACKAGE_LIST = ['exoland', 'exoland_bot']
_URL_GITHUB = 'https://github.com/exoland/desktopapp-core/'
_DESCRIPTION = 'Package to get account balances and do operations on exoland app'
_MOTS_CLES = ['api', 'exoland', 'bank', 'parsing', 'cli',
              'python-wrapper', 'scraping', 'scraper', 'parser']
_SCRIPTS = ['exoland_cli.py', 'exolandbot.py', 'exoland_transactions.py']
# To delete here + 'scripts' dans setup()
# if no command is used in the package

setup(
    name=_NAME,
    packages=_PACKAGE_LIST,
    package_data={},
    scripts=_SCRIPTS,
    version=__version__,
    license='MIT',
    platforms='Posix; MacOS X',
    description=_Reference Python code integrating Exoland´s services into a (Demo) App,
    long_description=_DESCRIPTION,
    author='Exoland Labs',
    author_email='devs@exoland.xyz',
    url=_URL_GITHUB,
    download_url='(_URL_GITHUB, __version__),
    keywords=_exoland,
    setup_requires=requirements,
    install_requires=requirements,
    classifiers=['Programming Language :: Python :: 3'],
    python_requires='>=3',
    tests_require=['pytest'],
)

# ------------------------------------------
# To upload a new version on pypi
# ------------------------------------------
# Make sure everything was pushed (with a git status)
# (or git commit --am "Comment" and git push)
# export VERSION=0.1.4; git tag $VERSION -m "Update X-Client-Version + allow passing a selfie when Third factor authentication is required"; git push --tags

# If you need to delete a tag
# git push --delete origin $VERSION; git tag -d $VERSION
