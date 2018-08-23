# Elastic Search
### install
* 安装 java 8
* 下载es
```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.2.tar.gz
tar xf elasticsearch-5.5.2.tar.gz
cd elasticsearch-5.5.2/bin
./elasticsearch
```

### 配置
* 修改配置: ${elasticsearch}/config/elasticsearch.yml
```yaml
# 默认为 elasticsearch
cluster.name: <集群名称>
# 节点名称，应该集群内唯一
node.name: node.10.70.1.101
# 数据和日志目录
path.data:
path.logs:
# 绑定
network.host: 0.0.0.0
# 集群内其它任意点的IP列表
discovery.zen.ping.unicast.hosts: ["10.70.1.102"]
```

# 插件
## [ik 中文分词器](https://github.com/medcl/elasticsearch-analysis-ik)

# trouble shooting
#### fielddata text error
错误:
Fielddata is disabled on text fields by default. Set fielddata=true on [interests] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead
解决:
```sh
curl -XPUT 'localhost:9200/megacorp/_mapping/employee?pretty' -H 'Content-Type: application/json' -d'
{
  "properties": {
    "interests": { 
      "type":     "text",
      "fielddata": true
    }
  }
}
'
# 其中 megacorp 为 index
# employee 为 type
```


#### `Variable [new_tag] is not defined.`
教程上请求:
```sh
curl -XPOST 'localhost:9200/website/blog/1/_update?pretty' -H 'Content-Type: application/json' -d'
{
   "script" : "ctx._source.tags+=new_tag",
   "params" : {
      "new_tag" : "search"
   }
}
'
```
新版语法:
```sh
curl -XPOST 'localhost:9200/website/blog/1/_update?pretty' -H 'Content-Type: application/json' -d'
{
    "script": {
        "inline": "ctx._source.tags.add(params.new_tag)",
        "params": {
            "new_tag": "test"
        }
    }
}'
```


### 当运行的host 不为默认值(127.0.0.1)时，会触发检查，报以下错
* max file descriptors [4096] for elasticsearch process is too low, increase to at least [65536]
```sh
# vim /etc/security/limits.conf append
admin            -       nofile          65536 # add this line for es
```
* max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```sh
sudo sysctl -w vm.max_map_count=262144
```

### JVM Heap size error
* Java HotSpot(TM) 64-Bit Server VM warning: INFO: os::commit_memory(0x000000008a660000, 1973026816, 0) failed; error='Cannot allocate memory' (errno=12)
```sh
# 启动时加 JVM 选项
ES_JAVA_OPTS="-Xms512m -Xmx512m" ./bin/elasticsearch
```

### can not run elasticsearch as root
不能用root 运行elasticsearch, 出于安全考虑
```sh
# 创建用户组
groupadd es
# 创建用户
useradd es -g es -p es

# 更改elasticsearch目录所属
chown -R es:es elasticsearch-5.5.2

# 切换到 es 用户运行
```
