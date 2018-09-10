# Gardener plugin
gardener plugin helps switching between garden, seed and shoot clusters easier.
Copy this folder (gardener) into "~/.kube/plugins" on *nix, Apple Mac machines. Should work on windows too!

* this plugin heavily depends on _gardenctl_ command, make sure gardenctl is in the path and garden config file is configured accordingly.

* Gardener plugin help
```
$ kubectl plugin gardener -h
gardener plugin helps switching between garden, seed, shoot clusters easier. Run
with "-h" for help. If the flag values does not make sense, pass "all"

Examples:
  kubectl plugin gardener --garden="GARDEN-NAME" --seed="SEED-NAME"
--cmd="KUBECTL-COMMAND"

Options:
      --cmd='': execute command in garden, seed, shoot context
      --garden='': get details in Garden context
      --seed='': get details in Seed context
      --shoot='': get details in Shoot context

Usage:
  kubectl plugin gardener [flags] [options]

Use "kubectl options" for a list of global command-line options (applies to all
commands).
```

* Run in Garden context
```
List garden clusters
$ kubectl plugin gardener --garden="ls"
Pick one of the garden's name from above command output
$ kubectl plugin gardener --garden="pd-dev-garden" --cmd="kubectl get ns"
$ kubectl plugin gardener --garden="pd-dev-garden" --cmd="kubectl cluster-info"
$ kubectl plugin gardener --garden="pd-dev-garden" --cmd="kubectl get po -n garden"
$ kubectl plugin gardener --garden="pd-dev-garden" --cmd="kubectl get po -n --all-namespaces"

It is of the format
$ kubectl plugin gardener --garden="GARDEN-CLUSTER-NAME" --cmd="KUBECTL-COMMANDS-IN-GARDEN-CONTEXT" 
```

* Run in Seed context
```
List seed clusters in specific garden context
$ kubectl plugin gardener --garden="pd-sec-garden" --seed="ls"

Pick one of the seed's name from above command output
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="azure-westus-02" --cmd="kubectl get ns"
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="azure-westus-02" --cmd="kubectl cluster-info"
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="aws-westus-02" --cmd="kubectl get po -n shoot--pd--pd"
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="aws-westus-02" --cmd="kubectl get po -n --all-namespaces"

It is of the format
$ kubectl plugin gardener --garden="GARDEN-CLUSTER-NAME" --seed="SEED-CLUSTER-NAME" --cmd="KUBECTL-COMMANDS-IN-SEED-CONTEXT"
```

* Run in Shoot context
```
List shoot clusters in specific garden and seed context
$ kubectl plugin gardener --garden="pd-sec-garden" --seed="azure-westus-02" --shoot="ls"

Pick one of the seed's name from above command output
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="azure-westus-02" --shoot="test" --cmd="kubectl get ns"
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="azure-westus-02" --shoot="pd" --cmd="kubectl cluster-info"
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="aws-westus-02" --shoot="forensics" --cmd="kubectl get po -n shoot--pd--pd"
$ kubectl plugin gardener --garden="pd-dev-garden" --seed="aws-westus-02" --shoot="pentest" --cmd="kubectl get po -n --all-namespaces"

It is of the format
$ kubectl plugin gardener --garden="GARDEN-CLUSTER-NAME" --seed="SEED-CLUSTER-NAME" ---shoot="SHOOT_-CLUSTER-NAME" -cmd="KUBECTL-COMMANDS-IN-GARDEN-SEED-SHOOT-CONTEXT"
```

## Feedback/Comments for improvement are welcome!!
