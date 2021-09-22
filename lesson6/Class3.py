class Mammal:
    pass


class HomoSapiens():
    pass


class Human(HomoSapiens, Mammal):
    pass


print(Mammal.mro())
print(HomoSapiens.mro())
print(Human.mro())
