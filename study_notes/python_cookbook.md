[原书](https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p03_keep_last_n_items.html)

### 解压赋值
```python
# 个数要求一样
data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
name, shares, price, date = data
name, shares, price, (year, mon, day) = data

# 对字符串也适用
s = 'Hello'
a, b, c, d, e = s

# *用于赋值
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
```

### deque 保留最后几位
```python
from collections import deque
q = deque(maxlen=2)
q.append(1)
q.append(2)
q.append(3)
# 只有2，3，deque会最多保留maxlen个元素，先进先出
print(q)

```

### 最大(小)的N个元素
```python
import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2]

# 对数组进行堆放置, 注意，不是排序！！！
heapq.heapify(nums)
# heapify后就可以用 heappop 进行操作
heapq.heappop(nums)
```
当要查找的元素个数相对比较小的时候，函数 nlargest() 和 nsmallest() 是很合适的。 如果你仅仅想查找唯一的最小或最大（N=1）的元素的话，那么使用 min() 和 max() 函数会更快些。 类似的，如果 N 的大小和集合大小接近的时候，通常先排序这个集合然后再使用切片操作会更快点 （ sorted(items)[:N] 或者是 sorted(items)[-N:] ）。 需要在正确场合使用函数 nlargest() 和 nsmallest() 才能发挥它们的优势 （如果 N 快接近集合大小了，那么使用排序操作会更好些）

### collections.defaultdict 一个键映射多个值
### collections.OrderedDict 顺序字典
* 按键排序
* 一个 OrderedDict 的大小是一个普通字典的两倍，因为它内部维护着另外一个链表

### 字典的运算
* `zip(list_a, list_b, ...)`: 产生一个迭代器，以最短的列表为准，把个列表的同一个index对应的项组合成一个新列表，类似于下面的实现
```python
def zip(iterable, *other_lists):
	min_len = min(len(a) for a in [iterable, *other_lists])
	for i in range(min_len):
		yield (iterable[i], *(a[i] for a in other_lists))
```

### 命名切片
```python
items = [0, 1, 2, 3, 4, 5, 6]
a = slice(2, 4)
items[a] # [2, 3]
```

### 查找众数: collections.Counter
```python
words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]
from collections import Counter
word_counts = Counter(words)
# 出现频率最高的3个单词
top_three = word_counts.most_common(3)
print(top_three)
# Outputs [('eyes', 8), ('the', 5), ('look', 4)]
```
### operator包 vs lambda
* itemgetter(...) <==> lambda d: d['x']
* attrgetter(...) <==> lambda d: getattr(d, 'x')

### itertools.groupby 通过某个字段将记录分组
```python
from operator import itemgetter
from itertools import groupby

# Sort by the desired field first
rows.sort(key=itemgetter('date'))
# Iterate in groups
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)
```
```sh
07/01/2012
  {'date': '07/01/2012', 'address': '5412 N CLARK'}
  {'date': '07/01/2012', 'address': '4801 N BROADWAY'}
07/02/2012
  {'date': '07/02/2012', 'address': '5800 E 58TH'}
  {'date': '07/02/2012', 'address': '5645 N RAVENSWOOD'}
  {'date': '07/02/2012', 'address': '1060 W ADDISON'}
07/03/2012
  {'date': '07/03/2012', 'address': '2122 N CLARK'}
07/04/2012
  {'date': '07/04/2012', 'address': '5148 N CLARK'}
  {'date': '07/04/2012', 'address': '1039 W GRANVILLE'}
```

### Unicode文本标准化 unicodedata
### decimal 模块，精确浮点数运算
### struct 二进制打包/解包
### itertools.islice 对迭代器进行切片
* 实际上是先丢弃掉前面部分循环, 类似于 for 中加 continue
### itertools.dropwhile
* 跳过可迭代对象的开始部分

*碰到看上去有些复杂的迭代问题时，最好可以先去看看itertools模块*
### itertools.permutations 对list进行排列迭代
### itertools.combinations 对list进行组合迭代
### enumerate 序列上索引值迭代
### zip 同时迭代多个序列

