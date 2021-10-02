from homework_02.base import Vehicle
from homework_02.exceptions import CargoOverload


class Plane(Vehicle):

    cargo = 0

    def __init__(self, max_cargo):
        self.max_cargo = max_cargo

    def load_cargo(self, cargo):
        cargo += self.cargo
        if cargo > self.max_cargo:
            raise CargoOverload
        self.cargo = cargo

    def remove_all_cargo(self):
        self.cargo, old_cargo = 0, self.cargo
        return old_cargo

if __name__ == '__main__':
    Plane()