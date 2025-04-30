import pytest
from entity.Pet import Pet

def test_thirst_setter_normal_value(): #Здесь хорошо, ты проверил что значение устанавливает в пределах
    pet = Pet('somename', 10) # подготовка данных
    expected_thirst = 5
    pet.thirst = 4 # акт действие так как вызываю функцию которую тестирую
    assert expected_thirst == pet.thirst # сравнение результата с ожидаемым

def test_thirst_setter_max_value(): #здесь главное
    pet = Pet('somename', 10)
    expected_thirst = 10
    pet.thirst = 21
    assert expected_thirst == pet.thirst

def test_thirst_setter_min_value():
    pet = Pet('somename', 10)
    expected_thirst = 0
    pet.thirst = -1

    assert expected_thirst == pet.thirst