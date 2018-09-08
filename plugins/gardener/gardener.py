#!/usr/bin/env python

import sys,os
import subprocess

def get_values(env):
  val = env.split(" ")
  # count: 1 val=cluster-info, 2 val=get ns, 3 val=get po -n dev
  return val

def exec_command(cmd):
 # print "split flag_val:", flag_val.split(" ")
 # cluster_ctx = flag_val.split(" ")[0]
 # cmd = "gardenctl target garden " + cluster_ctx
 # if len(flag_val.split(" ")) == 2 and "cluster-info" in flag_val:
 #   pass
 #   # CHECK
 # else:
 #   verb = flag_val.split(" ")[1]
 # cluster_ctx = flag_val.split(" ")[0]
  print "executing ", cmd
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = proc.communicate()
  if err:
    if "gardenctl" in cmd:
      print "check \"gardenctl\" PATH"
    else:
      print "invalid [verb, resource, namespace]:", val_list
  else:
    print "out:",out
  return out

def get_cluster_kubecfg(cluster_ctx, cluster_name):
  if "garden_ctx" in cluster_ctx:
    cmd = "gardenctl target garden " + cluster_name
    return exec_command(cmd)

def parse_values(cluster_ctx, flag_val, kctl):
  cluster_name = flag_val.split(" ")[0]
  cluster_kubecfg = get_cluster_kubecfg(cluster_ctx, cluster_name)
  print "cluster_kubecfg:", cluster_kubecfg
  kcfg_file = cluster_kubecfg.split("=")[1]
  
  val_list = flag_val.split(" ")
  if len(val_list) == 4:
    if "--all-namespaces" in val_list[3]:
      cmd = kctl + " " + val_list[1] + " " + val_list[2] + " " + val_list[3]
    else:
      cmd = kctl + " " + val_list[1] + " " + val_list[2] + " -n " + val_list[3]
  elif len(val_list) == 3:
    cmd = kctl + " " + val_list[1] + " " + val_list[2]
  elif len(val_list) == 2:
    if "cluster-info" in val_list[1]:
      cmd = kctl + " " + val_list[1]
    elif "all" in val_list[1]:
      cmd = "gardenctl ls gardens"
      garden_ls = exec_command(cmd) 
      if garden_ls:
        print "garden_ls:", garden_ls

  print "Executing :", cmd, "in context of ",kcfg_file 
  cmd += " --kubeconfig=" + kcfg_file
  return cmd

def exec_ls(ctx):
  if "gardens" in ctx:
    cmd = "gardenctl ls gardens"
  if "seeds" in ctx:
    cmd = "gardenctl ls seeds"
  if "shoots" in ctx:
    cmd = "gardenctl ls shoots"
  exec_command(cmd)
    
def main():
  garden_flag = 0
  seed_flag = 0
  shoot_flag = 0

  kctl = os.environ.get('KUBECTL_PLUGINS_CALLER')
  #print "plugin name:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_NAME')
  #print "command file:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_COMMAND')
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN'):
    garden_flag = 1
    garden_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN')
    if len(garden_flag_val.split(" ")) == 1 and "all" in garden_flag_val or "ls" in garden_flag_val:
      exec_ls("gardens")
      return

    cmd = parse_values("garden_ctx", garden_flag_val, kctl)
    exec_command(cmd)
  
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'):
    seed_flag = 1
    if not garden_flag:
      print "Set garden cluster context"
      return

    seed_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED')
    if len(seed_flag_val.split(" ")) == 1 and "all" in seed_flag_val or "ls" in seed_flag_val:
      exec_ls("seeds")
      return
    k8s_val = get_values(os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'))
    print "k8s_val:", k8s_val
    print "seeds list"
    print os.system("gardenctl ls seeds")
  
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT'):
    shoot_flag = 1
    shoot_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT')
    if len(flag_val.split(" ")) == 1 and "all" in shoot_flag_val or "ls" in shoot_flag_val:
      exec_ls("shoots")
      return
    k8s_val = get_values(os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT'))
    print "k8s_val:", k8s_val
    print "shoots list"
    print os.system("gardenctl ls shoots")

  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GETNS'):
    print "Current namespace context:", os.environ.get('KUBECTL_PLUGINS_CURRENT_NAMESPACE')

  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SETNS'):
    # need to save details in file to maintain state
    cn_ctx = os.environ.get('KUBECTL_PLUGINS_CURRENT_NAMESPACE')
    os.environ['KUBECTL_PLUGINS_CURRENT_NAMESPACE'] = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SETNS')
    new_ns_ctx = os.environ.get('KUBECTL_PLUGINS_CURRENT_NAMESPACE')
    prav = new_ns_ctx
    print "Changing namespace context from ", cn_ctx, " to ", new_ns_ctx

if __name__ == "__main__":
  print "gardener plugin helps switching between garden, seed, shoot easier\n"
  main()
