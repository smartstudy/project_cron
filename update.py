import os
import shutil
import setup
from utils import processutil


USER_ROOT = os.path.expanduser('~')
APP_NAME = setup.APP_NAME + '.app'
APP_ROOT = os.path.join('/usr/local/bin', setup.APP_NAME)
DST_PATH = os.path.join(APP_ROOT, setup.VERSION, APP_NAME)
SYMLINK_PATH = os.path.join(USER_ROOT, 'Applications', APP_NAME)


def update():
    if not os.path.exists('/usr/local/bin/terminal-notifier'):
        processutil.call(['/usr/local/bin/brew', 'install', 'terminal-notifier'])

    command = ['pip3', 'install', '-r', 'requirements.txt', '-U']
    processutil.call(command)

    command = ['python3', 'setup.py', 'py2app']
    processutil.call(command)

    if os.path.exists(SYMLINK_PATH):
        os.remove(SYMLINK_PATH)

    shutil.move(os.path.abspath(os.path.join('dist', APP_NAME)), DST_PATH)
    shutil.rmtree('dist')
    shutil.rmtree('build')
    os.symlink(DST_PATH, SYMLINK_PATH)


if __name__ == "__main__" and not os.path.exists(DST_PATH):
    update()

