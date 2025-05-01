import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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

#<editor-fold desc="Test hunger">
def test_hunger_setter_normal_value(pet):
    """Голод корректно устанавливается в допустимом диапазоне"""
    expected_hunger = 5
    pet.state.hunger = expected_hunger
    assert expected_hunger == pet.state.hunger

def test_hunger_setter_max_value(pet):
    """Голод не должен превышать максимум"""
    expected_hunger = 10
    pet.state.hunger = 15
    assert expected_hunger == pet.state.hunger

def test_hunger_setter_min_value(pet):
    """Голод не должен быть меньше нуля"""
    expected_hunger = 0
    pet.state.hunger = -5
    assert expected_hunger == pet.state.hunger

# </editor-fold>

#<editor-fold desc="Test critical hunger">

def test_critical_hunger_reduces_health(pet):
    """Проверка уменьшения здоровья при hunger > 5"""
    print(pet.state.health)
    expected_health = 4
    pet.state.hunger = 6
    assert pet.state.health == expected_health

def test_hunger_streak_increases_penalty(pet):
    """Накопление штрафа при повторном голоде"""
    expected_health = 2
    pet.state.hunger = 6
    pet.state.hunger = 7
    assert pet.state.health == expected_health

def test_hunger_sreak_resets_decrease(pet):
    """Сброс штрафа при уменьшении голода ниже 5"""
    expected_health = 3
    pet.state.hunger = 6
    pet.state.hunger = 4
    pet.state.hunger = 6
    assert pet.state.health == expected_health

def test_critical_hunger_kills_pet(pet):
    """Питомец умирает если голод уменьшил здоровье"""
    expected_health = 0
    pet.state.hunger = 6
    pet.state.hunger = 7
    pet.state.hunger = 8
    assert pet.state.health == expected_health

# </editor-fold>
