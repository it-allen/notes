<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [认证与登录](#%E8%AE%A4%E8%AF%81%E4%B8%8E%E7%99%BB%E5%BD%95)
  - [密钥登录](#%E5%AF%86%E9%92%A5%E7%99%BB%E5%BD%95)

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
