class Pet():
    ##todo ДЛЯ ВСЕХ, я добавлю описание всего что я сделал, в случае несостыковки логики - дайте знать, исправлю!
    type_of_pet = "Питомец" #Это поле для красивого отображения в __str__ - стр это аналог toString() из java
    def __init__(self, name: str, health: int, voice: str = "Фьють-фьють!",
                 happiness: int = 2,
                 hunger: int = 2, thirst: int = 2):  # Конструктор
        """Инициализирует питомца.
        :param name: Кличка питомца
        :param thirst: Уровень жажды(0 - 20)
        :param health: Очки здоровья
        :param happiness: Уровень счастья(по умолчанию 2)
        :param hunger: Уровень голода(по умолчанию 2)
        :param voice: Голос питомца
        """
        self.__name = name  # кличка
        self.__thirst = thirst  # Жажда
        self.__health = health  # Очки здоровья
        # todo по заданию, задается при создании, но если сделать большое кол очков
        # то получиться так, что тестить долго в первое время, потому, максимальное значение хп
        # будет зависеть от животного
        self.__happiness = happiness
        self.__hunger = hunger  # Голод
        self.__hunger_penalty = 1  # Переменная для хранения штрафа за отнимание жизней
        self.__voice = voice  # Голос животного
        self.__life = True # Жизнь питомца

    ##Геттеры Мурат
    @property  # Это сигнатура для геттера!
    def name(self):
        return self.__name  # Геттеры возвращают просто значение полей(свойств)

    @property
    def thirst(self):
        return self.__thirst

    @property
    def health(self):
        return self.__health

    @property
    def happiness(self):
        return self.__happiness

    @property
    def hunger(self):
        return self.__hunger

    @property
    def voice(self):
        return self.__voice
    
    @property
    def life(self):
        """Возвращает статус жизни питомца (True/False)."""
        return self.__life

    ##Сеттеры Мурат
    @name.setter  # Сигнатура для сеттера
    def name(self, name: str):
        if len(name) <= 2:  # Условие, что нельзя имя дать меньше по длине
            print("Никнейм(Кличка) должен быть от двух символов")
            return
        else:
            self.__name = name

    @thirst.setter
    def thirst(self, thirst: int):
        if thirst > 20:
            print("Стоп! Это критический уровень жажды!")
            return
        elif thirst < 0:
            print("Обойдемся только положительными числами!")
            return
        self.__thirst = thirst

    @health.setter
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

    # todo конечно же это может отличаться у каждого животного

    def water(self):
        """Уменьшает уровень жажды на 2, но не ниже 0."""
        self.thirst = max(0, self.thirst - 2) # Берет максимальное значение

    def feed(self):
        # todo Игорь
        """покормить питомца.
        -2 к голоду + 1 к жажде"""
        self.hunger = max(0, self.hunger - 2)
        self.thirst += 1

    def stroke(self):
        """погладить питомца.
        + 1 к счастью, +1 к голоду"""
        pass

    def give_treat(self):
        """дать вкусняшку питомцу.
        +2 к счастью,- 1 к голоду"""
        self.happiness += 2
        self.hunger = max(0, self.hunger - 1)

    def walk(self):
        """погулять с питомцем.
        + 1 к счастью, + 3 к голоду +2 к жажде"""
        print(f"{self.name} идет на прогулку!")
        self.happiness += 1
        self.hunger += 3
        self.thirst += 2

        # Проверка на исчезновение питомца
        if self.happiness <= 0 or self.health <= 0:
            print(f"{self.nickname} исчез! ")
            self.__life = False

    def ignore(self):
        """игнорировать питомца.
        -1 к счастью, + 1 к голоду"""
        pass

    def __str__(self):
            return (f"{self.type_of_pet}: \n"
                    f"Кличка: {self.__name}\n"
                    f"❤️Здоровье: {self.__health}:\n"
                    f"😊Cчастье: {self.__happiness}:\n"
                    f"🍗Голод: {self.__hunger}:\n"
                    f"💧 Жажда: {self.thirst}:\n"
                    f"🔊Голос: {self.__voice}")
