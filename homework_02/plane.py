from homework_02.base import Vehicle
from homework_02.exceptions import CargoOverload


class Plane(Vehicle):
    cargo = int
    max_cargo = int

    def __init__(self, weight, fuel, fuel_consumption, max_cargo):
        self.max_cargo = max_cargo
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption


    def load_cargo(self, cargo):
        cargo += cargo
        if cargo > self.max_cargo:
            raise CargoOverload
        self.cargo = cargo

    def remove_all_cargo(self):
        old_cargo = self.cargo
        self.cargo = 0
        return old_cargo

if __name__ == '__main__':
    Plane()