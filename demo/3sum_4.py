class Solution:
    def do_sorted_sum(self, sorted_nums, start, end):
        if end - start < 3:
            return []
        if end - start == 3:
            if sum(sorted_nums[start:end]) == 0:
                return [sorted_nums[start:end]]
            return []
        mid = start + (end - start) // 2
        results = self.do_sorted_sum(sorted_nums, start, mid)
        right_sub = self.do_sorted_sum(sorted_nums, mid, end)
        for i in right_sub:
            if i not in results:
                results.append(i)
        for i in range(start, mid):
            l = mid
            r = end - 1
            while r > l:
                s = sorted_nums[i] + sorted_nums[l] + sorted_nums[r]
                if s == 0:
                    t = [sorted_nums[i], sorted_nums[l], sorted_nums[r]]
                    if t not in results:
                        results.append(t)
                    l += 1
                    r -= 1
                elif s > 0:
                    r -= 1
                else:
                    l += 1
        for i in range(mid, end):
            l = start
            r = mid - 1
            while r > l:
                s = sorted_nums[l] + sorted_nums[r] + sorted_nums[i]
                if s == 0:
                    t = [sorted_nums[l], sorted_nums[r], sorted_nums[i]]
                    if t not in results:
                        results.append(t)
                    l += 1
                    r -= 1
                elif s > 0:
                    r -= 1
                else:
                    l += 1
        return results

    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if not nums or len(nums) < 3:
            return []
        sorted_nums = sorted(nums)
        return self.do_sorted_sum(sorted_nums, 0, len(sorted_nums))
                   
                    

if __name__ == "__main__":
    src = [-7,-5,5,-6,-2,1,7,3,-4,-2,-2,-4,-8,-1,8,8,-2,-7,3,2,-7,8,-3,-10,5,2,8,7,7]
    src = [0, 1, -1, 2, -1]
    src = [0, 0, 0, 1, -1, 2, -1, -7,-5,5,-6,-2,1,7,3,-4,-2,-2,-4,-8,-1,8,8,-2,-7,3,2,-7,8,-3,-10,5,2,8,7,7]
    src = [-4, -2, -1]
    src = [-2, -2, 0, 1, 1, 2]
    s = Solution()
    print(s.threeSum(src))

