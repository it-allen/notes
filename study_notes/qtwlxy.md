# "极客时间" 刘超《趣谈网络协议》
## 第一讲 为什么要学习网络协议
#### 协议三要素
* 语法
* 语义
* 顺序

## 第二讲 网络分层的真实含义是什么？
#### 为什么要分层？
复杂的程序都要分层，这是程序设计的要求

*只要是在网络上跑的包，都是完整的，可以有下层没上层，但不能有上层没有下层*

二层设备: 解析 mac 头
三层设备：解析 IP 头

## 第三讲 ifconfig
windows: ipconfig
linux: ifconfig(net-tools)、 ip addr(iproute2)

*IP地址是一个网卡在网络世界的通讯地址，相当于门牌号; MAC像身份证，是一个唯一的标识，没有定位功能*
### ip 分类
![ip分类图](./images/ip_class.jpeg)
A、B、C类地址分两部分: 前一部分为网络号，后一部分为主机号
![ABC类地址说明](./images/abc.jpeg)

*问题*: C类地址主机数量太少，而B类太多
解决方案: CIDR
### CIDR(无类型域间选路)
将IP地址一分为二，前面是网络号，后面是主机号
例: 10.100.122.2/24, 表示前24位为网络号，后8位为主机号。广播地址为10.100.122.255，子网掩码为255.255.255.0。将IP与子网掩码进行与操作即可得到网络号

### ip addr
输出解析
* UP: 网卡处于启动状态
* BROADCAST: 有广播地址，可以发送广播包
* MULTICAST: 可发送多播
* LOWER_UP: L1 是启动的，即插了网线
* qdisc: queue discipline, 排队规则。有以下几种, pfifo(先进先出), pfifo_fast(队列中包含三个波段band, band 内部先进先出. band 0 最高，band 2 最低, 实际上就是个优先队列)，IP头中的TOS(Type of service)字段可以决定放在哪个队列中

## 第四讲 DHCP与PXE
配置 ip
```sh
ifconfig eth1 10.0.0.1/24
ifconfig eth1 up
# 或
ip addr add 10.0.0.1/24 dev eth1
ip link set up eth1
```
Linux 的默认逻辑：如果是跨网段的，则发送到网关，而不是直接将包发送到网络

### DHCP(动态主机配置协议) 工作方式 
* 新机器(A)发起 DHCP discover
* DHCP server 提供 DHCP Offer
* A选择一个Offer(通常是第一个到达的Offer), 并且发一个广播数据包(DHCP Request)告知所有 DHCP Server 选择了XX, 这样它们可以回收IP
* 被选择的DHCP Server 接到 Request 后返回一个 ACK
**DHCP Request也能用于续租，通常是在租期过去50%的时候**

### PXE(预启动执行环境) 过程
* BIOS启动，并调用 PXE Client(正常启动的话是读取MBR扇区，启动GRUB, GRUB会加载内核和根文件系统的initramfs，这时将权力交给内核)
* PXE Client 发送DHCP 请求
* DHCP Server 分配一个IP, 并在返回IP时告知 PXE Server的地址(next-server)以及文件名字
* PXE Client 用TFTP协议下载镜像，然后执行安装,系统就好了
![PXE工作流程](./images/pxe_flow.jpeg)

## 第五讲 从物理层到MAC层
* hub: 没有路由功能，所有都是广播
* switch(交换机): 会对包来源进行记忆(转换表)，这样后面有去此源的包就直接发送到该口，避免了广播
### 数据链路层，也即MAC层需要解决的问题
问题：
1. 包的来源和目的
2. 谁先发？谁后发？同时发混乱？
3. 出错怎么办？

方案(多路访问):
1. 信道划分: 各走各的
2. 轮流协议：限号
3. 随机接入协议：堵车就加来，错峰出行。以太网用的就是这个方式
![mac header](./images/mac_header.jpeg)
*其中类型表示数据内容，CRC(循环冗余检测)用于校验，解决传输出错的问题*

### POINTS
* MAC层用多路访问来解决堵车问题
* ARP通过广播(吼)的方式来寻找MAC,并会缓存一段时间 
* 交换机有MAC学习功能，学习完后就知道目的，不需要再广播

## 第六讲 交换机与VLAN
* 交换机可能导致环路问题, 解决方案如下
	- STP(Spanning Tree Protocol)， 生成树, 原理类似于比武争夺武林盟主
		* Root Bridge, 根交换机，"掌门"
		* Designated Bridges, 指定交换机, "小弟"
		* Bridge Protocol Data Units(BPDU), 网桥协议数据单元，互相比较实力的协议, 只有"掌门"能发
		* Priority Vector, 优先级向量。一组ID列表，[Root Bridge ID, Root Path Cost, Bridge ID, Port ID]， 实际上就是逐个比较
	- STP 工作过程
		* 开始所有机器都发BPDU(ID由管理员按性能指定，所以有部分机器容易成为"掌门")
		* "比输"的机器自动变为“小弟”，转发BPDU, 这样就形成了很多小门派
		* 接着合并
			- 掌门遇到掌门: 比输的带所有小弟归顺
			- 同门相遇: 掌门遇到不认识的小弟，可能影响优先级; 都是同门小弟相遇，其中之一可能成为上司
			- 掌门与其他帮派小弟相遇: 掌门赢小弟，则小弟归顺，并带连接的兄弟归顺；反之与上同
			- 不同门小弟相遇：输的归顺，并带连接的兄弟归顺
			- 不断重复，最终只有一个盟主胜出

### VLAN 解决广播和安全问题
网络隔离的方式
* 物理隔离: 投入高，不灵活
* 虚拟隔离(VLAN):
![vlan header](./images/vlan_header.jpeg)
*实际上是mac头部增加Vlan ID用于决定从哪个口去转发*
![vlan sample](./images/vlan_top.jpeg)
* VLAN间用 trunk口进行转发, 不受VLAN ID限制

## 第七讲 ICMP与ping
ping 基于ICMP(Internet Control Message Protocol, 互联网控制报文协议)协议，
![ICMP](./images/icmp.jpeg)
### ICMP类型
* 8: 主动请求
* 0: 主动请求应答
* 差错报文:
	- 3: 终点不可达
	- 4：源抑制, 太快了
	- 5: 重定向 
	- 11: 超时

### ping
ping 发出请求(ICMP ECHO REQUEST), 得到回复(ICMP ECHO REPLY)。
ping 的Request 比原生ICMP多了两个字段: 
- 标识符, 标识包的作用
- 序号，查看质量

### traceroute: 利用差错报文类型
* 设置特殊TTL来追踪去往目的地时沿途经过的路由器
* 故意设置不分片，从而确定MTU

### POINTS
* ICMP相当于网络世界的侦查兵，有主动探查的查询报文和异常报告的差错报文
* ping 使用查询报文，traceroute使用差错报文

## 第八讲 访问外网
![mac & ip header](./images/mac_ip_header.jpeg)
* 判断是不是同一网段(局域网),是则通过ARP直接发送；否则就发往默认网关
* 网关通常是一个路由器，是一个三层转发的设备

网关
- 转发网关: 不改变IP，只改变mac(mac必定改变，因为换了局域网)
- NAT网关: 改变IP

### 欧洲十国游型

### 玄奘西行型
