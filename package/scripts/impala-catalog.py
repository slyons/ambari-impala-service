# -*- coding: utf-8 -*-
import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.base import Fail
from resource_management.core.exceptions import ComponentIsNotRunning
from subprocess import call


class ImpalaCatalog(Script):
    #Call setup.sh to install the service
    def install(self, env):

        # Install packages listed in metainfo.xml
        self.install_packages(env)

        cmd = 'wget http://archive.cloudera.com/impala/ubuntu/precise/amd64/impala/cloudera.list ' \
              '-O /etc/apt/sources.list.d/cloudera.list '

        Execute('echo "Running ' + cmd + '"')
        Execute(cmd)

        cmd = 'apt-get update'
        Execute('echo "Running ' + cmd + '"')
        Execute(cmd)

        cmd = 'apt-get install -y impala-server impala-catalog impala-state-store impala-shell'
        Execute('echo "Running ' + cmd + '"')
        Execute(cmd)

        self.configure(env)

    def configure(self, env):
        import params

        env.set_params(params)


    #Call start.sh to start the service
    def start(self, env):
        cmd = 'service impala-catalog start'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    #Called to stop the service using the pidfile
    def stop(self, env):
        cmd = 'service impala-catalog stop'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    #Called to get status of the service using the pidfile
    def status(self, env):
        cmd = 'service impala-catalog status'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

if __name__ == "__main__":
    ImpalaCatalog().execute()
