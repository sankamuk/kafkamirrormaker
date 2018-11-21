import sys, os, pwd, grp, signal, time, glob
from resource_management.libraries.script.script import Script
from resource_management.libraries import *
from resource_management.core import *
from subprocess import call
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
from ambari_commons import OSConst

class Longrun(Script):

  def install(self, env):
    import params
    import status_params
            
    Execute('rm -rf ' + status_params.longrun_home_dir, ignore_failures=True)
    Execute('rm -rf ' + status_params.longrun_log_dir, ignore_failures=True)
            
    Directory([status_params.longrun_log_dir, status_params.longrun_home_dir])

    File(status_params.longrun_log_file,mode=0644,content='')
    File(status_params.longrun_conf_file,mode=0644,content='#Config File')
    File(status_params.longrun_script_file,mode=755,content='#!/bin/bash')
    
    Execute('echo Installing ...')
    Execute('echo >> '+status_params.longrun_conf_file+ ' ')
    Execute('echo group='+params.longrun_groupname+' >> '+status_params.longrun_conf_file+ ' ')
    Execute('echo white='+params.white_list+' >> '+status_params.longrun_conf_file+ ' ')
    Execute('echo ack='+str(params.ack_value)+' >> '+status_params.longrun_conf_file+ ' ')
    Execute('echo broker='+params.broker_list+' >> '+status_params.longrun_conf_file+ ' ')

    Execute('echo >> '+status_params.longrun_script_file+ ' ')
    Execute('echo while : >> '+status_params.longrun_script_file+ ' ')
    Execute('echo do >> '+status_params.longrun_script_file+ ' ')
    Execute('echo date >> '+status_params.longrun_script_file+ ' ')
    Execute('echo done >> '+status_params.longrun_script_file+ ' ')

  def configure(self, env, isInstall=False):
    pass
    
  def stop(self, env):
    import status_params
    import params
    #env.set_params(status_params)
    #env.set_params(params)
    #self.configure(env)
    if not status_params.longrun_pid_file or not os.path.isfile(status_params.longrun_pid_file):
      raise ComponentIsNotRunning()
    pid = str(sudo.read_file(status_params.longrun_pid_file))
    try:
      Execute('kill '+ pid)
    except:
      raise
    Execute('rm -f '+status_params.longrun_pid_file, ignore_failures=True)
      
  def start(self, env):
    import status_params
    import params

    cmd = format("cd {status_params.longrun_log_dir}; nohup {status_params.longrun_script_file} >> {status_params.longrun_log_file} 2>> {status_params.longrun_log_file} &")
    try:
      Execute(cmd)
      Execute("ps -ef | grep "+status_params.longrun_script_file+" | grep -v grep | awk '{ print $2 }' | head -n1 >> "+status_params.longrun_pid_file)
    except:
      raise

  @OsFamilyFuncImpl(os_family=OsFamilyImpl.DEFAULT)
  def status(self, env):
    import status_params       
    from resource_management.libraries.functions.check_process_status import check_process_status
    check_process_status(status_params.longrun_pid_file)

if __name__ == "__main__":
  Longrun().execute()
