import Pet
import Dog
import Cat

class PetFactory:
    @staticmethod
    def create_pet(pet_type: str) -> Pet:
        pets = {
            'dog': Dog,
            'cat': Cat
        }

        if pet_type not in pets:
            raise ValueError(f'Unknown pet type: {pet_type}')

        return pets[pet_type]()