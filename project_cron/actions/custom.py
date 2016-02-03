from project_cron.utils import processutil, logutil


def call(parameters):
    command = parameters["command"]
    cwd = parameters.get('cwd', None)
    ret_code, out, err = processutil.call(command, cwd=cwd)

    logutil.info('Return Code', str(ret_code))
    logutil.info('Output', out)
    logutil.info('Error', err)
