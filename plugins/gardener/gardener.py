#!/usr/bin/env python

import sys,os
import subprocess

def get_values(env):
  val = env.split(" ")
  # count: 1 val=cluster-info, 2 val=get ns, 3 val=get po -n dev
  return val

def exec_command(cmd):
  print "EXECUTING: ", cmd
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = proc.communicate()
  print "OUT:", out, "ERR:", err
  if err:
    if "gardenctl" in cmd:
      out = err + " ,check \"gardenctl\" PATH"
    else:
      out = err, "may be invalid [verb, resource, namespace]"
  return out

def get_cluster_kubecfg(cluster_ctx, cluster_name):
  if "garden_ctx" in cluster_ctx:
    cmd = "gardenctl target garden " + cluster_name
  if "seed_ctx" in cluster_ctx:
    cmd = "gardenctl target seed " + cluster_name
  if "shoot_ctx" in cluster_ctx:
    cmd = "gardenctl target shoot " + cluster_name
  # return KUBECONFIG
  return exec_command(cmd)

def parse_values(cluster_ctx, flag_val, kctl):
  cluster_name = flag_val.split(" ")[0]
  if "garden_ctx" in cluster_ctx:
    cluster_kubecfg = get_cluster_kubecfg(cluster_ctx, cluster_name)
    print "PPPP:", cluster_ctx, flag_val, kctl, cluster_name
    print "cluster_kubecfg:", cluster_kubecfg
    kcfg_file = cluster_kubecfg.split("=")[1]
  elif "seed_ctx" in cluster_ctx:
    # get garden kubeconfig
    garden_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN')
    garden_cluster_name = garden_flag_val.split(" ")[0]
    gcluster_kubecfg = get_cluster_kubecfg("garden_ctx", garden_cluster_name)
    garden_kcfg_file = gcluster_kubecfg.split("=")[1]
    print "KCFGGG:", gcluster_kubecfg, garden_kcfg_file
    cmd = "export " + gcluster_kubecfg
    res = exec_command(cmd)
    # get seed kubeconfig in specified garden cluster
    #cmd = "gardenctl target seed " + cluster_name = flag_val.split(" ")[0]
    seed_cluster_kubecfg = get_cluster_kubecfg("seed_ctx", cluster_name)
    print "PQPQP:", seed_cluster_kubecfg 
    kcfg_file = seed_cluster_kubecfg.split("=")[1]

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
    elif len(val_list) == 1:
      pass

  print "Executing :", cmd, "in context of ",kcfg_file 
  cmd += " --kubeconfig=" + kcfg_file
  return cmd

def exec_ls(ctx):
  garden_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN')
  garden_cluster_name = garden_flag_val.split(" ")[0]

  if "gardens" in ctx:
    cmd = "gardenctl ls gardens"
  if "seeds" in ctx:
    # set garden context, where seed is located
    cluster_kubecfg = get_cluster_kubecfg("garden_ctx", garden_cluster_name)
    cmd = "export " + cluster_kubecfg
    res = exec_command(cmd)
    cmd = "gardenctl ls seeds"
  if "shoots" in ctx:
    # setting garden context is enough as garden talks to seed to get KUBECONFIG of shoots
    garden_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN')
    garden_cluster_name = garden_flag_val.split(" ")[0]
    cluster_kubecfg = get_cluster_kubecfg("garden_ctx", garden_cluster_name)
    cmd1 = "gardenctl ls shoots"
    cmd = "kubectl get shoots --all-namespaces " + "--kubeconfig=" + cluster_kubecfg.split("=")[1]
    print exec_command(cmd)
  res = exec_command(cmd)
  print res
    
def main():
  garden_flag = 0
  seed_flag = 0
  shoot_flag = 0

  kctl = os.environ.get('KUBECTL_PLUGINS_CALLER')
  #print "plugin name:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_NAME')
  #print "command file:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_COMMAND')
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN'):
    cluster_ctx = "garden_ctx"
    garden_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN')
    flag_val = garden_flag_val
    garden_cluster_name = garden_flag_val.split(" ")[0]
    if len(garden_flag_val.split(" ")) == 1:
      if "all" in garden_flag_val or "ls" in garden_flag_val:
        exec_ls("gardens")
        return
      elif os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'):
        pass
      else:
        print "Invalid value. Allowed values all, ls!"
        return


  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'):
    cluster_ctx = "seed_ctx"
    seed_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED')
    flag_val = seed_flag_val 
    seed_cluster_name = seed_flag_val.split(" ")[0]
    if len(seed_flag_val.split(" ")) == 1:
      if "all" in seed_flag_val or "ls" in seed_flag_val:
        exec_ls("seeds")
        return
      elif os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT'):
        pass
      else:
        print "Invalid value. Allowed values all, ls!"
        return
  
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT'):
    cluster_ctx = "shoot_ctx"
    shoot_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT')
    flag_val = shoot_flag_val 
    shoot_cluster_name = shoot_flag_val.split(" ")[0]
    if len(shoot_flag_val.split(" ")) == 1:
      if "all" in shoot_flag_val or "ls" in shoot_flag_val:
        exec_ls("shoots")
      else:
        print "Invalid value. Allowed values all, ls!"
      return

  cmd = parse_values(cluster_ctx, flag_val, kctl)
  res = exec_command(cmd)
  print res
  return

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
