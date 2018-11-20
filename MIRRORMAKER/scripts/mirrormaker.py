import sys, os, pwd, grp, signal, time, glob
from resource_management import *
from subprocess import call

class Master(Script):
  def install(self, env):

    import params
    import status_params
      
    service_packagedir = os.path.realpath(__file__).split('/scripts')[0] 
            
    Execute('rm -rf ' + params.mirrormaker_home_dir, ignore_failures=True)
    Execute('rm -rf ' + params.mirrormaker_log_dir, ignore_failures=True)
            
    Directory([status_params.mirrormaker_pid_dir, params.mirrormaker_log_dir, params.mirrormaker_home_dir],
            owner=params.mirrormaker_user
    )   

    File(params.mirrormaker_log_file,
            mode=0644,
            owner=params.mirrormaker_user,
            content=''
    )
    
    Execute('echo Installing Mirror Maker')
    Execute('group='+params.mirrormaker_groupname+' >> '+params.mirrormaker_home_dir+'/source.configuration')
    Execute('group='+params.mirrormaker_groupname+' >> '+params.mirrormaker_home_dir+'/destination.configuration')
    Execute('chown '+params.mirrormaker_user+' '+params.mirrormaker_home_dir+'/source.configuration')
    Execute('chown '+params.mirrormaker_user+' '+params.mirrormaker_home_dir+'/destination.configuration')
  

  def configure(self, env, isInstall=False):

        
    
  def stop(self, env):
 
 
      
  def start(self, env):


  def check_mirrormaker_status(self, pid_file):


  def status(self, env):
    import status_params       
    from datetime import datetime
    self.check_mirrormaker_status(status_params.flink_pid_file)

  def set_conf_bin(self, env):

          
if __name__ == "__main__":
  Master().execute()
