#!/usr/bin/env python
from resource_management.libraries.script.script import Script
import sys, os, glob
    
config = Script.get_config()

mirrormaker_groupname = config['configurations']['mirrormaker-ambari-config']['mirrormaker_groupname']
white_list = config['configurations']['mirrormaker-ambari-config']['white_list']
source_broker = config['configurations']['mirrormaker-ambari-config']['source_broker']
destination_broker = config['configurations']['mirrormaker-ambari-config']['destination_broker']

