# -*- coding: utf-8 -*-
import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.base import Fail
from resource_management.core.exceptions import ComponentIsNotRunning
from subprocess import call


class ImpalaDaemon(Script):
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

        env_content = InlineTemplate(params.impala_defaults_content)
        File("/etc/default/impala", content=env_content, owner=params.impala_user, group=params.impala_group)

        XmlConfig("hdfs-site.xml",
            conf_dir=params.impala_conf_dir,
            configurations=params.config['configurations']['hdfs-site'],
            configuration_attributes=params.config['configuration_attributes']['hdfs-site'],
            owner=params.impala_user,
            group=params.impala_group
        )

        XmlConfig("core-site.xml",
            conf_dir=params.impala_conf_dir,
            configurations=params.config['configurations']['core-site'],
            configuration_attributes=params.config['configuration_attributes']['core-site'],
            owner=params.impala_user,
            group=params.impala_group,
            mode=0644
        )

        XmlConfig("hbase-site.xml",
            conf_dir = params.impala_conf_dir,
            configurations = params.config['configurations']['hbase-site'],
            configuration_attributes=params.config['configuration_attributes']['hbase-site']
        )

        XmlConfig("hive-site.xml",
          conf_dir=params.impala_conf_dir,
          configurations=params.config['configuration_attributes']['hive-site'],
          owner=params.impala_user,
          group=params.impala_group,
          mode=0644
        )


    #Call start.sh to start the service
    def start(self, env):
        self.configure(env)
        cmd = 'service impala-server start'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    #Called to stop the service using the pidfile
    def stop(self, env):
        cmd = 'service impala-server stop'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    #Called to get status of the service using the pidfile
    def status(self, env):
        cmd = 'service impala-server status'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def setup_config(self, env):
        import params
        env.set_params(params)


        

if __name__ == "__main__":
    ImpalaDaemon().execute()
