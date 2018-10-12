# 第三方参考
[排序算法演示](https://visualgo.net/zh/sorting)
[笔记](https://github.com/qiwsir/algorithm)

# 排序
## 堆排序
[动画演示](https://bajdcc.github.io/html/heap.html)
[示例](http://bubkoo.com/2014/01/14/sort-algorithm/heap-sort/)

# 子串匹配
## 最长回文子串
[题目](https://leetcode.com/problems/longest-palindromic-substring/description/)

# 路径算法
## 最短路径算法
### Dijsktra
* [实现一](./demo/dijkstra.py)

# 动态规划
## 背包问题
* [实现](./demo/knapsack.py)


# 思考题
* 已知字符串A, 求其中的所有的对称子串。（对称子串定义为 "aa", "aba", "abba"等）
	- 方法一：将A倒序为 A`，对 A 和 A` 求公共子串，求子串方法[参考](), 复杂度为 O(n + k)
	- 方法二：遍历找到两种类型(`aa`, `aba`)的所有子串，然后分开以中线为中心向两边扩展
* 已知一棵树，求任意两个节点的共同祖先。
	- 方法一: BFS, 需要记录中间状态
	- 方法二：递归分治, 性能差一点, 但逻辑简单
* 输入任意 N 个数，求前 k 大的数(0 < k < N).
	- 方法一: 先排序，再取 k 个大的数, O(nlgn)
	- 方法二：入大堆，再出堆 k 个。

# leetcode
* [三数和](https://leetcode-cn.com/problems/3sum/description/)
	- 方法一: [递归](./demo/3sum.py), O(n^2)
	- 方法二：[分类](./demo/3sum_1.py), O(n^2)
	- 方法三: [利用两数之和递推](./demo/3sum_2.py), O(nlogn)
	- 方法四：[分治+两数之和](./demo/3sum_4.py), O(nlogn)
    - *拓展*: [N数和](https://leetcode.com/problems/4sum/discuss/8545/Python-140ms-beats-100-and-works-for-N-sum-(Ngreater2))



# TODO
## 无锁队列
* [Coolshell](https://coolshell.cn/articles/8239.html)

## MPI
* [zhihu](https://zhuanlan.zhihu.com/p/25332041)
