from homework_02.base import Vehicle
from homework_02.exceptions import CargoOverload


class Plane(Vehicle):

    cargo = 0

    def __init__(self, max_cargo):
        super().__init__(self)
        self.max_cargo = max_cargo

    def load_cargo(self, cargo):
        cargo += self.cargo
        if cargo > self.max_cargo:
            raise CargoOverload
        self.cargo = cargo

    def remove_all_cargo(self):
        old_cargo = self.cargo
        self.cargo = 0
        return old_cargo

if __name__ == '__main__':
    Plane()