Tool for creating and configuring pods in Kubernetes

Types of files:
- Deployment
- Service
- Secret

![[nginx-deployment.yaml]]

![[nginx-service.yaml]]

# Every configuration file has three parts

- Metadata
	- This contains name of the application
- Specification
	- The kind key will tell Kubernetes what kind of configuration you want to create
		- Like deployment, service
		- Make sure the apiVersion matches the deployment type
- Status
	- This is automatically generated for us by Kubernetes
- Note: You can combine multiple configs into one file
	- Separate by ---

## Explanation of the basic pieces

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx >> under the selector label, make sure it matches the name under the spec
  template: >> this section applies to the pod
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 8080 >> This setting does not make any changes! It is just here for informational purposes. Use it to make note of the Port(s) available to the user.
```

------------------------------------------------------------------

``` yaml
apiVersion: v1  
kind: Service  
metadata:  
  name: nginx-service  
spec:  
  selector:  
    app: nginx >> under the selector label, make sure it matches the name under the Deployment spec  
  ports:  
    - protocol: TCP  
      port: 8080 >> You can access the port internally using this port number. In other words all traffic on port 8080 will be forwarded to port 80  
      targetPort: 80 >> This is the actual port that will be used to access the container. Note that containers already have a default port they work on, use that one. Also make sure this matches the containerPort in Deployment
```
--------------------------------------------------------------------------------------------------------------

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  type: NodePort 
  ports:
    - name: http
      protocol: TCP
      port: 80 >> this can be any available port that is available internally
      targetPort: 80 >> traffic from "port" is directed to "targetPort"
      nodePort: 30000 >> port for external ip (range = [30000 - 32767])
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - name: http
      nodePort: 30475
      port: 8089
      protocol: TCP
      targetPort: 8080
    - name: metrics
      nodePort: 31261
      port: 5555
      protocol: TCP
      targetPort: 5555
    - name: health
      nodePort: 30013
      port: 8443
      protocol: TCP
      targetPort: 8085
```
if you hit the my-service:8089 the traffic is routed to 8080 of the container(targetPort). Similarly, if you hit my-service:8443 then it is redirected to 8085 of the container(targetPort). But this myservice:8089 is internal to the kubernetes cluster and can be used when one application wants to communicate with another application. So to hit the service from outside the cluster someone needs to expose the port on the host machine on which kubernetes is running so that the traffic is redirected to a port of the container. This is node port(port exposed on the host machine). From the above example, you can hit the service from outside the cluster(Postman or any rest-client) by host_ip:nodePort

Say your host machine ip is 10.10.20.20 you can hit the http, metrics, health services by 10.10.20.20:30475, 10.10.20.20:31261, 10.10.20.20:30013.