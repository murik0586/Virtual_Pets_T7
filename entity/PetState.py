class PetState:

    STAT_LIMITS = {
        "health" : {"min" : 0, "max" : 5}, #вводится пользователем
        "happiness" : {"min" : 0, "max" : 10},
        "hunger" : {"min" : 0, "max" : 5}
    }

    def __init__(self, health: int, happiness: int = 2, hunger: int = 2):
        self._health = health
        self._happiness = happiness
        self._hunger = hunger
        self._is_alive = True

    #<editor-fold desc="Getters">
    @property
    def health(self) -> int:
        return self._health

    @property
    def happiness(self) -> int:
        return self._happiness

    @property
    def hunger(self) -> int:
        return self._hunger

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    # </editor-fold>

    #<editor-fold desc="Setters">
    @health.setter
    def health(self, value: int) -> None:
        self._health = self._clamp(value, "health")
        self._update_alive_status()

    @happiness.setter
    def happiness(self, value: int) -> None:
        self._happiness = self._clamp(value, "happiness")
        self._update_alive_status()

    @hunger.setter
    def hunger(self, value: int) -> None:
        self._hunger = self._clamp(value, "hunger")

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        self._is_alive = value

    # </editor-fold>

    def _clamp(self, value: int, stat_name: str) -> int:
        limits = self.STAT_LIMITS.get(stat_name)
        return max(limits.get('min'), min(limits.get('max'), value))

    def _update_alive_status(self) -> None:
        self._is_alive = self._health > 0 and self._happiness > 0

    def __str__(self):
        return (f"❤️Здоровье: {self._health}:\n"
                f"😊Cчастье: {self._happiness}:\n"
                f"🍗Голод: {self._hunger}")