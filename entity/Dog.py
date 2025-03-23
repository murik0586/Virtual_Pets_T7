from entity.Pets import Pet


class Dog(Pet):
    def __init__(self, eat, drink, thirst, health, hunger):
        super().__init__(eat, drink, thirst, health, hunger, "sfasfs")
        self.__voice = "Гав-Гав"

    def get_walk(self): return "Топ-Топ"

    def set_walk(self): return