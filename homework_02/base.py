from homework_02.exceptions import LowFuelError, NotEnoughFuel, CargoOverload


class Vehicle(LowFuelError):

    weight: int = 0
    started: bool = False
    fuel: int = 0
    fuel_consumption: int = 0

    def __init__(self, weight, fuel, fuel_consumption):
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if self.fuel > 0:
            self.started = True
        else:
            raise LowFuelError

    def move(self, distance):
        max_distance = self.fuel / self.fuel_consumption
        if max_distance < distance:
            raise NotEnoughFuel
        self.fuel -= distance * self.fuel_consumption

if __name__ == '__main__':
    Vehicle()
