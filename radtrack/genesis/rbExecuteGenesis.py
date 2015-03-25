__author__ = 'swebb'

import os

class rbExecuteGenesis(object):

    def execute_genesis(self, input_name):

        try:
            commandline = 'echo ' + input_name + ' | genesis'
            print commandline
            os.system(commandline)

        except Exception:
            print 'Unable to execute Genesis on ' + input_name
            raise
