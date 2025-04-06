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
        """Погулять с собакой.
        +1 к счастью, +3 к голоду, +2 к жажде"""
        print(f"{self.nickname} радостно бежит на прогулку! ")
        self.happiness_indicator += 1
        self.hunger_level += 3
        self.thirst += 2
    
        # Проверка на исчезновение питомца
        if self.happiness_indicator <= 0 or self.points_health <= 0:
            print(f"{self.nickname} исчез! ")
            self.__life = False

    def ignore(self):
        #todo Дарья
        pass


    def __str__(self):
        return super().__str__() + f"\nПорода:{self.__breed} "
