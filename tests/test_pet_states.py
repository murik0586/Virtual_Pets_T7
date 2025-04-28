import pytest
from entity.Pet import Pet

@pytest.fixture()
def pet():
    """Фикстура для создания питомца"""
    return Pet("somename", 5)

#<editor-fold desc="Test health">

def test_health_setter_normal_value(pet):
    """Здоровье корректно устанавливается в допустимом диапозоне"""
    expected_health = 5
    pet.state.health = expected_health
    assert expected_health == pet.state.health

def test_health_setter_max_value(pet):
    """Здоровье не должно превышать максимум"""
    expected_health = 5
    pet.state.health = 21
    assert expected_health == pet.state.health

def test_health_setter_min_value(pet):
    """Здоровье не должно быть меньше нуля"""
    expected_health = 0
    pet.state.health = -5
    assert expected_health == pet.state.health

def test_health_setter_zero_value_is_alive_false(pet):
    """Питомец должен умереть при нулевом здоровье"""
    pet.state.health = 0
    assert not pet.state.is_alive

# </editor-fold>

#<editor-fold desc="Test happiness">

def test_happiness_setter_normal_value(pet):
    """Счастье корректно устанавливается в допустимом диапозоне"""
    expected_happiness = 7
    pet.state.happiness = 7
    assert expected_happiness == pet.state.happiness

def test_happiness_setter_max_value(pet):
    """Счастье не должно превышать максимум"""
    expected_happiness = 10
    pet.state.happiness = 15
    assert expected_happiness == pet.state.happiness

def test_happiness_setter_min_value(pet):
    """Счастье не должно быть меньше нуля"""
    expected_happiness = 0
    pet.state.happiness = -5
    assert expected_happiness == pet.state.happiness

def test_happiness_setter_zero_value_is_alive_false(pet):
    """Питомец должен умереть при нулевом счастье"""
    pet.state.happiness = 0
    assert not pet.state.is_alive

def test_happiness_setter_max_value_is_alive_false(pet):
    """Питомец остается жив при счастье выше нуля"""
    pet.state.happiness = 20
    assert pet.state.is_alive

# </editor-fold>

#<editor-fold desc="Test hungry>

# </editor-fold>