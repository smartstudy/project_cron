import os
from subprocess import Popen, PIPE
from utils import logutil


def call(command, cwd=None):
    _install_package_if_not_exists(command)
    logutil.info('Execute', ' '.join(command))
    popen = Popen(command, stdout=PIPE, stderr=PIPE, env=_get_env(), cwd=cwd)
    out, err = popen.communicate()
    if popen.returncode != 0:
        logutil.error('Return Code', popen.returncode)
        logutil.error('Output', out.decode('utf8', errors='ignore'))
        logutil.error('Error', err.decode('utf8', errors='ignore'))

    return popen.returncode, out.decode('utf8', errors='ignore'), err.decode('utf8', errors='ignore')


def _get_env():
    env = os.environ.copy()
    env['__PYVENV_LAUNCHER__'] = '/usr/local/bin/python3'
    if 'PYTHONHOME' in env:
        env.pop('PYTHONHOME')
    if 'PYTHONPATH' in env:
        env.pop('PYTHONPATH')
    env['PATH'] = '/usr/local/bin:/usr/local/sbin:%s' % (env['PATH'] if 'PATH' in env else '')

    return env


def _install_package_if_not_exists(command):
    if os.path.exists(command[0]) or command[0].find('/usr/local/bin') == -1:
        return

    package_name = os.path.split(command[0])[1]
    if package_name == 'ffmpeg':
        command = ['/usr/local/bin/brew', 'install', 'ffmpeg', '--with-libass', '--with-faac']
    elif package_name == 'mkvmerge':
        command = ['/usr/local/bin/brew', 'install', 'mkvtoolnix']
    else:
        command = ['/usr/local/bin/brew', 'install', package_name]

    Popen(command, env=_get_env()).communicate()
