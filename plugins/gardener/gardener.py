#!/usr/bin/env python

import sys,os
import subprocess

def get_values(env):
  val = env.split(" ")
  # count: 1 val=cluster-info, 2 val=get ns, 3 val=get po -n dev
  return val

def exec_command(val_list, kctl, kube_ctx):
  kcfg_file = kube_ctx.split("=")[1]
  if len(val_list) == 3:
    if "--all-namespaces" in val_list[2]:
      cmd = kctl + " " + val_list[0] + " " + val_list[1] + " " + val_list[2]
    else:
      cmd = kctl + " " + val_list[0] + " " + val_list[1] + " -n " + val_list[2]
  elif len(val_list) == 2:
    cmd = kctl + " " + val_list[0] + " " + val_list[1]
  elif len(val_list) == 1:
    if "cluster-info" in val_list[0]:
      cmd = kctl + " " + val_list[0]
    elif "all" in val_list[0]:
      cmd = "gardenctl ls gardens"
      proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      kctx, err = proc.communicate()
      if not err:
        print "kctx:", kctx
        return
  else:
    print "invalid [verb, resource, namespace]:", val_list
  print "Executing :", cmd, "in context of ",kube_ctx 
  cmd += " --kubeconfig=" + kcfg_file
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  kout, err = proc.communicate()
  if not err:
      print "kout:\n", kout

def main():
  kctl = os.environ.get('KUBECTL_PLUGINS_CALLER')
  #print "plugin name:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_NAME')
  #print "command file:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_COMMAND')
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN'):
    cmd = "gardenctl target garden msa-dev-garden"
    try:
      proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      kctx, err = proc.communicate()
      if not err:
        print "kctx:", kctx
    except:
      print "gardenctl not present, check PATH"
      return

    k8s_val = get_values(os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN'))
    exec_command(k8s_val, kctl, kctx)
  
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'):
    k8s_val = get_values(os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEED'))
    print "k8s_val:", k8s_val
    print "seeds list"
    print os.system("gardenctl ls seeds")
  
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOT'):
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
