import os
from datetime import datetime


def info(class_, message):
    _write('[INFO] %s - %s: %s\n' % (datetime.now(), class_, message))


def error(class_, message):
    _write('[ERROR] %s - %s: %s\n' % (datetime.now(), class_, message))


def newline():
    _write('\n\n')


def _write(line):
    USER_ROOT = os.path.expanduser('~')
    DOCUMENTS = os.path.join(USER_ROOT, 'Documents')
    open(os.path.join(DOCUMENTS, 'project_cron.log'), 'a', encoding='utf8') .write(line)
