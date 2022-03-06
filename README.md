# hit_record

The steps to DevOps challenge:
1. Create APP and containerize it and push that to public docker hub.
2. Launch Jenkins through Docker Compose
3. Create 3 LXC Container for k3s
4. Create k3s Cluster on those
5. Deploy the hit_record APP with k3s


# 1. Build and Push Image
```bash
$ docker build -f Dockerfile -t <DOCKERHUB_USER>/hit_record:latest .
```

```bash
$ docker push <DOCKERHUB_USER>/hit_record:latest
```

# 2. JenkinsServer
Need docker-compose.

```bash
$ cd JenkinsServer
$ docker-compose up -d
```

This will start the Jenkins Server.

# 3. Create 3 lxc container

```bash
$ sudo apt install lxd zfsutils-linux
```

Configure LXD

```bash
$ lxd init
```

```bash
$ lxc launch ubuntu:20.04 k1
$ lxc launch ubuntu:20.04 k2
$ lxc launch ubuntu:20.04 k3
```

# 4. Create k3s Cluster

```bash
$ git clone git@github.com:k3s-io/k3s-ansible.git;cd k3s-ansible;
```

First create a new directory based on the sample directory within the inventory directory:

```bash
cp -R inventory/sample inventory/k3s-cluster-inventory
```

Second, edit inventory/k3s-cluster-inventory/hosts.ini to match the system information gathered above. For example:

```ini
[master]
192.168.168.100

[node]
192.168.168.[101:102]

[k3s_cluster:children]
master
node
```

group_vars
```yaml
---
k3s_version: v1.23.4+k3s1
ansible_user: root
systemd_dir: /etc/systemd/system
master_ip: "{{ hostvars[groups['master'][0]]['ansible_host'] | default(groups['master'][0]) }}"
extra_server_args: ""
extra_agent_args: ""
```

Also, to use the hosts created by LXC, needed to set ssh key to those and enable ssh properly.

Let's create:
```bash
ansible-playbook site.yml -i inventory/k3s-cluster-inventory/hosts.ini
```

It will create the cluster.

# 5. Deploy the hit_record APP with k3s

Need ingress

```
helm install hitrecord-ingress nginx-stable/nginx-ingress
```


```bash
$ cd deployment
$ kubectl apply -f .
```

This will deploy the application.


```bash
# kubectl apply -f .
deployment.apps/hit-record-api-v1-deployment created
service/hit-record-api-v1-service created
deployment.apps/hit-record-api-v2-deployment created
service/hit-record-api-v2-service created
configmap/hit-record-configmap created
ingress.networking.k8s.io/hitrecord-ingress created
deployment.apps/redis-deployment created
service/redis-service created
```

Need helm to install linkerd and inject linkerd

```commandline
$ curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
```

```bash
$ cat hit_record_api_v1_deployment.yaml| linkerd inject - | kubectl apply -f -
$ cat hit_record_api_v2_deployment.yaml| linkerd inject - | kubectl apply -f -
```

Visualize

```bash
$ linkerd viz install | kubectl apply -f -
$ linkerd viz dashboard
```

```bash
% kubectl get pods                        
NAME                                                READY   STATUS    RESTARTS      AGE
hit-record-api-v1-deployment-68b97bb87-wlth2        1/1     Running   0             3m22s
hit-record-api-v2-deployment-767d67bb4d-cwckk       1/1     Running   0             3m21s
hit-record-release-nginx-ingress-64f777454d-6ctj2   1/1     Running   2 (10h ago)   18h
redis-deployment-756b4b8956-hbqmk                   1/1     Running   0             3m21s
```