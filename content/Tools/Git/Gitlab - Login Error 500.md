![[Pasted image 20240915161405.png|500]]

# log into Gitlab docker container
``` sh
sudo docker exec -it clab-cicd_topo-gitlab sh
```


# Restart the service
``` sh
gitlab-ctl restart
ok: run: alertmanager: (pid 2567) 1s
ok: run: gitaly: (pid 2583) 0s
ok: run: gitlab-exporter: (pid 2612) 0s
ok: run: gitlab-kas: (pid 2624) 0s
ok: run: gitlab-workhorse: (pid 2642) 1s
ok: run: logrotate: (pid 2658) 0s
ok: run: nginx: (pid 2664) 1s
ok: run: postgres-exporter: (pid 2680) 0s
ok: run: postgresql: (pid 2689) 1s
ok: run: prometheus: (pid 2698) 0s
ok: run: puma: (pid 2738) 0s
ok: run: redis: (pid 2743) 1s
ok: run: redis-exporter: (pid 2750) 0s
ok: run: sidekiq: (pid 2767) 0s
ok: run: sshd: (pid 2773) 1s
```

# Check logs
``` sh
cat /var/log/gitlab/gitaly/current
```

