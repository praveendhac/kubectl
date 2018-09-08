# Gardener plugin
gardener plugin helps switching between garden, seed, shoot clusters easier.

```
$ kubectl plugin gardener -h
gardener plugin helps switching between garden, seed, shoot easier. Run with
"-h" for help. If the flag values does not make sense, pass "all"

Options:
      --gardens='': get garden details
      --getgardenns='': get namespaces in garden cluster/context
      --getns='': current namespace context
      --getshootns='': get namespaces in shoot cluster/context
      --seeds='': get seed details
      --setns='': set namespace context to different namespace
      --shoots='': get shoot details

Usage:
  kubectl plugin gardener [flags] [options]

Use "kubectl options" for a list of global command-line options (applies to all
commands).
```
Run as
```
kubectl plugin gardener --gardens='all' --seeds='all' --shoots='all'
```
or
```
kubectl plugin gardener --gardens='all' 
```
