import pytest
from entity.Pet import Pet

@pytest.fixture
def alive_pet():
    return Pet(name = "alivepet", health = 10)

@pytest.fixture
def dead_pet():
    pet = Pet(name = "deadpet", health = 1)
    pet.state.health = 0
    return pet

def test_pet_initialization(alive_pet):
    assert alive_pet.name == "alivepet"
    assert alive_pet.state.health == 10
    assert alive_pet.state.is_alive is True

def test_feed_reduces_hunger(alive_pet):
    alive_pet.state.hunger = 5
    alive_pet.feed()
    assert alive_pet.state.hunger == 3

def test_stroke_increases_happiness_and_hunger(alive_pet):
    initial_happy = alive_pet.state.happiness
    initial_hunger = alive_pet.state.hunger
    alive_pet.stroke()
    assert alive_pet.state.happiness == initial_happy + 1
    assert alive_pet.state.hunger == initial_hunger + 1

def test_give_treat_effects(alive_pet):
    alive_pet.give_treat()
    assert alive_pet.state.happiness == 4
    assert alive_pet.state.hunger == 1

def test_hunger_never_negative(alive_pet):
    alive_pet.state.hunger = 1
    alive_pet.feed()
    assert alive_pet.state.hunger == 0

def test_max_happiness(alive_pet):
    alive_pet.state.happiness = 9
    alive_pet.give_treat()
    assert alive_pet.state.happiness == 10

def test_dead_pet_actions(dead_pet, capsys):
    dead_pet.feed()
    captured = capsys.readouterr()
    assert dead_pet.state.hunger == 2

def test_str_dead_pet(dead_pet):
    assert "умер :(" in str(dead_pet)

def test_name_validation_too_short(capsys):
    pet = Pet(name = "А", health = 5)
    captured = capsys.readouterr()
    assert "" in captured.out

def test_name_validation_correct():
    pet = Pet(name = "Аз", health = 5)
    pet.name = "НовоеИмя"
    assert pet.name == "НовоеИмя"