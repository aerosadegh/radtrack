__author__ = 'swebb'

import subprocess


class rbExecuteGenesis(object):

    def execute_genesis(self, input_name):

        try:
            commandline = 'echo ' + input_name + '| genesis'
            subprocess.call(commandline)

        except Exception:
            print 'Unable to execute Genesis on' + input_name
            raise
