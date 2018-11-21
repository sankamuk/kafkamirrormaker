#!/usr/bin/env python
import sys, os
from resource_management.libraries.script.script import Script

config = Script.get_config()
longrun_home_dir = config['configurations']['longrun-env']['longrun_home_dir']
longrun_log_dir = config['configurations']['longrun-env']['longrun_log_dir']


longrun_pid_file = longrun_log_dir +'/longrun.pid'
longrun_log_file = longrun_log_dir +'/longrun.log'

longrun_conf_file = longrun_home_dir +'/longrun.conf'
longrun_script_file = longrun_home_dir +'/longrun.sh'
