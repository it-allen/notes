import heapq

class Heap:
	def __init__(self):
		self.elements = []

	def push(self, ele):
		current_idx = len(self.elements)
		self.elements.append(ele)
		parent_idx = (current_idx - 1) >> 1
		# 最小堆，父亲的权重小于子节点的权重
		while current_idx > 0 and self.elements[current_idx] < self.elements[parent_idx]:
			self.elements[current_idx], self.elements[parent_idx] = self.elements[parent_idx], self.elements[current_idx]
			current_idx, parent_idx = parent_idx, (parent_idx - 1) >> 1
	
	def pop(self):
		if not self.elements:
			return None
		ele = self.elements.pop(0)
		if len(self.elements) == 0:
			return ele
		self.elements.insert(0, self.elements.pop())
		max_idx = len(self.elements) - 1
		current_idx = 0
		while 2 * current_idx + 1 <= max_idx:
			left_cld = 2 * current_idx + 1
			right_cld = 2 * (current_idx + 1)
			smaller_cld_idx = left_cld
			if right_cld <= max_idx and self.elements[right_cld] < self.elements[left_cld]:
				smaller_cld_idx = right_cld
			# 最小堆，父亲的权重小于子节点的权重
			if self.elements[smaller_cld_idx] >= self.elements[current_idx]:
				# 节点值已经比子节点们都小
				break
			self.elements[current_idx], self.elements[smaller_cld_idx] = self.elements[smaller_cld_idx], self.elements[current_idx]
			current_idx = smaller_cld_idx
		return ele

if __name__ == "__main__":
	src = [23, 1, 3, 42, 2, 5, 7, 3, 9, 36]
	h = Heap()
	for each in src:
		h.push(each)
		print("After push:", h.elements)
	a = h.pop()
	while a:
		print(a, end=' ')
		a = h.pop()
	print()

	print("Use heapq")
	h1 = []
	for each in src:
		heapq.heappush(h1, each)
		print("After push:", h1)
	a = heapq.heappop(h1)
	while a:
		print(a, end=' ')
		if not h1:
			break
		a = heapq.heappop(h1)
	print()


