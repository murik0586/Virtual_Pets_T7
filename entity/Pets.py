import abc


class Pets(abc.ABC):
    ##todo ДЛЯ ВСЕХ, я добавлю описание всего что я сделал, в случае несостыковки логики - дайте знать, исправлю!
    type_of_pet = "Питомец" #Это поле для красивого отображения в __str__ - стр это аналог toString() из java
    def __init__(self, nickname: str, points_health: int, voice: str = "Это абстрактный класс",
                 happiness_indicator: int = 2,
                 hunger_level: int = 2, thirst: int = 2):  # Конструктор
        """Инициализирует питомца.
        :param nickname: Кличка питомца
        :param thirst: Уровень жажды(0 - 20)
        :param points_health: Очки здоровья
        :param happiness_indicator: Уровень счастья(по умолчанию 2)
        :param hunger_level: Уровень голода(по умолчанию 2)
        :param voice: Голос питомца
        """
        self.__nickname = nickname  # кличка
        self.__thirst = thirst  # Жажда
        self.__points_health = points_health  # Очки здоровья
        # todo по заданию, задается при создании, но если сделать большое кол очков
        # то получиться так, что тестить долго в первое время, потому, максимальное значение хп
        # будет зависеть от животного
        self.__happiness_indicator = happiness_indicator
        self.__hunger_level = hunger_level  # Голод
        self.__voice = voice  # Голос животного

    ##Геттеры Мурат
    @property  # Это сигнатура для геттера!
    def nickname(self):
        return self.__nickname  # Геттеры возвращают просто значение полей(свойств)

    @property
    def thirst(self):
        return self.__thirst

    @property
    def points_health(self):
        return self.__points_health

    @property
    def happiness_indicator(self):
        return self.__happiness_indicator

    @property
    def hunger_level(self):
        return self.__hunger_level

    @property
    def voice(self):
        return self.__voice

    ##Сеттеры Мурат
    @nickname.setter  # Сигнатура для сеттера
    def nickname(self, nickname: str):
        if len(nickname) <= 2:  # Условие, что нельзя имя дать меньше по длине
            print("Никнейм(Кличка) должен быть от двух символов")
            return

        else:
            self.__nickname = nickname

    @thirst.setter
    def thirst(self, thirst: int):
        if thirst > 20:
            print("Стоп! Это критический уровень жажды!")
            return
        elif thirst < 0:
            print("Обойдемся только положительными числами!")
            return
        self.__thirst = thirst

    @points_health.setter
    def points_health(self, points_health: int):
        if points_health <= 0:  # не даем установить здоровье меньше нуля или 0(по логике тогда питомец должен исчезнуть)
            print("Обойдемся только положительными числами и больше 0!")
            return
        self.__points_health = points_health

    @happiness_indicator.setter
    def happiness_indicator(self, happiness_indicator: int):
        if happiness_indicator <= 0:
            print("Обойдемся только положительными числами и больше 0!")
            return
        elif happiness_indicator > 20:
            self.__happiness_indicator = 20  # Спецом устанавливаем в таком случае максимальный уровень счастья, и не даем выйти за пределы
            print("Максимальный уровень счастья достигнут!")
            return
        self.__happiness_indicator = happiness_indicator

    @hunger_level.setter
    def hunger_level(self, hunger_level: int):
        if hunger_level <= 0:
            print("Обойдемся только положительными числами и больше 0!")
            return
        elif hunger_level > 5:
            self.__points_health -= 1
            self.__hunger_level = hunger_level
            points_health = self.__points_health - 1  # Уменьшаем хп
            print(f"Критичный уровень голода! - 1hp, здоровье питомца {points_health}")
            return
        self.__hunger_level = hunger_level

    # Методы абстрактные
    # TODO определимся в дальнейшем: нам создать пользователя и который будет иметь свои методы
    #  а у животного будут методы "пить, есть и т.д которые вызываются в методах юзера"
    #  или же оставим их тут, щас я не думаю что это критично,

    # todo конечно же это может отличаться у каждого животного

    @abc.abstractmethod
    def give_water(self):
        """Абстрактный метод: напоить питомца
        Если напоить (- 2) """
        pass

    @abc.abstractmethod
    def feed(self):
        # todo Игорь
        """Абстрактный метод: покормить питомца.
        -2 к голоду + 1 к жажде"""
        pass

    @abc.abstractmethod
    def pet(self):
        """Абстрактный метод: погладить питомца.
        + 1 к счастью, +1 к голоду"""
        pass

    @abc.abstractmethod
    def give_treat(self):

        """Абстрактный метод: дать вкусняшку питомцу.
        +2 к счастью,- 1 к голоду"""
        pass

    @abc.abstractmethod
    def walk(self):
        """Абстрактный метод: погулять с питомцем.
        + 1 к счастью, + 3 к голоду +2 к жажде"""
        pass

    @abc.abstractmethod
    def ignore(self):
        """Абстрактный метод: игнорировать питомца.
        -1 к счастью, + 1 к голоду"""
        pass

    def __str__(self):
            return (f"{self.type_of_pet}: \n"
                    f"Кличка: {self.__nickname}\n"
                    f"❤️Здоровье: {self.__points_health}:\n"
                    f"😊Cчастье: {self.__happiness_indicator}:\n"
                    f"🍗Голод: {self.__hunger_level}:\n"
                    f"💧 Жажда: {self.thirst}:\n"
                    f"🔊Голос: {self.__voice}")
