# Create a file named test.yaml

\# k3d configuration file
apiVersion: k3d.io/v1alpha4
kind: Simple
metadata:
  name: mycluster
servers: 1
agents: 2
image: rancher/k3s:v1.20.4-k3s1 # same as `--image rancher/k3s:v1.20.4-k3s1`

k3d cluster create --config test.yaml
- This will create your kubernetes cluster

