# -*- coding: utf-8 -*-
import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.base import Fail
from resource_management.core.exceptions import ComponentIsNotRunning
from subprocess import call


class StateStore(Script):
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

        cmd = 'apt-get install -y --force-yes impala-server impala-catalog impala-state-store impala-shell'
        Execute('echo "Running ' + cmd + '"')
        Execute(cmd)

        self.configure(env)

    def configure(self, env):
        import params

        env.set_params(params)


    #Call start.sh to start the service
    def start(self, env):
        import params
        self.configure(env)

        self.create_hdfs_user(params.impala_user)

        cmd = 'cp /etc/impala/conf/impala.defaults /etc/default/impala'
        #Execute('echo "Running cmd: ' + cmd + '"')
        #Execute(cmd)

        cmd = 'service impala-state-store start'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    #Called to stop the service using the pidfile
    def stop(self, env):
        cmd = 'service impala-state-store stop'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    #Called to get status of the service using the pidfile
    def status(self, env):
        cmd = 'service impala-state-store status'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def create_hdfs_user(self, user):
        Execute('hadoop fs -mkdir -p /user/'+user, user='hdfs', ignore_failures=True)
        Execute('hadoop fs -chown ' + user + ' /user/'+user, user='hdfs')
        Execute('hadoop fs -chgrp ' + user + ' /user/'+user, user='hdfs')

if __name__ == "__main__":
    StateStore().execute()
