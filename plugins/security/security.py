#!/usr/bin/env python

import sys,os
import subprocess

if __name__ == "__main__":
  print "security plugin helps scanning kubernetes clusters. Run with \"-h\" for help. If the flag values does not make sense, pass \"all\"\n"
  if os.environ.get('KUBECTL_PLUGINS_LOCAL_FLAG_GARDEN'):
    main()
  else:
    print "Check help!"
