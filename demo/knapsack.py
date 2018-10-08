import numpy

class PkgUnit:
	def __init__(self):
		self.exist = False
		self.belong = False

	def __str__(self):
		return "PkgUnit(exist={}, belong={})".format(self.exist, self.belong)
	
# weights: 可选择的物品重量表
# pkg_size: 背包大小
# return:
#	P[i][k] 布尔型二维数组，表示前i个物品和大小为k的背包存在解
def knapsack(weights: list, pkg_size: int):
	I = len(weights)
	K = pkg_size
	if I == 0 or K == 0:
		return None
	P = [[PkgUnit() for k in range(K + 1)] for i in range(I + 1)]
	for i in range(I + 1):
		for k in range(K + 1):
			print(i, k, "---", id(P[i][k]))
	# 初始情况是存在解的
	P[0][0].exist = True
	# 第0个物品时对有重量的情况都不会存在解
	for k in range(K):
		P[0][k + 1].exist = False
	for i, weight in enumerate(weights):
		i_idx = i + 1
		for k_idx in range(K + 1):
			P[i_idx][k_idx].exist = False
			if P[i_idx - 1][k_idx].exist:
				# i - 1 时解就存在了，不需要再选此物品了
				P[i_idx][k_idx].exist = True
			elif k_idx >= weight:
				# 此时的背包大小本身可以容纳这个物品
				if P[i_idx - 1][k_idx - weight].exist:
					P[i_idx][k_idx].exist = True
					P[i_idx][k_idx].belong = True
	return P

if __name__ == "__main__":
	src = [1, 1]
	res = knapsack(src, 2)
	for i, row in enumerate(res):
		for k, col in enumerate(row):
			c = '-'
			if col.exist:
				if col.belong:
					c = 'Y'
				else:
					c = 'n'
			print(c, end=' ')
		print('')
