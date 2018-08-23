<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [前置条件](#%E5%89%8D%E7%BD%AE%E6%9D%A1%E4%BB%B6)
- [](#)
    - [下载最新版kubernetes](#%E4%B8%8B%E8%BD%BD%E6%9C%80%E6%96%B0%E7%89%88kubernetes)
- [etcd 安装](#etcd-%E5%AE%89%E8%A3%85)
    - [etcd master](#etcd-master)
    - [etcd slave 1](#etcd-slave-1)
    - [etcd slave 2](#etcd-slave-2)
- [flannel](#flannel)
    - [在 etcd 中设置flannel](#%E5%9C%A8-etcd-%E4%B8%AD%E8%AE%BE%E7%BD%AEflannel)
    - [启动flannel](#%E5%90%AF%E5%8A%A8flannel)
- [kubernetes](#kubernetes)
    - [master](#master)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 前置条件
* docker/docker-compose

## 
#### 下载最新版kubernetes
在[此页面](https://github.com/kubernetes/kubernetes/releases)中查找最新版
```sh
wget https://storage.googleapis.com/kubernetes-release/release/v1.6.6/kubernetes.tar.gz
tar xf kubernetes.tar.gz
cd kubernetes
```

当前环境为 ubuntu, 所以进入下列目录
```sh
cd cluster/ubuntu
```

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
docker run --rm --name=flannel -v /run:/run -v /var:/var -v /dev/net:/dev/net -it --privileged --net=host -d quay.io/coreos/flannel:v0.7.1
```
* /run:/run 用于将 /run/flannel/subnet.env 映射出来
* /var:/var 用于将 /var/run/flannel/subnet.env 映射出来
* /dev/net:/dev/net 用于映射 /dev/net/tun

## kubernetes

#### master
```sh
sudo docker run --net=host -d -v /var/run/docker.sock:/var/run/docker.sock \
    gcr.io/google_containers/hyperkube@sha256:039dc96edbb7fec89199674f9605f3969cdfea043e6d3518eb5873916d90a101 \
    /hyperkube kubelet --api_servers=http://localhost:8080 --v=2 \
    --address=0.0.0.0 --enable_server --hostname_override=127.0.0.1 \
    --kubeconfig=/etc/kubernetes/manifests-multi
```
```sh

```
