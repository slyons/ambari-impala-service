#!/usr/bin/env python
from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob
from resource_management.libraries.functions.version import format_hdp_stack_version
from resource_management.libraries.functions.default import default

config = Script.get_config()

#Core settings required
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
user_group = config['configurations']['cluster-env']['user_group']


impala_conf_dir = config['configurations']['impala-env']['impala_conf_dir']
impala_user = config['configurations']['impala-env']['impala_user']
impala_group = config['configurations']['impala-env']['impala_group']
impala_log_dir = config['configurations']['impala-env']['impala_log_dir']
impala_defaults_content = config['configurations']['impala-default']['content']
impala_log_file = os.path.join(impala_log_dir,'impala-setup.log')
