class Solution:
    def binary_search(self, sorted_list, start, end, target):
        if end == start:
            if target == sorted_list[start]:
                return True
            return False
        if end == start + 1:
            if target in sorted_list[start:end+1]:
                return True
            return False
        mid = start + (end - start) // 2
        if target < sorted_list[mid]:
            return self.binary_search(sorted_list, start, mid - 1, target)
        elif target > sorted_list[mid]:
            return self.binary_search(sorted_list, mid + 1, end, target)
        else:
            return True

    def twoSortedSum(self, sorted_list, target, start, end):
        if end == start:
            return []
        if end == start + 1:
            if sorted_list[start] + sorted_list[end] == target:
                return [[sorted_list[start], sorted_list[end]]]
            return []
        results = []
        filter_ = set()
        while start < end:
            s = sorted_list[start] + sorted_list[end]
            if s == target:
                hashable = (sorted_list[start], sorted_list[end])
                if hashable not in filter_:
                    results.append([sorted_list[start], sorted_list[end]])
                    filter_.add(hashable)
                end -= 1
                continue
            if s > target:
                end -= 1
                continue
            if s < target:
                start += 1
                continue
        return results

    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if len(nums) < 3:
            return []
        sorted_nums = sorted(nums)
        size = len(sorted_nums)
        results = []

        filter_ = set()
        for i in range(2, size):
            two_tuples = self.twoSortedSum(sorted_nums, 0 - sorted_nums[i], 0, i - 1)
            print("Got", two_tuples)
            for t in two_tuples:
                hashable = (*t, sorted_nums[i])
                if hashable not in filter_:
                    results.append([*t, sorted_nums[i]])
                    filter_.add(hashable)
        return results

if __name__ == "__main__":
	src = [0, 0, 0]
	s = Solution()
	print(s.threeSum(src))

