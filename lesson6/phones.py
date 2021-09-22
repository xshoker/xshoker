class BaseProduct:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):  # user view
        # print("__str__ is called")
        return f"{self.name} (price = {self.price})"

    def __repr__(self):  # python view
        # print("__repr__ is called")
        return f"{self.__class__.__name__} ('{self.name}', {self.price})"


class Laptop(BaseProduct):
    pass


class MobilePhone(BaseProduct):
    pass


class Basket:

    def __init__(self):
        self._items = []

    def __iadd__(self, product):
        self._items.append(product)
        return self

    def add(self, product):
         self._items.append(product)


samsung_note_10 = MobilePhone('Samsung Galaxy Note 10', 1000)
mac_pro = Laptop('Macbook Pro 16"', 3500)
nokia = MobilePhone("Nokia 3310", 50)

# basket = 0
# # print(samsung_note_10)
# basket = [samsung_note_10, mac_pro, nokia]
# # print(basket)
# nokia_repr = repr(nokia)
# print(nokia_repr, type(nokia_repr))
# nokia_clone = eval(repr(nokia))
# print(nokia_clone, type(nokia_clone))
# print(nokia_clone.price)

basket = Basket()
# basket.items.append(samsung_note_10)
# basket.items.append(mac_pro)
# print(basket)
# basket += samsung_note_10
# basket += mac_pro
# basket += nokia
print(basket._discount)
# print(basket._Basket__item)