class PetState:

    BASE_LIMITS = {
        "happiness" : {"min" : 0, "max" : 10},
        "hunger" : {"min" : 0, "max" : 10}
    }

    def __init__(self, health: int, happiness: int = 2, hunger: int = 2):
        self._limits = {"health": {"min": 0, "max": health}, **self.BASE_LIMITS}
        self._health = self._clamp(health, "health")
        self._happiness = self._clamp(happiness, "happiness")
        self._hunger = self._clamp(hunger, "hunger")
        self._is_alive = True
        self._health_decrease_streak = 0
        self._hungry_penalty = 5
        self._was_hunger_critical = False

    #<editor-fold desc="Getters">
    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._limits["health"]["max"]

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
        previous_value = self._hunger
        self._hunger = self._clamp(value, "hunger")

        if self._is_hunger_critical():
            if previous_value <= self._hungry_penalty:
                self._reset_hunger_decrease_streak()
            self._apply_hunger_damage()
            self._was_hunger_critical = True
        elif self._was_hunger_critical and value < previous_value:
            self._reset_hunger_decrease_streak()
            self._was_hunger_critical = False

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        self._is_alive = value

    # </editor-fold>

    def _clamp(self, value: int, stat_name: str) -> int:
        limits = self._limits.get(stat_name, {"min": 0, "max": value})
        return max(limits["min"], min(limits["max"], value))

    def _update_alive_status(self) -> None:
        self._is_alive = self._health > 0 and self._happiness > 0

    def _is_hunger_critical(self) -> bool:
        return self._hunger > self._hungry_penalty

    def _apply_hunger_damage(self) -> None:
        self._health_decrease_streak += 1
        self.health -= self._health_decrease_streak

    def _reset_hunger_decrease_streak(self) -> None:
        self._health_decrease_streak = 0

    def __str__(self):
        status = "жив" if self.is_alive else "мёртв"
        return (f"❤️ Здоровье: {self._health}/{self.max_health}\n"
                f"😊 Счастье: {self._happiness}/{self._limits['happiness']['max']}\n"
                f"🍗 Голод: {self._hunger}/{self._limits['hunger']['max']}\n"
                f"Состояние: {status}")