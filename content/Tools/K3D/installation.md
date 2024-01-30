There are a few options to get a small and simple Kubernetes installation in your computer.

- Minikube - This is the official way to get a local version from the kubernetes team
- K3s - Is a lightweight version (<40mb)
	- [https://k3s.io/](https://k3s.io/)
- K3d - k3d is a lightweight wrapper to run k3s in docker
	- [https://k3d.io/](https://k3d.io/)
- Install in Alpine Linux
	- Apk add curl
	- Apk add bash
	- Apk add docker
	- wget -q -O - [https://raw.githubusercontent.com/rancher/k3d/main/install.sh](https://raw.githubusercontent.com/rancher/k3d/main/install.sh) | bash
- Install in Kali Linux
	- Apt install -y docker.io
	- Systemctl enable docker --now
	- Apt install kubernetes-client
	- Reboot now
	- wget -q -O - [https://raw.githubusercontent.com/rancher/k3d/main/install.sh](https://raw.githubusercontent.com/rancher/k3d/main/install.sh) | bash