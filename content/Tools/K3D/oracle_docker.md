[https://ronekins.com/2020/10/10/oracle-19c-on-docker-and-kubernetes-part-2-running-oracle-on-docker/](https://ronekins.com/2020/10/10/oracle-19c-on-docker-and-kubernetes-part-2-running-oracle-on-docker/)

[https://www.youtube.com/watch?v=5-DC5QOrU-c](https://www.youtube.com/watch?v=5-DC5QOrU-c)

- [https://container-registry.oracle.com](https://container-registry.oracle.com)
	- Create an account and make note of user pass (david@gmail.com/PASS_GOES_HERE)
	- This is where we are going to get the Oracle DB images
- docker login container-registry.oracle.com
	- User/pass from container-registry.oracle.com from step#1
	- WARNING! Your password will be stored unencrypted in /root/.docker/config.json
- docker pull container-registry.oracle.com/database/enterprise:latest
	- This might take 5-10 minutes
- docker images
	- Make sure you see the database image
- Run the commands below
	- Make an oracle folder under /home/YOUR_USER_NAME/
		- Make an oradata folder
		- Make a scripts folder
			- Make a startup folder
			- Make a setup folder
	- chmod 777 all folders created under /home/kali/
	- Oracle recommends that the password entered should be at least 8 characters in length, contain at least 1 uppercase character, 1 lower case character and 1 digit (0-9). Oracle will reject your password if it does not meet the minimum criteria

==NOTE: before running the command below, make sure to remove the oradata folder and recreate with chmod 777. If not you will have issues starting the image. To remove use rm -rf oradata==

``` sh
docker run -d --name mydb \
-p 1521:1521 -p 5500:5500 \
-e ORACLE_SID=PSTGCDB \
-e ORACLE_PDB=PSTGPDB1 \
-e ORACLE_PWD=PASS_GOES_HERE \
-v /home/kali/oracle/oradata:/opt/oracle/oradata \
-v /home/kali/oracle/scripts/startup:/opt/oracle/scripts/startup \
-v /home/kali/oracle/scripts/setup:/opt/oracle/scripts/setup \
container-registry.oracle.com/database/enterprise:latest
```
- docker logs mydb --follow
	- You can see if the database is being created without any issues
- Connecting to database
	- docker exec -it mydb sqlplus / as sysdba
	- docker exec -it mydb sql / as sysdba    >> for sqlcl
- Stopping/removing the database and any docker objects
	- docker stop $(docker ps -a -q)
	- docker rm $(docker ps -a -q)

To connect via port 1521, update sqlnet.ora file
- docker exec -t ol7_19_con bash -ic 'echo DISABLE_OOB=ON > $ORACLE_HOME/network/admin/sqlnet.ora'

# Sqlcl

- Download
	- [https://edelivery.oracle.com/ocom/faces/Downloads?auth=false&auth_token=1667927552_ZjVmZGE2YmJmZWM3M2Q5ZjYwODE0ODE2NzFmYmM0ZjNhOTY2MjFjMjBlNzc0N2ExMWI2YjVjNzM3ZTVkMmU4Mjo6b3NkY19vcmFjbGUuY29t&dlp_cid=1098513&rel_cid=1094630](https://edelivery.oracle.com/ocom/faces/Downloads?auth=false&auth_token=1667927552_ZjVmZGE2YmJmZWM3M2Q5ZjYwODE0ODE2NzFmYmM0ZjNhOTY2MjFjMjBlNzc0N2ExMWI2YjVjNzM3ZTVkMmU4Mjo6b3NkY19vcmFjbGUuY29t&dlp_cid=1098513&rel_cid=1094630)
	- Get zip file, move to Windows, unzip
	- Move to Kali desktop and move to folder
- To run in Linux
	- Cd /home/…/oracle/tools/sqlcl/bin
	- Chmod 777 sql
	- ./sql
- Move sql files from host to docker image
	- Docker ps
		- Container id = 7c40792a997f
	- docker cp /home/kali/oracle/tools/sqlcl/breaktest.sql 7c40792a997f:/breaktest.sql