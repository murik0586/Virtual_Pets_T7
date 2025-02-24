import abc

class Pet(abc.ABC):
    _eat = ""
    _drink = ""
    _voice = ""
    _thirst = 0.0
    _health = 0
    _hunger = 0.0

    def __init__(self, _eat, _drink, _voice, _thirst, _health, _hunger):
        self._eat = _eat
        self._drink = _drink
        self._voice = _voice
        self._thirst = _thirst
        self._health = _health
        self._hunger = _hunger

    @abc.abstractmethod
    def eat(self): pass

    @abc.abstractmethod
    def drink(self): pass

    @abc.abstractmethod
    def voice(self): pass

class Cat(Pet):
    def __init__(self, _eat, _drink, _voice, _thirst, _health, _hunger):
        super().__init__(_eat, _drink, _voice, _thirst, _health, _hunger)

        def eat(self): return "Хрум-Хрум"
        def drink(self): return "Хлюп-Хлюп"
        def voice(self): return "Мяу-Мяу"

        def walk(self): return "Топ-Топ"

class Dog(Pet):
    def __init__(self, _eat, _drink, _voice, _thirst, _health, _hunger):
        super().__init__(_eat, _drink, _voice, _thirst, _health, _hunger)

        def eat(self): return "Хрум-Хрум"
        def drink(self): return "Хлюп-Хлюп"
        def voice(self): return "Гав-Гав"

        def walk(self): return "Топ-Топ"
