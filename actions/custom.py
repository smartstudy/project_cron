from utils import processutil, logutil


def call(parameters):
    command = parameters["command"]
    cwd = parameters.get('cwd', None)
    out, err = processutil.call(command, cwd=cwd)

    logutil.info('Output', out)
    logutil.info('Error', err)
