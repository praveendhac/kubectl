# Gardener plugin
gardener plugin helps switching between garden, seed, shoot clusters easier.

```
$ kubectl plugin gardener -h
gardener plugin helps switching between garden, seed, shoot clusters easier. Run
with "-h" for help. If the flag values does not make sense, pass "all"

Options:
      --garden='': get details in Garden context
      --getgardenns='': get namespaces in garden cluster/context
      --getns='': current namespace context
      --getshootns='': get namespaces in shoot cluster/context
      --seed='': get details in Seed context
      --setns='': set namespace context to different namespace
      --shoot='': get details in Shoot context

Usage:
  kubectl plugin gardener [flags] [options]

Use "kubectl options" for a list of global command-line options (applies to all
commands).
```

* Run in Garden context
```
$ kubectl plugin gardener --garden="ls"
$ kubectl plugin gardener --garden="all"
Pick one of the garden's name from above command output
$ kubectl plugin gardener --garden="pd-dev get ns"
It is of the format
$ kubectl plugin gardener --garden="GARDEN-CLUSTER-NAME VERB RESOURCE NAMESPACE"
for all namespaces
$ kubectl plugin gardener --garden="GARDEN-CLUSTER-NAME VERB RESOURCE --all-namespaces"
```

* Run in Seed context
```
List seed clusters
$ kubectl plugin gardener --garden="pd-infra-garden" --seed="all"
Execute commands in seed cluster context
get Shoot namespaces in seed cluster 
kubectl plugin gardener --garden="pd-infra-garden" --seed="azure-westus-02 get ns"
get pods from one of the namespaces from above command
$ kubectl plugin gardener --garden="pd-infra-garden" --seed="azure-westus-02 get po shoot--pd-infra--infra-test"
the command is of the form
$ kubectl plugin gardener --garden="GARDEN-CLUSTER-NAME" --seed="SEED-CLUSTER-NAME VERB RESOURCE shoot-namespace-in-seed"
```

* Run in Shoot context
```
$ kubectl plugin gardener --garden="pd-infra-garden" --seed="azure-westus-02" --shoot="infra-test get ns"
get pods from one of the namespaces in Shoot cluster
$ kubectl plugin gardener --garden="pd-infra-garden" --seed="azure-westus-02" --shoot="infra-test get po pd-logging"
$ kubectl plugin gardener --garden="pd-security-garden" --seed="aws-westus-02" --shoot="secops get po pd-logging"
The commands are of the form
$ kubectl plugin gardener --garden="GARDEN-CLUSTER-NAME" --seed="SEED-CLUSTER-NAME" --shoot="SHOOT-CLUSTER-NAME VERB RESOURCE NAMESPACE"
The commands are of the form
```

## Feedback/Comments for improvement are welcome!!
