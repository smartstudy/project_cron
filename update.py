import os
import shutil
import setup
from utils import processutil


USER_ROOT = os.path.expanduser('~')
APP_NAME = setup.APP_NAME + '.app'
APP_ROOT = os.path.join('/usr/local/bin', setup.APP_NAME)
DST_PATH = os.path.join(APP_ROOT, '%s-%05X' % (setup.VERSION, setup.BUILD_NUMBER), APP_NAME)
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


def increase_build_number():
    SCRIPT_ROOT = os.path.dirname(__file__)
    SETUP = os.path.join(SCRIPT_ROOT, 'setup.py')

    lines = open(SETUP).readlines()
    with open(SETUP, 'w') as file:
        while len(lines) > 0:
            line = lines[0]
            if 'BUILD_NUMBER = ' in line:
                line = 'BUILD_NUMBER = %d\n' % (setup.BUILD_NUMBER + 1)

            file.write(line)
            lines.pop(0)


if __name__ == "__main__" and not os.path.exists(DST_PATH):
    increase_build_number()
    update()

