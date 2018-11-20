#!/usr/bin/env python
from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions.default import default
    
# server configurations
config = Script.get_config()

# params from mirrormaker-ambari-config
mirrormaker_groupname = config['configurations']['mirrormaker-ambari-config']['mirrormaker_groupname']
kafka_config_dir = config['configurations']['mirrormaker-ambari-config']['kafka_config_dir']

# params from mirrormaker-env
mirrormaker_log_dir = config['configurations']['mirrormaker-env']['mirrormaker_log_dir']
mirrormaker_home_dir = config['configurations']['mirrormaker-env']['mirrormaker_home_dir']
mirrormaker_user = config['configurations']['mirrormaker-env']['mirrormaker_user']
mirrormaker_log_file = mirrormaker_log_dir + '/mirrormaker.log'
