import pytest
from entity.Pet import Pet

def test_thirst_setter_normal_value():
    pet = Pet('somename', 'somebreed') #подготовка данных
    expected_thirst = 4
    pet.thirst = 4 #акт действие так как вызываю функцию которую тестирую
    assert expected_thirst == pet.thirst #сравнение результата с ожидаемым

def test_thirst_setter_max_value():
    pet = Pet('somename', 'somebreed')
    expected_thirst = 2
    pet.thirst = 21
    assert expected_thirst == pet.thirst

def test_thirst_setter_min_value():
    pet = Pet('somename', 'somebreed')
    expected_thirst = 2
    pet.thirst = -1
    assert expected_thirst == pet.thirst