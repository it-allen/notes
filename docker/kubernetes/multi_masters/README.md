<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [环境](#%E7%8E%AF%E5%A2%83)
- [允许root ssh](#%E5%85%81%E8%AE%B8root-ssh)
- [CA Certification](#ca-certification)
- [Install master node](#install-master-node)
    - [install etcd](#install-etcd)
      - [master 1](#master-1)
      - [master 2](#master-2)
    - [设置flannel](#%E8%AE%BE%E7%BD%AEflannel)
    - [安装kubernetes软件](#%E5%AE%89%E8%A3%85kubernetes%E8%BD%AF%E4%BB%B6)
      - [直接装软件](#%E7%9B%B4%E6%8E%A5%E8%A3%85%E8%BD%AF%E4%BB%B6)
      - [利用Docker运行Kubernetes](#%E5%88%A9%E7%94%A8docker%E8%BF%90%E8%A1%8Ckubernetes)
- [Install worker node](#install-worker-node)
    - [安装flannel(未成功)](#%E5%AE%89%E8%A3%85flannel%E6%9C%AA%E6%88%90%E5%8A%9F)
      - [node 1.1 (10.70.1.31)](#node-11-1070131)
    - [kubernetes](#kubernetes)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 环境
master 1: 10.70.1.28
    * node 1.1: 10.70.1.31
master 2: 10.70.1.29
    * node 2.1: 10.70.1.32

```sh
SERVICE_CLUSTER_IP_RANGE=10.70.1.0/16
Flannel_NET = 172.17.0.0/16

# 可能需要安装systemd
apt-get install systemd
```

# 允许root ssh
```sh
sudo su
# 设置密码
passwd
vim /etc/ssh/sshd_config
```
```diff
- PermitRootLogin without-password 
+ PermitRootLogin yes
```
```sh
/etc/init.d/ssh restart
```

# CA Certification
用于无密登录
* 中`master 1`上
```sh
mkdir -p /srv/kubernetes; cd /srv/kubernetes
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -subj "/CN=kube-system" -days 10000 -out ca.crt
```
这样在`~/srv_kubernetes`中将有 ca.crt/ca.key 两个文件

# Install master node
必需的软件
* etcd
* kube-apiserver
* kube-controller-manager
* kube-scheduler
可选的软件(如果 master 同时作为一个 worker node 的话)
* kubelet
* flannel
* docker

* 在`master 1`上
```sh
cat <<EOF | sudo tee server-openssl.cnf

[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
IP.1 = 127.0.0.1
IP.2 = 10.70.1.32
EOF


openssl genrsa -out server.key 2048
openssl req -new -key server.key -subj "/CN=10.70.1.32" -out server.csr -config server-openssl.cnf
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 10000 -extensions v3_req -extfile server-openssl.cnf
openssl x509 -noout -text -in server.crt


# copy to nodes and masters
scp -r /srv/kubernetes 10.70.1.29:/srv
scp -r /srv/kubernetes 10.70.1.31:/srv
scp -r /srv/kubernetes 10.70.1.32:/srv
```

### install etcd
#### master 1

```sh
export ETCD_VERSION=v3.0.7
cd /tmp
curl -L https://github.com/coreos/etcd/releases/download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz -o etcd-${ETCD_VERSION}-linux-amd64.tar.gz
tar xzvf etcd-${ETCD_VERSION}-linux-amd64.tar.gz && cd etcd-${ETCD_VERSION}-linux-amd64

mkdir -p /opt/etcd/bin
mkdir -p /opt/etcd/config/
cp etcd* /opt/etcd/bin/
mkdir -p /var/lib/etcd/

cat <<EOF | sudo tee /opt/etcd/config/etcd.conf
ETCD_DATA_DIR=/var/lib/etcd
ETCD_NAME=Master1
ETCD_LISTEN_PEER_URLS=http://0.0.0.0:2380
ETCD_LISTEN_CLIENT_URLS=http://0.0.0.0:2379
ETCD_INITIAL_CLUSTER_STATE=new
ETCD_INITIAL_CLUSTER=Master1=http://10.70.1.28:2380,Master2=http://10.70.1.29:2380
ETCD_INITIAL_ADVERTISE_PEER_URLS=http://10.70.1.28:2380
ETCD_ADVERTISE_CLIENT_URLS=http://10.70.1.28:2379
ETCD_HEARTBEAT_INTERVAL=6000
ETCD_ELECTION_TIMEOUT=30000
ETCD_INITIAL_CLUSTER_TOKEN=etcd
GOMAXPROCS=$(nproc)
EOF

cat <<EOF | sudo tee /etc/systemd/system/etcd.service
[Unit]
Description=Etcd Server
Documentation=https://github.com/coreos/etcd
After=network.target
[Service]
User=root
Type=simple
EnvironmentFile=-/opt/etcd/config/etcd.conf
ExecStart=/opt/etcd/bin/etcd
Restart=on-failure
RestartSec=10s
LimitNOFILE=40000
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload && systemctl enable etcd && systemctl start etcd
```
#### master 2

```sh
cd /tmp
curl -L https://github.com/coreos/etcd/releases/download/v3.0.7/etcd-v3.0.7-linux-amd64.tar.gz -o etcd-v3.0.7-linux-amd64.tar.gz
tar xzvf etcd-v3.0.7-linux-amd64.tar.gz && cd etcd-v3.0.7-linux-amd64

mkdir -p /opt/etcd/bin
mkdir -p /opt/etcd/config/
cp etcd* /opt/etcd/bin/
mkdir -p /var/lib/etcd/

cat <<EOF | sudo tee /opt/etcd/config/etcd.conf
ETCD_DATA_DIR=/var/lib/etcd
ETCD_NAME=Master2
ETCD_LISTEN_PEER_URLS=http://0.0.0.0:2380
ETCD_LISTEN_CLIENT_URLS=http://0.0.0.0:2379
ETCD_INITIAL_CLUSTER_STATE=new
ETCD_INITIAL_CLUSTER=Master1=http://10.70.1.28:2380,Master2=http://10.70.1.29:2380
ETCD_INITIAL_ADVERTISE_PEER_URLS=http://10.70.1.29:2380
ETCD_ADVERTISE_CLIENT_URLS=http://10.70.1.29:2379
ETCD_HEARTBEAT_INTERVAL=6000
ETCD_ELECTION_TIMEOUT=30000
ETCD_INITIAL_CLUSTER_TOKEN=etcd
GOMAXPROCS=$(nproc)
EOF

cat <<EOF | sudo tee /etc/systemd/system/etcd.service
[Unit]
Description=Etcd Server
Documentation=https://github.com/coreos/etcd
After=network.target
[Service]
User=root
Type=simple
EnvironmentFile=-/opt/etcd/config/etcd.conf
ExecStart=/opt/etcd/bin/etcd
Restart=on-failure
RestartSec=10s
LimitNOFILE=40000
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload && systemctl enable etcd && systemctl start etcd
```

### 设置flannel
```sh
/opt/etcd/bin/etcdctl set /coreos.com/network/config '{"Network":"10.70.1.0/24", "Backend": {"Type": "vxlan"}}'
```

### 安装kubernetes软件
#### 直接装软件
```sh
cd /tmp
curl -L 'https://github.com/kubernetes/kubernetes/releases/download/v1.6.6/kubernetes.tar.gz' -O kubernetes.tar.gz
tar xvf kubernetes.tar.gz && cd kubernetes
tar xf ./server/kubernetes-server-linux-amd64.tar.gz -C /opt/
```


#### 利用Docker运行Kubernetes
docker-compose.yml
```yaml
version: '2'
services:
    apiserver:
        image: quay.io/coreos/hyperkube:v1.6.6_coreos.1
        container_name: apiserver
        network_mode: host
        command:
            - /hyperkube
            - apiserver
            - --service-cluster-ip-range=10.70.1.28/24
            - --address=0.0.0.0
            - --etcd_servers=http://10.70.1.28:4001,http://10.70.1.29:4001
            - --v=2
    controller:
        image: quay.io/coreos/hyperkube:v1.6.6_coreos.1
        network_mode: host
        command:
            - /hyperkube
            - controller-manager
            - --master=127.0.0.1:8080
            - --v=2
    scheduler:
        image: quay.io/coreos/hyperkube:v1.6.6_coreos.1
        container_name: scheduler
        network_mode: host
        command:
            - /hyperkube
            - scheduler
            - --master=127.0.0.1:8080
            - --v=2
```
```sh

```


# Install worker node
必需的软件
* kubelet
* kube-proxy
* flannel
* docker

### 安装flannel(未成功)
#### node 1.1 (10.70.1.31)
```sh
cd /tmp
curl -L https://github.com/coreos/flannel/releases/download/v0.6.1/flannel-v0.6.1-linux-amd64.tar.gz -o flannel.tar.gz
mkdir -p /opt/flannel
tar xzf flannel.tar.gz -C /opt/flannel
# flannel config
cat << EOF | sudo tee /etc/systemd/system/flanneld.service
[Unit]
Description=Flanneld
Documentation=https://github.com/coreos/flannel
After=network.target
Before=docker.service
[Service]
User=root
ExecStart=/opt/flannel/flanneld \
--etcd-endpoints="http://10.70.1.28:2379,http://10.70.1.29:2379" \
--iface= 10.70.1.31 \
--ip-masq
ExecStartPost=/bin/bash /opt/flannel/update_docker.sh
Restart=on-failure
Type=notify
LimitNOFILE=65536
[Install]
WantedBy=multi-user.target
EOF

# add update_docker.sh
cat <<EOF | sudo tee /opt/flannel/update_docker.sh

source /run/flannel/subnet.env
sed -i "s|ExecStart=.*|ExecStart=\/usr\/bin\/dockerd -H tcp:\/\/127.0.0.1:4243 -H unix:\/\/\/var\/run\/docker.sock --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU}|g" /lib/systemd/system/docker.service
rc=0

ip link show docker0 >/dev/null 2>&1 || rc="$?"
if [[ "$rc" -eq "0" ]]; then
ip link set dev docker0 down
ip link delete docker0
fi

systemctl daemon-reload
EOF

systemctl daemon-reload && systemctl enable flanneld && systemctl start flanneld
```

### kubernetes
* node.1
```yaml
version: "2"
services:
    kubelet:
        image: quay.io/coreos/hyperkube:v1.6.6_coreos.1
        container_name: kubelet
        network_mode: host
        pid: host
        # privileged 用于给容器权限，不然 会报这个错
        # skipping pod synchronization - [Failed to start ContainerManager [open /proc/sys/vm/overcommit_memory: read-only file system, open /proc/sys/kernel/panic: read-only file system, open /proc/sys/kernel/panic_on_oops: read-only file system]]
        privileged: true
        volumes:
            - /var/lib/docker/:/var/lib/docker:rw
            - /:/rootfs:rw
            - /sys:/sys:rw
            - /var/run:/var/run
            - /var/lib/kubelet:/var/lib/kubelet
        command:
            - /hyperkube
            - kubelet
            - --hostname-override=10.70.1.32
            - --api-servers=http://10.70.1.28:8080,http://10.70.1.29:8080
            - --address=0.0.0.0
            - --enable_server
            - --logtostderr=true
            - --v=2
#            - --containerized=true
    proxy:
        image: quay.io/coreos/hyperkube:v1.6.6_coreos.1
        container_name: proxy
        network_mode: host
        privileged: true
        command:
            - /hyperkube
            - proxy
            - --master=http://10.70.1.28:8080,http://10.70.1.29:8080 --v=2
            - --hostname-override=10.70.1.32
```
* node.2
```yaml
version: "2"
services:
    kubelet:
        image: quay.io/coreos/hyperkube:v1.6.6_coreos.1
        container_name: kubelet
        network_mode: host
        pid: host
        # privileged 用于给容器权限，不然 会报这个错
        # skipping pod synchronization - [Failed to start ContainerManager [open /proc/sys/vm/overcommit_memory: read-only file system, open /proc/sys/kernel/panic: read-only file system, open /proc/sys/kernel/panic_on_oops: read-only file system]]
        privileged: true
        volumes:
            - /var/lib/docker/:/var/lib/docker:rw
            - /:/rootfs:rw
            - /sys:/sys:rw
            - /var/run:/var/run
            - /var/lib/kubelet:/var/lib/kubelet
        command:
            - /hyperkube
            - kubelet
            - --hostname-override=10.70.1.32
            - --api-servers=http://10.70.1.28:8080,http://10.70.1.29:8080
            - --address=0.0.0.0
            - --enable_server
            - --logtostderr=true
            - --v=2
#            - --containerized=true
    proxy:
        image: quay.io/coreos/hyperkube:v1.6.6_coreos.1
        container_name: proxy
        network_mode: host
        privileged: true
        command:
            - /hyperkube
            - proxy
            - --master=http://10.70.1.28:8080,http://10.70.1.29:8080 --v=2
            - --hostname-override=10.70.1.32
```
