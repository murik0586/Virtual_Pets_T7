from entity.PetState import PetState

class Pet():
    type_of_pet = "Питомец"

    def __init__(self, name: str, health: int = 5):
        self.__name = name
        self.state = PetState(health)

    ##Геттеры Мурат
    @property  # Это сигнатура для геттера!
    def name(self):
        return self.__name  # Геттеры возвращают просто значение полей(свойств)

    ##Сеттеры Мурат
    @name.setter  # Сигнатура для сеттера
    def name(self, name: str):
        if len(name) <= 2:  # Условие, что нельзя имя дать меньше по длине
            print("Имя должно быть от двух символов")
            return
        else:
            self.__name = name

    def feed(self):
        # todo Игорь
        """покормить питомца -2 к голоду"""
        if not self.state.is_alive:
            return
        self.state.hunger -= 2

    def stroke(self):
        """погладить питомца + 1 к счастью, +1 к голоду"""
        if not self.state.is_alive:
            return
        self.state.happiness += 1
        self.state.hunger += 1

    def give_treat(self):
        """дать вкусняшку питомцу +2 к счастью,- 1 к голоду"""
        if not self.state.is_alive:
            return
        self.state.happiness += 2
        self.state.hunger -= 1

    def walk(self):
        """погулять с питомцем + 1 к счастью, + 3 к голоду"""
        if not self.state.is_alive:
            return
        print(f"{self.name} идет на прогулку!")
        self.state.happiness += 1
        self.state.hunger += 3

    def ignore(self):
        """игнорировать питомца -1 к счастью, + 1 к голоду"""
        if not self.state.is_alive:
            return
        self.state.happiness -= 1
        self.state.hunger += 1

    def __str__(self):
        if not self.state.is_alive:
            return f"{self.type_of_pet} {self.name} умер :("
        return f"{self.type_of_pet} {self.name}\n{self.state}"