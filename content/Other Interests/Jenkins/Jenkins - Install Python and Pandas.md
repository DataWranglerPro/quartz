# cicd.clab.yml
``` yaml
name: cicd_topo

topology:
  nodes:
    jenkins:
      kind: linux
      image: jenkins/jenkins
      ports:
        - 8080:8080
      binds:
        - /home/kali/data/jenkins_home:/var/jenkins_home   
```
# Start the lab
sudo containerlab deploy --topo cicd.clab.yml

# Shell into Jenkins docker image as root
If you do not shell into Jenkins as root you will be logged in as the Jenkins user. This user will not be able to sudo or use the apt-get commands.
``` sh
sudo docker exec -it --user root clab-cicd_topo-jenkins sh
```

# Install python and pandas
``` sh
apt-get update
apt-get install python3
apt-get install python3-pandas
```

# Get default admin password
``` sh
cat /var/jenkins_home/secrets/initialAdminPassword
```

# Go to http://localhost:8080 and log in

# Pipeline code
``` jenkinsfile
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                writeFile file: 'david.py', text: """
import pandas as pd
df = pd.DataFrame({'a': [3, 4, 5]})
print(df.head(1))
"""

            sh 'python3 david.py'
            }
        }
    }
}
```