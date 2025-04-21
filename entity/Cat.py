from entity.Pet import Pet


# todo доделать
class Cat(Pet):
    type_of_pet = "Кот" #Это поле для красивого отображения в __str__ - стр это аналог toString() из java
    def __init__(self, nickname: str, breed: str, points_health: int = 10, voice: str = "Мяу-мяу",
                 happiness_indicator: int = 2, hunger_level: int = 2, thirst: int = 2):
        """Инициализирует Кота.
             :param nickname: Кличка Кота
             :param thirst: Уровень жажды(0 - 20)
             :param points_health: Очки здоровья (пока условимся что у Кота макс 30)
             :param happiness_indicator: Уровень счастья(по умолчанию 2)
             :param hunger_level: Уровень голода(по умолчанию 2)
             :param voice: мяукает по умолчанию
             :param breed: Порода Кота
             """
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
        """Погулять с котом.
        +1 к счастью, +3 к голоду, +2 к жажде"""
        print(f"{self.nickname} идет на прогулку!")
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
