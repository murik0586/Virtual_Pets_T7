import abc

class Pet(abc.ABC):
    _eat = "" # Звук еды (Заглушка для тестирования, переделаем на анимации)
    _drink = "" # Звук питья (Заглушка для тестирования, переделаем на анимации)
    _voice = "" # Голос животного
    _thirst = 0.0 # Жажда
    _health = 0 # Очки здоровья
    _hunger = 0.0 # Голод

    def __init__(self, _eat, _drink, _thirst, _health, _hunger): #Конструктор
        self._eat = _eat #Инициализация полей (в некоторых яп называют переменными)
        self._drink = _drink
        self._thirst = _thirst
        self._health = _health
        self._hunger = _hunger

    @abc.abstractmethod
    def eat(self):
        print(self._eat)
        self._hunger = 0
        return

    @abc.abstractmethod
    def drink(self):
        print(self._drink)
        self._thirst = 0
        return

    @abc.abstractmethod
    def voice(self):
        print(self._voice)
        return

class Cat(Pet):
    def __init__(self, _eat, _drink, _thirst, _health, _hunger):
        super().__init__(_eat, _drink, _thirst, _health, _hunger)
        self._voice = "Мяу-Мяу"

    def walk(self): return "Топ-Топ"

class Dog(Pet):
    def __init__(self, _eat, _drink, _thirst, _health, _hunger):
        super().__init__(_eat, _drink, _thirst, _health, _hunger)
        self._voice = "Гав-Гав"

    def walk(self): return "Топ-Топ"

