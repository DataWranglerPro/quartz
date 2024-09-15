How I was able to install Gitlab in 7 minutes!

# gitlab.clab.yml

``` yml
name: gitlab_topo

topology:
  nodes:
    gitlab:
      kind: linux
      image: gitlab/gitlab-ce
      ports:
        - 8081:80
      binds:
        - /home/kali/data/gitlab_data:/var/opt/gitlab    
```

# Start lab
``` sh
sudo containerlab deploy --topo gitlab.clab.yml
```

# Go to http://127.0.0.1:8081    
**Note:** it may take Gitlab a few minutes to start up :)

# Shell into gitlab docker image
``` sh
sudo docker exec -it clab-gitlab_topo-gitlab sh
```

# Get default admin password
``` sh
cat /etc/gitlab/initial_root_password
```

**Warning:** after the initial login, the initial_root_password file will be deleted!

# To reset your password
``` sh
gitlab-rake "gitlab:password:reset[root]" force=true
```
