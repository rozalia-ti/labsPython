nums = [0, 6]
target = 6
def two_sum(nums, target):
    for _o1 in range(len(nums)- 1):
        for _o2 in range(_o1 + 1, len(nums)):
            if nums[_o1] + nums[_o2] == target:
                res = [_o1, _o2]
                return(res)
print(two_sum(nums,target))
assert(two_sum(nums,target) == [0, 1], "Проверка провалена")