## 前置条件
* docker/docker-compose
* 


## etcd 安装
参考:
    - [etcd 使用入门](http://cizixs.com/2016/08/02/intro-to-etcd)
两个结点:
- master: 10.70.1.28
- slave1: 10.70.1.29
- slave2: 10.70.1.31

利用 etcd.io 提供的发现服务，生成一个token
https://discovery.etcd.io/new?size=3 ==> https://discovery.etcd.io/d2757d7cdcca38a43a34e9288671475e

#### etcd master
```yaml
version: "2"
services:
    etcd:
        image: elcolio/etcd
        container_name: etcd_master
        volumes:
        -   /usr/share/ca-certificates/:/etc/ssl/certs:ro
        network_mode: host
        command:
        -   --name=etcd0
        -   --discovery=https://discovery.etcd.io/947ede23437a275be1521fe46764c9e1
        -   --advertise-client-urls=http://10.70.1.28:2379,http://10.70.1.28:4001
        -   --listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001
        -   --initial-advertise-peer-urls=http://10.70.1.28:2380
        -   --listen-peer-urls=http://0.0.0.0:2380
        -   --initial-cluster-token=etcd-cluster-1
        #-   --initial-cluster=etcd0=http://10.70.1.28:2380,etcd1=http://10.70.1.29:2380
        -   --initial-cluster-state=new
```

#### etcd slave 1
```yaml
version: "2"
services:
    etcd:
        image: elcolio/etcd
        container_name: etcd_slave_1
        volumes:
        -   /usr/share/ca-certificates/:/etc/ssl/certs:ro
        network_mode: host
        command:
        -   --name=etcd1
        -   --advertise-client-urls=http://10.70.1.29:2379,http://10.70.1.29:4001
        -   --listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001
        -   --initial-advertise-peer-urls=http://10.70.1.29:2380
        -   --listen-peer-urls=http://0.0.0.0:2380
        -   --initial-cluster-token=etcd-cluster-1
        -   --initial-cluster=etcd0=http://10.70.1.28:2380,etcd1=http://10.70.1.29:2380
        -   --initial-cluster-state=new
```
#### etcd slave 2
```yaml
version: "2"
services:
    etcd:
        image: elcolio/etcd
        container_name: etcd_slave
        volumes:
        -   /usr/share/ca-certificates/:/etc/ssl/certs:ro
        network_mode: host
        command:
        -   --name=etcd1
        -   --advertise-client-urls=http://10.70.1.29:2379,http://10.70.1.29:4001
        -   --listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001
        -   --initial-advertise-peer-urls=http://10.70.1.29:2380
        -   --listen-peer-urls=http://0.0.0.0:2380
        -   --initial-cluster-token=etcd-cluster-1
        -   --initial-cluster=etcd0=http://10.70.1.28:2380,etcd1=http://10.70.1.29:2380
        -   --initial-cluster-state=new
```


## flannel
用于统一管理集群网络分配
#### 在 etcd 中设置flannel
```sh
docker exec -it etcd_master etcdctl set /coreos.com/network/config '{"Network":"10.1.0.0/16"}'
```

#### 启动flannel
```sh
docker run --rm --name=flannel -v /run:/run -v /var:/var quay.io/coreos/flannel:v0.7.1
```
* /run:/run 用于将 /run/flannel/subnet.env 映射出来
* /var:/var 用于将 /var/run/flannel/subnet.env 映射出来

## kubernetes

