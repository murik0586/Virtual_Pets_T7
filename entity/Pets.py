import abc


class Pet(abc.ABC):
    _minHP = 0
    def __init__(self, eat: str, drink: str, thirst: float, health: int, hunger: float, voice: str):  # Конструктор
        self.__eat = eat  # Звук еды (Заглушка для тестирования
        self.__drink = drink  # Звук питья (Заглушка для тестирования)
        self.__thirst = thirst  # Жажда
        self.__health = health  # Очки здоровья
        self.__hunger = hunger  # Голод
        self.__voice = voice  # Голос животного

    def get_eat(self):
        """
        Порвывавы
        """

        return self.__eat

    def set_eat(self, eat: str):
        self.__eat = eat
        return

    def get_drink(self):
        return self.__drink

    def set_drink(self, drink: str):
        self.__drink = drink
        return

    def get_voice(self):
        """difdsfasf"""
        return self.__voice

    def set_voice(self, voice: str):
        self.__voice = voice
        return

