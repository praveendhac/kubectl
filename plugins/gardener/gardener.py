#!/usr/bin/env python

import sys,os
import argparse

def main():
  #print "kubectl path:", os.environ.get('KUBECTL_PLUGINS_CALLER')
  #print "plugin name:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_NAME')
  #print "command file:", os.environ.get('KUBECTL_PLUGINS_DESCRIPTOR_COMMAND')
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDENS'):
    print "garden list"
    print os.system("gardenctl ls gardens")
  
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SEEDS'):
    print "seeds list"
    print os.system("gardenctl ls seeds")
  
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_SHOOTS'):
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
