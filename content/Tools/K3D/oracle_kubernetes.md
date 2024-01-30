[https://github.com/javiermugueta/k8s-orcldb](https://github.com/javiermugueta/k8s-orcldb)

[https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)

- [https://container-registry.oracle.com](https://container-registry.oracle.com)
	- Create an account and make note of user pass (david@gmail.com/PASS_GOES_HERE)
- k3d cluster create mycluster
	- This will create 1 docker process (slave and master will be on the same kubernetes node)
- Kubernetes Secrets to store Database and Oracle Container Registry (OCR) credentials
	- docker login container-registry.oracle.com
		- User/pass from container-registry.oracle.com from step#1
	- kubectl create secret generic regcred --from-file=.dockerconfigjson=$HOME/.docker/config.json  --type=kubernetes.io/dockerconfigjson
		- Creates Kubernetes secret using OCR credentials
- Run the commands below
	- kubectl get nodes
	- docker exec -it <ENTER_NODE_NAME_HERE> sh
		- This will shell you into the node
	- Make an oracle folder under /tmp/oracle (this needs to be done on all master/slave nodes)
		- Make an oradata folder (mkdir oradata)
		- Make a scripts folder (mkdir scripts)
			- Make a startup folder (mkdir startup)
				- This is where you can add all SQL files that will be run at startup
			- Make a setup folder (mkdir setup)
	- chmod 777 all folders created under /tmp
- kubectl apply -f orcldb3.yaml
- kubectl get pods
	- kubectl describe pod <ENTER_POD_NUMBER_HERE>  (to get details)
	- Kubectl logs <ENTER_POD_NUMBER_HERE> --follow (to see the database be created)
- kubectl exec -it <ENTER_POD_NUMBER_HERE> sqlplus / as sysdba 
- kubectl exec -it pods/orcldb-5549d599b-qtsxr -- sqlplus pdbadmin/PASS_GOES_HERE@ORCLPDB1

# SSH into node

``` sh
kubectl get nodes
docker exec -it k3d-demo-server-0 sh
```

# Create oracle folders

``` sh
cd tmp
ls
mkdir oracle
cd oracle/
mkdir oradata
mkdir scripts
cd scripts/
mkdir startup
mkdir setup
cd startup/
touch 01_tbl.sql
vi 01_tbl.sql (ESC :w ENTER | ESC :x ENTER)
chmod 777 oracle/
cd oracle/
chmod oradata/
chmod 777 oradata/
chmod 777 scripts/
```

# To log into Enterprise Manager

[https://172.27.0.2:5500/em/login](https://172.27.0.2:5500/em/login)

- User - sys
- Pass - YOUR_PASS_GOES_HERE
- Container name - leave this blank