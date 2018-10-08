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
        if not nums or len(nums) < 3:
            return []
        sorted_nums = sorted(nums)
        size = len(sorted_nums)
        results = []
        for i in range(0, size - 1):
            l = i + 1
            r = size - 1
            while r > l:
                s = sorted_nums[i] + sorted_nums[l] + sorted_nums[r]
                if s < 0:
                    l += 1
                    continue
                elif s > 0:
                    r -= 1
                    continue
                else:
                    hashable = [sorted_nums[i], sorted_nums[l], sorted_nums[r]]
                    if hashable not in results:
                        results.append(hashable)
                    l += 1
                    r -= 1
        return results
                    
                    

if __name__ == "__main__":
    src = [-7,-5,5,-6,-2,1,7,3,-4,-2,-2,-4,-8,-1,8,8,-2,-7,3,2,-7,8,-3,-10,5,2,8,7,7]
    src = [0, 1, -1, 2, -1]
    src = [0, 0, 0, 1, -1, 2, -1, -7,-5,5,-6,-2,1,7,3,-4,-2,-2,-4,-8,-1,8,8,-2,-7,3,2,-7,8,-3,-10,5,2,8,7,7]
    #src = [-4, -2, -1]
    #src = [-2, -2, 0, 1, 1, 2]
    s = Solution()
    print(s.threeSum(src))

