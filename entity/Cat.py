from entity.Pets import Pet


class Cat(Pet):
    def __init__(self, eat, drink, thirst, health, hunger, voice):
        super().__init__(eat, drink, thirst, health, hunger, voice)
        self.__voice = "Мяу-Мяу"

    def get_walk(self): return "Топ-Топ"

    def set_walk(self): return
