
环境:
master: 10.70.1.28
slave.1: 10.70.1.29
slave.2: 10.70.1.31
Ubuntu 16.04

```sh
ETCD_VERSION=${ETCD_VERSION:-"2.3.1"}
ETCD="etcd-v${ETCD_VERSION}-linux-amd64"
curl -L https://github.com/coreos/etcd/releases/download/v${ETCD_VERSION}/${ETCD}.tar.gz -o etcd.tar.gz

tar xzf etcd.tar.gz -C /tmp
cd /tmp/etcd-v${ETCD_VERSION}-linux-amd64

for h in localhost slave.1 slave.2; do ssh kk@$h mkdir -p '$HOME/kube' && scp -r etcd* kk@$h:~/kube; done
for h in localhost slave.1 slave.2; do ssh kk@$h 'sudo mkdir -p /opt/bin && sudo mv $HOME/kube/* /opt/bin && rm -rf $home/kube/*'; done
```
