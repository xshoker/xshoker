from homework_02.exceptions import LowFuelError, NotEnoughFuel, CargoOverload


class Vehicle(LowFuelError):

    weight = int
    started = bool
    fuel = int
    fuel_consumption = int

    def __init__(self, weight, fuel, fuel_consumption):
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if self.fuel <= 0:
            raise LowFuelError
        else:
            self.started = True

    def move(self, distance):
        max_distance = self.fuel / self.fuel_consumption
        if max_distance < distance:
            raise NotEnoughFuel
        self.fuel -= distance * self.fuel_consumption

if __name__ == '__main__':
    Vehicle()
