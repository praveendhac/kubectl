# kubectl
kubectl plugins

Each plugin has it's own README

```
$ pwd
~/PRAVEENDHAC/kubectl
$ tree
.
├── LICENSE
├── README.md
└── plugins
    ├── gardener
    │   ├── README.md
    │   ├── gardener.py
    │   └── plugin.yaml
    ├── healthcheck
    │   ├── healthchecks.py
    │   └── plugin.yaml
    ├── operations
    │   ├── operations.py
    │   └── plugin.yaml
    └── security
        ├── plugin.yaml
        └── security.py
```

Coply all directories from this repo's plugins directory to `~/.kube/plugins/` on your local machine 

Plugins list
```
$ kubectl plugin
Runs a command-line plugin.

Plugins are subcommands that are not part of the major command-line distribution
and can even be provided by third-parties. Please refer to the documentation and
examples for more information about how to install and write your own plugins.

Available Commands:
  gardener     Gardener commands
  healthchecks Kubernetes health Checks
  operations   Kubernetes Security Checks
  security     Kubernetes Security Checks

Usage:
  kubectl plugin NAME [options]

Use "kubectl <command> --help" for more information about a given command.
Use "kubectl options" for a list of global command-line options (applies to all
commands).
```
* Reference
https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/

# only gardener plugin is available now, other plugins are for future releases
