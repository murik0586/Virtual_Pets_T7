from entity.Pet import Pet


class Dog(Pet):
    type_of_pet = "Собака" #Это поле для красивого отображения в __str__ - стр это аналог toString() из java
    def __init__(self, nickname: str, breed: str, points_health: int, voice: str = "Гав-гав",
                 happiness_indicator: int = 2, hunger_level: int = 2, thirst: int = 2):
        super().__init__(nickname, points_health, voice, happiness_indicator, hunger_level, thirst)
        self.__breed = breed



    def give_water(self):
        # todo Елизар
        pass

    def feed(self):
        # todo Игорь
        pass

    def pet(self):
        # todo Мурат
        pass

    def give_treat(self):
        # todo Игорь
        pass

    def walk(self):
        # todo Елизар
        pass

    def ignore(self):
        #todo Дарья
        pass


    def __str__(self):
        return super().__str__() + f"\nПорода:{self.__breed} "