
def power_numbers(*nums):
    return [num**2 for num in nums]


ODD = "odd"
EVEN = "even"
PRIME = "prime"


def is_prime(num):
    for i2 in range(2, num):
        if num % i2 == 0:
            return False
    if num < 2:
        return False
    return True


def filter_numbers(nums, factor):
    if factor == ODD:
        return list(filter(lambda x: x % 2 != 0, nums))
    if factor == EVEN:
        return list(filter(lambda x: x % 2 == 0, nums))
    if factor == PRIME:
        return list(filter(is_prime, nums))


print(filter_numbers(list(range(50)), PRIME))