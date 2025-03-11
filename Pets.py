import abc

class Pet(abc.ABC):
    # Инициализация полей (в некоторых яп называют переменными)
    def __init__(self, eat : str, drink : str, thirst : float, health : int, hunger : float, voice : str): #Конструктор
        self.__eat = eat # Звук еды (Заглушка для тестирования, переделаем на анимации)
        self.__drink = drink # Звук питья (Заглушка для тестирования, переделаем на анимации)
        self.__thirst = thirst # Жажда
        self.__health = health # Очки здоровья
        self.__hunger = hunger # Голод
        self.__voice = voice # Голос животного

    @abc.abstractmethod
    def get_eat(self):
        print(self.__eat)
        self.__hunger = 0
        return

    @abc.abstractmethod
    def set_eat(self, eat : str):
        self.__eat = eat
        return

    @abc.abstractmethod
    def get_drink(self):
        print(self.__drink)
        self.__thirst = 0
        return

    @abc.abstractmethod
    def set_drink(self, drink : str):
        self.__drink = drink
        return

    @abc.abstractmethod
    def get_voice(self):
        print(self.__voice)
        return

    @abc.abstractmethod
    def set_voice(self, voice : str):
        self.__voice = voice
        return

class Cat(Pet):
    def __init__(self, eat, drink, thirst, health, hunger):
        super().__init__(eat, drink, thirst, health, hunger)
        self.__voice = "Мяу-Мяу"

    def get_walk(self): return "Топ-Топ"

    def set_walk(self): return

class Dog(Pet):
    def __init__(self, eat, drink, thirst, health, hunger):
        super().__init__(eat, drink, thirst, health, hunger)
        self.__voice = "Гав-Гав"

    def get_walk(self): return "Топ-Топ"

    def set_walk(self): return

