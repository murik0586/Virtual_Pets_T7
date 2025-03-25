from entity.Pets import Pets

#todo доделать
class Cat(Pets):
    def __init__(self, eat, drink, thirst, points_health, hunger_level, voice):
        super().__init__(eat, drink, thirst, points_health, hunger_level, voice)
        self.__voice = "Мяу-Мяу"

    def get_walk(self): return "Топ-Топ"

    def set_walk(self): return
