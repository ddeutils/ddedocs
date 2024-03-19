# Pod Scheduling

**Scheduling** in Kubernetes is a core component as it determines where a pod will
be launched. For every pod scheduler finds the best Node for launching it. There
are several ways available through which one can determine on what node, pods
can be placed.

Among these features, Node selector, affinity and anti-affinity, taints & toleration,
stand out as essential tools for fine-tuning pod placement according to specific
requirements.

Let’s take a look at some of them.

## Node Selector

**Node Selector** is the simplest yet effective way to control pod scheduling on
specific nodes in a Kubernetes cluster based on labels. Node Selector allows us
to specify a label query (key-value pairs defined in Pod spec) that must be
satisfied by a node for a pod to be scheduled on that node. This feature provides
a straightforward mechanism for pod placement according to simple matching
attributes like node labels.

We can label the nodes where we want specific pods to be scheduled:

```shell
kubectl label nodes <node-name> disktype=ssd
```

Specifying Node Selector in Pod Spec:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: spark-executors
spec:
  containers:
  - name: spark-executors
    image: apache-spark:v3.4.1
  nodeSelector:
    disktype: ssd
```

This pod will only be scheduled on nodes labeled with `disktype=ssd`.

## References

- [K8s for Data Engineers — Pod Scheduling](https://blog.devgenius.io/k8s-for-data-engineers-pod-scheduling-f5f994da6618)
