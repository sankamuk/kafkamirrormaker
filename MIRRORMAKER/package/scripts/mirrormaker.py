#!/usr/bin/env python
import sys, os, pwd, grp, signal, time, glob
from resource_management.libraries.script.script import Script
from resource_management.libraries import *
from resource_management.core import *
from subprocess import call
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
from ambari_commons import OSConst

class Mirrormaker(Script):

  def install(self, env):
    import params
    import status_params
            
    Execute('rm -rf ' + status_params.mirrormaker_home_dir, ignore_failures=True)
    Execute('rm -rf ' + status_params.mirrormaker_log_dir, ignore_failures=True)
            
    Directory([status_params.mirrormaker_log_dir, status_params.mirrormaker_home_dir] ,owner=status_params.mirrormaker_user)
    File(status_params.mirrormaker_log_file,mode=0644,owner=status_params.mirrormaker_user)

    self.configure(env)

  def configure(self, env, isInstall=False):
    import status_params
    import params

    Execute('rm -f '+status_params.mirrormaker_script_file, ignore_failures=True)
    Execute('rm -f '+status_params.mirrormaker_source_file, ignore_failures=True)
    Execute('rm -f '+status_params.mirrormaker_destsn_file, ignore_failures=True)
    Execute('rm -f /usr/bin/mirrormaker.sh', ignore_failures=True)

    File(status_params.mirrormaker_script_file,mode=0755,owner=status_params.mirrormaker_user)
    File(status_params.mirrormaker_source_file,mode=0644,owner=status_params.mirrormaker_user)
    File(status_params.mirrormaker_destsn_file,mode=0644,owner=status_params.mirrormaker_user)
    Execute('ln -s '+status_params.mirrormaker_script_file+' /usr/bin/mirrormaker.sh')

    Execute('echo bootstrap.servers='+params.source_broker+' >> '+status_params.mirrormaker_source_file)
    Execute('echo group.id='+params.mirrormaker_groupname+' >> '+status_params.mirrormaker_source_file)
    Execute('echo bootstrap.servers='+params.destination_broker+' >> '+status_params.mirrormaker_destsn_file)

    Execute('echo "#!/bin/bash" >> '+status_params.mirrormaker_script_file)
    Execute('echo "#MirrorMaker Tool" >> '+status_params.mirrormaker_script_file)
    Execute('echo >> '+status_params.mirrormaker_script_file)
    Execute("echo 'arg=$1' >> "+status_params.mirrormaker_script_file)
    Execute("echo 'export KAFKA_OPTS=-Dkafka.logs.dir="+status_params.mirrormaker_log_dir+"' >> "+status_params.mirrormaker_script_file)
    Execute('echo >> '+status_params.mirrormaker_script_file)

    Execute("echo 'kafkastart() {' >> "+status_params.mirrormaker_script_file)
    Execute('echo cd '+status_params.mirrormaker_log_dir+' >> '+status_params.mirrormaker_script_file)
    Execute('echo "/usr/hdp/2.4.0.0-169/kafka/bin/kafka-mirror-maker.sh --new.consumer --consumer.config '+status_params.mirrormaker_source_file+' --producer.config '+status_params.mirrormaker_destsn_file+' --whitelist \''+params.white_list+'\' > '+status_params.mirrormaker_log_file+' 2>&1 &" >> '+status_params.mirrormaker_script_file)
    Execute("echo 'sleep 2' >> "+status_params.mirrormaker_script_file)
    Execute('echo "ps -ef | grep java | grep MirrorMaker | grep -v grep | tail -n1 | awk \'{ print \$2 }\' > '+status_params.mirrormaker_pid_file+'" >> '+status_params.mirrormaker_script_file)

    Execute('echo } >> '+status_params.mirrormaker_script_file)
    Execute('echo >> '+status_params.mirrormaker_script_file)
    Execute("echo 'kafkastop() {' >> "+status_params.mirrormaker_script_file)
    Execute("echo 'mmpid=$(cat "+status_params.mirrormaker_pid_file+")' >> "+status_params.mirrormaker_script_file)
    Execute("echo '[ ! -z ${mmpid} ] && kill ${mmpid}' >> "+status_params.mirrormaker_script_file)
    Execute("echo 'sleep 5' >> "+status_params.mirrormaker_script_file)
    Execute('echo "mmpid=\$(ps -ef | grep java | grep MirrorMaker | grep -v grep | awk \'{ print \$2 }\')" >> '+status_params.mirrormaker_script_file)
    Execute("echo '[ -z ${mmpid} ] && rm -f "+status_params.mirrormaker_pid_file+"' >> "+status_params.mirrormaker_script_file)
    Execute('echo } >> '+status_params.mirrormaker_script_file)
    Execute('echo >> '+status_params.mirrormaker_script_file)
    Execute("echo 'kafkastatus() {' >> "+status_params.mirrormaker_script_file)
    Execute('echo "mmpid=\$(ps -ef | grep java | grep MirrorMaker | grep -v grep | awk \'{ print \$2 }\')" >> '+status_params.mirrormaker_script_file)
    Execute("echo 'if [ -z ${mmpid} ] ; then' >> "+status_params.mirrormaker_script_file)
    Execute("echo 'exit 1' >> "+status_params.mirrormaker_script_file)
    Execute('echo else >> '+status_params.mirrormaker_script_file)
    Execute("echo 'exit 0' >> "+status_params.mirrormaker_script_file)
    Execute('echo fi >> '+status_params.mirrormaker_script_file) 
    Execute('echo } >> '+status_params.mirrormaker_script_file)
    Execute('echo >> '+status_params.mirrormaker_script_file)

    Execute("echo 'case $arg in' >> "+status_params.mirrormaker_script_file)
    Execute("echo 'start)' >> "+status_params.mirrormaker_script_file)
    Execute('echo kafkastart >> '+status_params.mirrormaker_script_file)
    Execute("echo ';;' >> "+status_params.mirrormaker_script_file)
    Execute("echo 'stop)' >> "+status_params.mirrormaker_script_file)
    Execute('echo kafkastop >> '+status_params.mirrormaker_script_file)
    Execute("echo ';;' >> "+status_params.mirrormaker_script_file)
    Execute("echo 'status)' >> "+status_params.mirrormaker_script_file)
    Execute('echo kafkastatus >> '+status_params.mirrormaker_script_file)
    Execute("echo ';;' >> "+status_params.mirrormaker_script_file)
    Execute('echo esac >> '+status_params.mirrormaker_script_file)
    Execute('echo >> '+status_params.mirrormaker_script_file)

    
  def stop(self, env):
    import status_params
    import params
    
    cmd = format("/usr/bin/mirrormaker.sh stop")
    try:
      Execute(cmd, user=status_params.mirrormaker_user)
    except:
      raise
      
  def start(self, env):
    import status_params
    import params

    self.configure(env)

    cmd = format("/usr/bin/mirrormaker.sh start")
    try:
      Execute(cmd, user=status_params.mirrormaker_user)
    except:
      raise

  @OsFamilyFuncImpl(os_family=OsFamilyImpl.DEFAULT)
  def status(self, env):
    import status_params       
    from resource_management.libraries.functions.check_process_status import check_process_status
    check_process_status(status_params.mirrormaker_pid_file)

if __name__ == "__main__":
  Mirrormaker().execute()
