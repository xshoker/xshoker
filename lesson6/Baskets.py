class Basket:

    def __init__(self, max_size = 0):
        self.max_size = 100


    def __str__(self):
        return f'{self.__class__.__name__}: max_size = {self.max_size}'


class IncorrectValueNumber(BaseException):
    pass
