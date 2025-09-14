
class CoffeeMachine:

    water_tank_size = 1000
    coffee_storage_size = 200
    waste_storage_size = 100

    def __init__(self):
        self.coffee_storage = 0
        self.water_tank = 0
        self.waste_storage = 0
        self.coffee_counter = 0

        self.coffee_per_brewing = 12
        self.water_per_brewing = 150

    def add_coffee(self, coffee_amount):
        self.coffee_storage = min(self.coffee_storage + coffee_amount, CoffeeMachine.coffee_storage_size)

    def add_water(self, water_amount):
        self.water_tank = min(self.water_tank + water_amount, CoffeeMachine.water_tank_size)

    def is_ready_to_brew(self):
        if self.water_tank < self.water_per_brewing:
            return False
        if self.coffee_storage < self.coffee_per_brewing:
            return False
        if self.waste_storage >= CoffeeMachine.waste_storage_size:
            return False
        return True
    
    def brew_coffee(self):
        if not self.is_ready_to_brew():
            print("Cannot brew coffee! :(")
            return
        self.water_tank -= self.water_per_brewing
        self.coffee_storage -= self.coffee_per_brewing
        self.waste_storage += self.coffee_per_brewing
        self.coffee_counter += 1
        print("Coffee is ready! :)")