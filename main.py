def power_numbers(*nums):
        return ([num ** 2 for num in nums])

print(power_numbers(1, 2, 5, 7))

ODD = [i for i in range(10)]
EVEN = [i for i in range(10)]

def filter_numbers(*nums):
    print([i for i in ODD if i % 2 == 0])
    print([i for i in EVEN if i % 2 != 0])
    return

filter_numbers(1, 2, 3)