nums = [3, 4] # вот эти значения вообще никак не влияют на результаты теста, это всего ллишь инициализация
target = 42
def two_sum(nums, target):
    if (all(isinstance(x, int) for x in nums)) and (isinstance(target, int)): #проверка на целочисленные значения
        for _o1 in range(len(nums)- 1):
            for _o2 in range(_o1 + 1, len(nums)):
                if nums[_o1] + nums[_o2] == target:
                    res = [_o1, _o2]
                    return(res)
    print(two_sum(nums,target))
    # assert(two_sum(nums,target) == [0, 1], "Проверка провалена") #вот эту строчку я комментирую потому что тесты происходят в файле test.py 
