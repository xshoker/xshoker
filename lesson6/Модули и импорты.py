import exception as ex
import Baskets


if __name__ == '__main__':
    basket = Baskets.Basket()
    print(basket)

try:
    first = int(input('Enter number: '))
    second = int(input('Enter number: '))
    print(second/first)
except (ValueError, ZeroDivisionError) as ex:
    print(ex)

try:
    f = open('otus.txt')
    content = f.readlines()
    print(content)
except AttributeError:
    print('Dich')
finally:
    f.close()