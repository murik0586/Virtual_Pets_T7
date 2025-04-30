from entity.Pet import Pet
from typing import Optional

class PetManager:
    def __init__(self):
        self._pets = {}  # {id: Pet}
        self._next_id = 1

    @property
    def pets(self) -> dict[int, 'Pet']:
        return self._pets.copy()

    def create_pet(self, name: str, health: int) -> int:
        """Создает питомца и возвращает его ID"""
        pet_id = self._next_id
        self._pets[pet_id] = Pet(name, health)
        self._next_id += 1
        return pet_id

    def get_pet(self, pet_id: int) -> Optional[Pet]:
        return self._pets.get(pet_id)

    def remove_pet(self, pet_id: int) -> bool:
        return self._pets.pop(pet_id, None) is not None

    def get_alive_pets(self) -> dict[int, 'Pet']:
        return {id_: p for id_, p in self._pets.items() if p.state.is_alive}