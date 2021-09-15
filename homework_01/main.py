
def power_numbers(*nums):
    return [num**2 for num in nums]
print(power_numbers(1, 2, 5, 7))


ODD = "odd"
EVEN = "even"
PRIME = "prime"


def is_ODD(num):
    return num%2 == 0


def is_EVEN(num):
    return num%2 != 0


def is_PRIME(num):
    for i2 in range(2, num):
        if num//i2:
            return False
    return True


def filter_numbers(nums, factor):
    if factor == ODD:
        return list(filter(is_ODD, nums))
    if factor == EVEN:
        return list(filter(is_EVEN, nums))
    if factor == PRIME:
        return list(filter(is_PRIME, nums))


print(filter_numbers(list(range(0, 40)), ODD))