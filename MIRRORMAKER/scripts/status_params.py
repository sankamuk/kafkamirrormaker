#!/usr/bin/env python
from resource_management import *
import sys, os

config = Script.get_config()

mirrormaker_pid_dir=config['configurations']['mirrormake-env']['mirrormaker_log_dir']
mirrormaker_pid_file=mirrormaker_pid_dir + '/mirrormaker.pid'

