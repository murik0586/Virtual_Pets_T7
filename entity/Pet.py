from functools import wraps

from entity.PetState import PetState

# Декоратор -> в общем запрещает действия если питомец мертв
def check_alive(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.state.is_alive:
            print(f"{self.name} больше не реагирует...")  # можно кастомизировать
            return
        return method(self, *args, **kwargs)

    return wrapper

class Pet:
    type_of_pet = "Питомец"


    def __init__(self, name: str, health: int = 5):
        self.__name = name
        self.state: PetState = PetState(health)


    ##Геттеры Мурат
    @property  # Это сигнатура для геттера!
    def name(self):
        return self.__name  # Геттеры возвращают просто значение полей(свойств)

    ##Сеттеры Мурат
    @name.setter  # Сигнатура для сеттера
    def name(self, name: str):
        if len(name) <= 2:  # Условие, что нельзя имя дать меньше по длине
            print("Имя должно быть не короче двух символов")
        else:
            self.__name = name
    @check_alive
    def feed(self):
        """покормить питомца -2 к голоду"""
        self.state.hunger -= 2

    @check_alive #Вызов декоратора!
    def stroke(self):
        """погладить питомца + 1 к счастью, +1 к голоду"""
        self.state.happiness += 1
        self.state.hunger += 1

    @check_alive
    def give_treat(self):
        """дать вкусняшку питомцу +2 к счастью,- 1 к голоду"""

        self.state.happiness += 2
        self.state.hunger -= 1

    @check_alive
    def walk(self):
        """погулять с питомцем + 1 к счастью, + 3 к голоду"""

        print(f"{self.name} идет на прогулку!")
        self.state.happiness += 1
        self.state.hunger += 3

    @check_alive
    def ignore(self):
        """игнорировать питомца -1 к счастью, + 1 к голоду"""

        self.state.happiness -= 1
        self.state.hunger += 1

    def __str__(self):
        if not self.state.is_alive:
            return f"{self.type_of_pet} {self.name} умер :("
        return f"{self.type_of_pet} {self.name}\n{self.state}"
