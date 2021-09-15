
def power_numbers(*nums):
    return [num**2 for num in nums]


ODD = "odd"
EVEN = "even"
PRIME = "prime"


def is_odd(num):
    return num % 2 != 0


def is_even(num):
    return num % 2 == 0


def is_prime(num):
    if num == 0:
        return False
    else:
        for i2 in range(2, num):
            if num % i2 == 0:
                return False
        return True


def filter_numbers(nums, factor):
    if factor == ODD:
        return list(filter(is_odd, nums))
    if factor == EVEN:
        return list(filter(is_even, nums))
    if factor == PRIME:
        return list(filter(is_prime, nums))


#print(filter_numbers(list(range(0, 40)), PRIME))