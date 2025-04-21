import pytest
from entity.Cat import Cat

def test_thirst_setter_normal_value():
    cat = Cat('somename', 'somebreed') #подготовка данных
    expected_thirst = 4
    cat.thirst = 4 #акт действие так как вызываю функцию которую тестирую
    assert expected_thirst == cat.thirst #сравнение результата с ожидаемым

def test_thirst_setter_max_value():
    cat = Cat('somename', 'somebreed')
    expected_thirst = 2
    cat.thirst = 21
    assert expected_thirst == cat.thirst

def test_thirst_setter_min_value():
    cat = Cat('somename', 'somebreed')
    expected_thirst = 2
    cat.thirst = -1
    assert expected_thirst == cat.thirst

    ### some