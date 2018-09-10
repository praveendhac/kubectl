#!/usr/bin/env python

import sys,os
import subprocess

def exec_command(cmd):
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  out, err = proc.communicate()
  #print "out:", out, "err:", err, "cmd:", cmd
  if "export KUBECONFIG" in cmd:
    return None
  elif out:
    if "No match for" in out:
      print "Check cluster name!", out
      sys.exit(-1)
    return out
  else:
    print "Check if cluster name is correct!" + "err:" + err
    print "command executed:", cmd
    sys.exit(-1)

def get_cluster_kubecfg(cluster_ctx, cluster_name):
  if "garden_ctx" in cluster_ctx:
    cmd = "gardenctl target garden " + cluster_name
  if "seed_ctx" in cluster_ctx:
    cmd = "gardenctl target seed " + cluster_name
  if "shoot_ctx" in cluster_ctx:
    cmd = "gardenctl target shoot " + cluster_name
  # return KUBECONFIG
  kube_config = exec_command(cmd)
  return kube_config

def main():
  kctl = os.environ.get('KUBECTL_PLUGINS_CALLER')
  cluster_ctx_kcfg = ""

  garden_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN')
  if "ls" in garden_flag_val.split(" ")[0]:
    cmd = "gardenctl ls gardens"
    gardens_list = exec_command(cmd)
    print gardens_list
    return
  else:
    if not os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_CMD') and not os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'):
      print "Empty \"--cmd\", pass kubectl commands to execute in the clusters context"
      return
    cluster_ctx = "garden_ctx"
    garden_cluster_name = garden_flag_val.split(" ")[0]
    gcluster_kubecfg = get_cluster_kubecfg("garden_ctx", garden_cluster_name)
    garden_kcfg_file = gcluster_kubecfg.split("=")[1]
    cluster_ctx_kcfg = garden_kcfg_file
    garden_export = "export " + gcluster_kubecfg

  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'):
    cluster_ctx = "seed_ctx"
    seed_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED')
    seed_cluster_name = seed_flag_val.split(" ")[0]
    if "ls" in seed_flag_val.split(" ")[0]:
      print "garden_export:", garden_export
      exec_command(garden_export)
      cmd = "gardenctl ls seeds"
      seeds_list = exec_command(cmd)
      print seeds_list
      return
    else:
      if not os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_CMD') and not os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT'):
        print "Empty \"--cmd\", pass kubectl commands to execute in the clusters context"
        return
      cluster_ctx = "seed_ctx"
      seed_cluster_kubecfg = get_cluster_kubecfg("seed_ctx", seed_cluster_name)
      seed_kcfg_file = seed_cluster_kubecfg.split("=")[1]
      cluster_ctx_kcfg = seed_kcfg_file
      seed_export = "export " + gcluster_kubecfg

  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT'):
    cluster_ctx = "shoot_ctx"
    shoot_flag_val = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT')
    shoot_cluster_name = shoot_flag_val.split(" ")[0]
    if "ls" in shoot_flag_val.split(" ")[0]:
      print "seed_export:", seed_export
      # set cluster context to seed
      exec_command(seed_export)
      cmd = "kubectl get shoots --all-namespaces " + "--kubeconfig=" + garden_kcfg_file 
      shoots_list = exec_command(cmd)
      print shoots_list
      return
    else:
      if not os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_CMD'):
        print "Empty \"--cmd\", pass kubectl commands to execute in the clusters context"
        return
      cluster_ctx = "shoot_ctx"
      shoot_cluster_kubecfg = get_cluster_kubecfg("shoot_ctx", shoot_cluster_name)
      shoot_kcfg_file = shoot_cluster_kubecfg.split("=")[1]
      cluster_ctx_kcfg = shoot_kcfg_file

  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_CMD'):
    kctl_cmd = os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_CMD')
    if len(kctl_cmd.split(" ")) < 2:
      print "Minimum 2 words needed, say, \"kubectl cluster-info\" or \"kubectl get ns\" etc."
    if "kubectl " in kctl_cmd:
      # make sure replace the first kubectl
      cmd = kctl_cmd + " " + "--kubeconfig=" + cluster_ctx_kcfg 
      print "cmd:", cmd
      res = exec_command(cmd)
      print res
    else:
      print "only kubectl commands are allowed in \"--cmd\""

if __name__ == "__main__":
  print "gardener plugin helps switching between garden, seed, shoot clusters easier. Run with \"-h\" for help.\n"
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN'):
    main()
  else:
    print "Check help! gardener context missing"
