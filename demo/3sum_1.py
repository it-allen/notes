class Solution:
    def binary_search(self, sorted_list, start, end, target):
        if end < start:
            return False
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
       
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if len(nums) < 3:
            return []
        sorted_nums = sorted(nums)
        size = len(sorted_nums)
        non_negative_idx = None
        for idx, each in enumerate(sorted_nums):
            if each >= 0:
                non_negative_idx = idx
                break
        if non_negative_idx is None:
            return []
        results = set()
        if sorted_nums[non_negative_idx] == 0:
            if non_negative_idx + 2 < size:
                if sorted_nums[non_negative_idx + 1] == 0 and sorted_nums[non_negative_idx + 2] == 0:
                    results.add((0, 0, 0))
        for i in range(0, non_negative_idx):
            for j in range(i + 1, non_negative_idx):
                tmp = 0 - (sorted_nums[i] + sorted_nums[j])
                if self.binary_search(sorted_nums, non_negative_idx, size - 1, tmp):
                    results.add((sorted_nums[i], sorted_nums[j], tmp))
        for i in range(non_negative_idx, size):
            for j in range(i + 1, size):
                tmp = 0 - (sorted_nums[i] + sorted_nums[j])
                if self.binary_search(sorted_nums, 0, non_negative_idx - 1, tmp):
                    results.add((tmp, sorted_nums[i], sorted_nums[j]))
        return [[*i] for i in results]

if __name__ == "__main__":
    src = [-7,-5,5,-6,-2,1,7,3,-4,-2,-2,-4,-8,-1,8,8,-2,-7,3,2,-7,8,-3,-10,5,2,8,7,7]
    src = [0, 1, -1, 2, -1]
    src = [0, 0, 0, 1, -1, 2, -1, -7,-5,5,-6,-2,1,7,3,-4,-2,-2,-4,-8,-1,8,8,-2,-7,3,2,-7,8,-3,-10,5,2,8,7,7]
    src = [-4, -2, -1]
    s = Solution()
    print(s.threeSum(src))

