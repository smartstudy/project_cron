from props import path
from datetime import datetime


def info(class_, message):
    _write('[INFO] %s - %s: %s\n' % (datetime.now(), class_, message))


def error(class_, message):
    _write('[ERROR] %s - %s: %s\n' % (datetime.now(), class_, message))


def newline():
    _write('\n\n')


def _write(line):
    open(path.LOG, 'a', encoding='utf8').write(line)
