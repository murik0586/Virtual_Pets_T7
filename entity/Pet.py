from entity.PetState import PetState

class Pet():
    ##todo ДЛЯ ВСЕХ, я добавлю описание всего что я сделал, в случае несостыковки логики - дайте знать, исправлю!
    type_of_pet = "Питомец" #Это поле для красивого отображения в __str__ - стр это аналог toString() из java
    def __init__(self, name: str, health: int = 5):  # Конструктор
        self.__name = name  # кличка
        self.state = PetState(health)
        # todo по заданию, задается при создании, но если сделать большое кол очков
        # то получиться так, что тестить долго в первое время, потому, максимальное значение хп
        # будет зависеть от животного

    ##Геттеры Мурат
    @property  # Это сигнатура для геттера!
    def name(self):
        return self.__name  # Геттеры возвращают просто значение полей(свойств)

    ##Сеттеры Мурат
    @name.setter  # Сигнатура для сеттера
    def name(self, name: str):
        if len(name) <= 2:  # Условие, что нельзя имя дать меньше по длине
            print("Никнейм(Кличка) должен быть от двух символов")
            return
        else:
            self.__name = name

    '''@health.setter
    def health(self, health: int):
        if health < 0:  # не даем установить здоровье меньше нуля или 0(по логике тогда питомец должен исчезнуть)
            health = 0
            print("Обойдемся только положительными числами и больше 0!")
        self.__health = health
        if health <= 0:
            print("Питомец умер от голода! 💀")

    @happiness.setter
    def happiness(self, happiness: int):
        if happiness <= 0:
            print("Обойдемся только положительными числами и больше 0!")
            return
        elif happiness > 20:
            self.__happiness = 20  # Спецом устанавливаем в таком случае максимальный уровень счастья, и не даем выйти за пределы
            print("Максимальный уровень счастья достигнут!")
            return
        self.__happiness = happiness

    @hunger.setter
    def hunger(self, hunger: int):
        if hunger <= 0:
            print("Обойдемся только положительными числами и больше 0!")
            return
        elif hunger > 5:
            self.__health -= self.__hunger_penalty  # Отнимаем текущий штраф
            self.__hunger = hunger
            #points_health = self.__points_health - 1  Не нужно т.к. уже отняли
            print(f"Критичный уровень голода! -{self.__hunger_penalty}hp, здоровье: {self.__health}")
            self.__hunger_penalty += 1  # Увеличиваем штраф для следующего раза
        else:
            self.__hunger_penalty = 1 # Если голод <= 5 — сбрасываем штраф (питомец поел)
            #return
        self.__hunger = hunger #Назначение в любом случае кроме того когда hunger_level <= 0

    # TODO определимся в дальнейшем: нам создать пользователя и который будет иметь свои методы
    #  а у животного будут методы "пить, есть и т.д которые вызываются в методах юзера"
    #  или же оставим их тут, щас я не думаю что это критично,

    # todo конечно же это может отличаться у каждого животного'''

    def feed(self):
        # todo Игорь
        """покормить питомца.
        -2 к голоду"""
        if not self.state.is_alive:
            return
        self.state.hunger -= 2

    def stroke(self):
        """погладить питомца.
        + 1 к счастью, +1 к голоду"""
        if not self.state.is_alive:
            return
        self.state.happiness += 1
        self.state.hunger += 1

    def give_treat(self):
        """дать вкусняшку питомцу.
        +2 к счастью,- 1 к голоду"""
        self.state.happiness += 2
        self.state.hunger -= 1

    def walk(self):
        """погулять с питомцем.
        + 1 к счастью, + 3 к голоду +2 к жажде"""
        print(f"{self.name} идет на прогулку!")
        self.state.happiness += 1
        self.state.hunger += 3

    def ignore(self):
        """игнорировать питомца.
        -1 к счастью, + 1 к голоду"""
        self.state.happiness -= 1
        self.state.hunger += 1

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"{self.state}")