import pytest
from entity.PetState import PetState

@pytest.fixture
def pet_state():
    return PetState(health = 10, happiness = 5, hunger = 5)

#<editor-fold desc="Test clamp function">

def test_clamp_value_limits(pet_state):
    """Тестируем значения внутри диапозоно"""
    expected_health = 5
    assert pet_state._clamp(5, "health") == expected_health
    expected_happiness = 3
    assert pet_state._clamp(3, "happiness") == expected_happiness
    expected_hunger = 7
    assert pet_state._clamp(7, "hunger") == expected_hunger

def test_clamp_value_min(pet_state):
    """Все статы имеют значение 0"""
    expected_health = 0
    assert pet_state._clamp(-5, "health") == expected_health
    expected_happiness = 0
    assert pet_state._clamp(-3, "happiness") == expected_happiness
    expected_hunger = 0
    assert pet_state._clamp(-7, "hunger") == expected_hunger

def test_clamp_value_max(pet_state):
    """Все статы имеют значение 0"""
    expected_health = 0
    assert pet_state._clamp(-5, "health") == expected_health
    expected_happiness = 0
    assert pet_state._clamp(-3, "happiness") == expected_happiness
    expected_hunger = 0
    assert pet_state._clamp(-7, "hunger") == expected_hunger

def test_clamp_boundary_values(pet_state):
    """Проверка граничных значений"""
    assert pet_state._clamp(0, "health") == 0
    assert pet_state._clamp(10, "health") == 10
    assert pet_state._clamp(0, "happiness") == 0
    assert pet_state._clamp(10, "happiness") == 10

def test_clamp_unknown_stat(pet_state):
    """Передаем неизвестный стат. Для неизвестного стата должен использоваться переданный максимум"""
    assert pet_state._clamp(5, "unknown_stat") == 5
    assert pet_state._clamp(-5, "unknown_stat") == 0
    assert pet_state._clamp(15, "unknown_stat") == 15

# </editor-fold>