#!/usr/bin/env python
from resource_management.libraries.script.script import Script
import sys, os, glob
    
config = Script.get_config()

longrun_groupname = config['configurations']['longrun-ambari-config']['longrun_groupname']
white_list = config['configurations']['longrun-ambari-config']['white_list']
ack_value = config['configurations']['longrun-ambari-config']['ack_value']
broker_list = config['configurations']['longrun-ambari-config']['broker_list']

