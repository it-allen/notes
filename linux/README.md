<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [认证与登录](#%E8%AE%A4%E8%AF%81%E4%B8%8E%E7%99%BB%E5%BD%95)
  - [密钥登录](#%E5%AF%86%E9%92%A5%E7%99%BB%E5%BD%95)
- [环境变量](#%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)
  - [打印所有环境变量](#%E6%89%93%E5%8D%B0%E6%89%80%E6%9C%89%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)
- [性能维护](#%E6%80%A7%E8%83%BD%E7%BB%B4%E6%8A%A4)
  - [dh 查询目录下文件大小](#dh-%E6%9F%A5%E8%AF%A2%E7%9B%AE%E5%BD%95%E4%B8%8B%E6%96%87%E4%BB%B6%E5%A4%A7%E5%B0%8F)
  - [ps 查看资源指标](#ps-%E6%9F%A5%E7%9C%8B%E8%B5%84%E6%BA%90%E6%8C%87%E6%A0%87)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 认证与登录
## 密钥登录
* 创建RSA密钥对
```sh
$ ssh-keygen -t rsa [-C 'demo']
Enter file in which to save the key (/home/demo/.ssh/id_rsa): <可以改名>
Enter passphrase (empty for no passphrase): <可以为密钥文件设密码>
``` 
这样可以生成以下两个文件
```sh
-rw-------  1 hyku  staff  1675  2 13 14:40 id_rsa
-rw-r--r--  1 hyku  staff   404  2 13 14:40 id_rsa.pub
```

* 将公钥放在服务器上(即客户端用私钥去登陆)
```sh
ssh-copy-id <username>@<host>
# 或者
cat ~/.ssh/id_rsa.pub | ssh <username>@<host> "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"
```

# 环境变量
## 打印所有环境变量
```sh
printenv
```

# 性能维护
## dh 查询目录下文件大小
* mac
```sh
du -h -d 1
```

## ps 查看资源指标
* linux
```sh
# CPU占用最多的前10个进程： 
ps auxw|head -1;ps auxw|sort -rn -k3|head -10

# 内存消耗最多的前10个进程 
ps auxw|head -1;ps auxw|sort -rn -k4|head -10

# 虚拟内存使用最多的前10个进程 
ps auxw|head -1;ps auxw|sort -rn -k5|head -10

# 或者
ps auxw --sort=rss
ps auxw --sort=%cpu
```

ps 参数含义
* %MEM: 进程的内存占用率
* MAJFL: the major page fault count
* VSZ: 进程所使用的虚存的大小
* RSS: 进程使用的驻留集大小或者是实际内存的大小(RSS is the "resident set size" meaning physical memory used)
* TTY 与进程关联的终端（tty）
    - 串行端口终端（/dev/ttySn）
    - 伪终端（/dev/pty/） 
    - 控制终端（/dev/tty） 
    - 控制台终端（/dev/ttyn,   /dev/console） 
    - 虚拟终端(/dev/pts/n)
* STAT 检查的状态：进程状态使用字符表示的，
    - R（running正在运行或准备运行）
    - S（sleeping睡眠）
    - I（idle空闲）
    - Z (僵死)
    - D（不可中断的睡眠，通常是I/O）
    - P（等待交换页）
    - W（换出,表示当前页面不在内存）
    - N（低优先级任务）
    - T(terminate终止)
    - W has no resident pages

    - <    高优先级 
    - N    低优先级 
    - L    有些页被锁进内存 
    - s    包含子进程 
    - +    位于后台的进程组； 
    - l    多线程，克隆线程  multi-threaded (using `CLONE_THREAD`, like NPTL pthreads do) 
