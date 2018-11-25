#!/usr/bin/env python
import sys, os
from resource_management.libraries.script.script import Script

config = Script.get_config()

mirrormaker_home_dir = config['configurations']['mirrormaker-env']['mirrormaker_home_dir']
mirrormaker_log_dir = config['configurations']['mirrormaker-env']['mirrormaker_log_dir']
mirrormaker_user = config['configurations']['mirrormaker-env']['mirrormaker_user']

mirrormaker_pid_file = mirrormaker_log_dir +'/mirrormaker.pid'
mirrormaker_log_file = mirrormaker_log_dir +'/mirrormaker.log'

mirrormaker_script_file = mirrormaker_home_dir +'/mirrormaker.sh'
mirrormaker_source_file = mirrormaker_home_dir +'/mirrormaker.source.conf'
mirrormaker_destsn_file = mirrormaker_home_dir +'/mirrormaker.destination.conf'
