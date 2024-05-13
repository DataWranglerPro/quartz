Information on this Jenkins job type. Freestyle jobs are basic compared to pipeline jobs.

- On your dashboard, click on **New Item**
![[Pasted image 20240513110348.png|200]]
- I have a very barebones Jenkins install, so all I see if a standard Freestyle project.
	- Add a name
	- Click on Freestyle project 
	- Click OK
![[Pasted image 20240513110557.png|600]]

- Go down to **Build Steps** and select **Execute shell**
![[Pasted image 20240513110916.png]]

You should now see a textbox that allows you to write shell code.
![[Pasted image 20240513111019.png]]

- Lets print some basic information using this Freestyle project.
	- For a list of available environment variables
		- http://localhost:8080/env-vars.html/
``` sh
ls
ls -ltra /var/jenkins_home/workspace
echo "${NODE_NAME}"
echo "${NODE_LABELS}"
echo "${WORKSPACE}"
```

- Select the Save button as shown below.
![[Pasted image 20240513111510.png]]

- Click the **Build Now** button to run your job
![[Pasted image 20240513111612.png]]

- Under **Build History**, select your job.
![[Pasted image 20240513111715.png]]

- Click on Console Output to see log file.
![[Pasted image 20240513112057.png]]


