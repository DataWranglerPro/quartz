# Examples followed
- [https://ronekins.com/2021/11/11/getting-started-with-the-oracle-database-kubernetes-operator-part-1/](https://ronekins.com/2021/11/11/getting-started-with-the-oracle-database-kubernetes-operator-part-1/)
- [https://thedatabaseme.de/2022/05/21/bastard-operator-from-hell-giving-the-kubernetes-oracle-database-operator-a-try/](https://thedatabaseme.de/2022/05/21/bastard-operator-from-hell-giving-the-kubernetes-oracle-database-operator-a-try/)

- [https://container-registry.oracle.com](https://container-registry.oracle.com)
	- Create an account and make note of user pass (david@gmail.com/PASS_GOES_HERE)
- k3d cluster create mycluster
	- k3d cluster create --agents 3 --volume /tmp/k3dvol:/tmp/k3dvol
	- test.yaml casued a bunch of issues, not sure why???
	- k3d cluster create --agents 3
	- k3d cluster create multiserver --servers 3     
		- Multiserver cluster make use of etcd
		- Single server nodes are not started with the --cluster-init flag and thus is not using the etcd backend
- kubectl apply -f [https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.yaml](https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.yaml)
	- Note: you must have internet connection
- kubectl apply -f [https://raw.githubusercontent.com/oracle/oracle-database-operator/main/oracle-database-operator.yaml](https://raw.githubusercontent.com/oracle/oracle-database-operator/main/oracle-database-operator.yaml)
	- You will get errors if you do not run the cert manager first
	- Only see issues if I created ther cluster with test.yaml
- kubectl create namespace oracle-namespace
- kubectl config set-context --current --namespace=oracle-namespace
	- Kubectl will now default to using the oracle–namespace
- Kubernetes Secrets to store Database and Oracle Container Registry (OCR) credentials
	- kubectl create secret generic admin-password \
	- --from-literal=sidb-admin-password='PASS_GOES_HERE' \
	- -n oracle-namespace
	- docker login container-registry.oracle.com
		- User/pass from container-registry.oracle.com from step#1
	- kubectl create secret generic regcred --from-file=.dockerconfigjson=$HOME/.docker/config.json  --type=kubernetes.io/dockerconfigjson -n oracle-namespace
		- Creates Kubernetes secret using OCR credentials
- If you forgot password
	- kubectl get secret/admin-password -n oracle-database-operator-system -o jsonpath='{.data}' -n oracle-namespace
	- echo 'PASS_GOES_HERE' | base64 --decode
		- Replace 'PASS_GOES_HERE' with the results from step 8a
- Touch singleinstancedatabase.yaml
	- Template = [https://github.com/oracle/oracle-database-operator/blob/main/config/samples/sidb/singleinstancedatabase.yaml](https://github.com/oracle/oracle-database-operator/blob/main/config/samples/sidb/singleinstancedatabase.yaml)	
		- name: sidb-oci
		- namespace: oracle-namespace
		- sid: XE (Express edition SID must only be XE)
		- secretName: admin-password
		- secretKey: sidb-admin-password
		- keepSecret: false
		- pullFrom: container-registry.oracle.com/database/express:21.3.0-xe
		- pullSecrets: regcred
		- xedition: express
		- pdbName: XEPDB1 (Express edition SID must only be XE)
		- flashBack: true
		- archiveLog: true
		- size: 20Gi
		- storageClass: "manual"
		- accessMode: "ReadWriteOnce"
		- volumeName: "task-pv-volume"
	- Add volume code below to the top of file

``` yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

	- Touch xe_singleinstancedatabase.yaml
		- Source = [https://github.com/oracle/oracle-database-operator/blob/main/config/samples/sidb/singleinstancedatabase_express.yaml](https://github.com/oracle/oracle-database-operator/blob/main/config/samples/sidb/singleinstancedatabase_express.yaml)
		- namespace: oracle-namspace
		- oracle_pwd: PASS_GOES_HERE
		- size: 10Gi
- kubectl apply -f xe_singleinstancedatabase.yaml -n oracle-namespace
- How to check status of DB?
	- List databases
		- kubectl get singleinstancedatabases -o name -n oracle-namespace
	- Database status
		- kubectl get singleinstancedatabase -n oracle-namespace 
			- Note: wait until it says healthy
	- Database health
		- kubectl get singleinstancedatabase sidb-oci -o "jsonpath={.status.status}" -n oracle-namespace
	- Database connection string
		- kubectl get singleinstancedatabase sidb-oci -o "jsonpath={.status.connectString}" -n oracle-namespace
	- Database enterprise manager url
		- kubectl get singleinstancedatabase sidb-oci -o "jsonpath={.status.oemExpressUrl}" -n oracle-namespace
	- SID name
		- kubectl get singleinstancedatabase sidb-oci -o "jsonpath={.status.sid}" -n oracle-namespace
	- Pluggable Database Name (PDB)
		- kubectl get singleinstancedatabase sidb-oci -o "jsonpath={.status.pdbName}" -n oracle-namespace
	- PDB Connection String
		- kubectl get singleinstancedatabase sidb-oci -o "jsonpath={.status.pdbConnectString}" -n oracle-namespace
	- Database details
		- kubectl get pods -n oracle-namespace -o wide
			- Note: the Oracle database host name is the pod name not the Kubernetes node.
	- Database storage details
		- kubectl get pvc -n oracle-namespace
- Connect to DB
	- kubectl exec -it pods/sidb-oci-7r5vz -n oracle-namespace -- sqlplus system/PASS_GOES_HERE@XEPDB1
	- kubectl exec -it pods/sidb-oci-o8qma -n oracle-namespace -- sqlplus system/PASS_GOES_HERE@SIDB1