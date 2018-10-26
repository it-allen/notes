<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [language](#language)
  - [C](#c)
  - [Go](#go)
    - [教程 & 文章](#%E6%95%99%E7%A8%8B--%E6%96%87%E7%AB%A0)
- [linux](#linux)
  - [进程间通信](#%E8%BF%9B%E7%A8%8B%E9%97%B4%E9%80%9A%E4%BF%A1)
    - [pipe](#pipe)
- [protocol](#protocol)
  - [http](#http)
    - [http status](#http-status)
- [database](#database)
  - [mysql](#mysql)
    - [MySQL索引优化分析](#mysql%E7%B4%A2%E5%BC%95%E4%BC%98%E5%8C%96%E5%88%86%E6%9E%90)
    - [MySQL-索引](#mysql-%E7%B4%A2%E5%BC%95)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# language
## C
* "||" 操作最终的值是bool(0/1), 不像 python 的 or 那样可以将短路运算的值返回

## Go
### 教程 & 文章
* [《Go入门指南》](http://wiki.jikexueyuan.com/project/the-way-to-go/)

# linux
## 进程间通信
方式: pipe

### pipe
参见[这篇文章](https://segmentfault.com/a/1190000009528245)

# protocol
## http
### http status
* [502 vs 504](https://github.com/zhangyachen/zhangyachen.github.io/issues/89) 写得极好
* 502: 

# database
## mysql
### [MySQL索引优化分析](http://www.cnblogs.com/itdragon/p/8146439.html)
**精品**

### [MySQL-索引](https://segmentfault.com/a/1190000003072424)
* 索引存储分类
    - B-Tree: 最常见，大部分引擎都支持 B-Tree
    - Hash: 只有 Memory 引擎支持
    - R-Tree(空间索引): MyISAM的一种特殊索引类型，主要用于地理空间数据类型
    - Full-text (全文索引)：MyISAM的一种特殊索引类型，主要用于全文索引，InnoDB从MYSQL5.6版本提供对全文索引的支持。
* B-Tree 索引类型
    - 普通索引
    - UNIQUE索引
    - 主键：PRIMARY KEY索引
* 索引操作语法
    - 设置索引
```SQL
ALTER TABLE table_name ADD INDEX index_name (column_list);
ALTER TABLE table_name ADD UNIQUE (column_list);
ALTER TABLE table_name ADD PRIMARY KEY (column_list);


CREATE INDEX index_name ON table_name (column_list);
CREATE UNIQUE INDEX index_name ON table_name (column_list);
```

    - 删除索引
```sql
DROP INDEX index_name ON talbe_name;
ALTER TABLE table_name DROP INDEX index_name;
ALTER TABLE table_name DROP PRIMARY KEY;
```

    - 查看索引
```sql
show index from tblname;
show keys from tblname;
```

* 索引选择原则
    - 较频繁的作为查询条件的字段应该创建索引
    - 唯一性太差的字段不适合单独创建索引，即使频繁作为查询条件
    - 更新非常频繁的字段不适合创建索引
    - 不会出现在 WHERE 子句中的字段不该创建索引

* 下面情况不适合用索引
    - 表记录比较少(2000 以内？)
    - 索引的选择性较低
    - MySQL只对一下操作符才使用索引：<,<=,=,>,>=,between,in, 以及某些时候的like(不以通配符%或\_开头的情形)
    - 不要过度索引，只保持所需的索引

* 索引的弊端: 消耗资源(维护和存储)

