"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
APP_NAME = 'Project Cron'
DATA_FILES = ['icon.png']
VERSION = '0.1'
BUILD_NUMBER = 4
OPTIONS = {
    'argv_emulation': True,
    'plist': 'Info.plist',
    'packages': ['actions', 'models', 'utils']
}

if __name__ == "__main__":
    setup(
        app=APP,
        name=APP_NAME,
        version=VERSION,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
