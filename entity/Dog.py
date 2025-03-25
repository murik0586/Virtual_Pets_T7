from entity.Pets import Pets

#todo доделать
class Dog(Pets):
    def __init__(self, eat, drink, thirst, points_health, hunger_level):
        super().__init__(eat, drink, thirst, points_health, hunger_level, "sfasfs")
        self.__voice = "Гав-Гав"

    def get_walk(self): return "Топ-Топ"

    def set_walk(self): return