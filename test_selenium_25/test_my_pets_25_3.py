import pytest
from config import *

# Строка для запуска теста
# python -m pytest -v --driver Chrome --driver-path c:/Chrome/chromedriver.exe  test_my_pets_25_3.py


def test_show_my_pets():
    # Настраиваем неявные ожидания
    pytest.driver.implicitly_wait(10)

    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_pass)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_xpath("(//div[contains(text(), 'Все питомцы наших пользователей')])")
    # Находим все вебэлементы соответсвующие фотографиям питомцев
    images = pytest.driver.find_elements_by_css_selector('.card-img-top')
    # Находим все вебэлементы соответсвующие именам питомцев
    names = pytest.driver.find_elements_by_css_selector('.card-title')
    # Находим все вебэлементы соответсвующие виду и возрасту питомцев
    descriptions = pytest.driver.find_elements_by_css_selector('.card-text')

    for i in range(len(names)):
        # Проверяем, что у питомцев есть фотография
        # (на этом месте тест падает, т.к. не у всех питомцев есть фото)
        assert images[i].get_attribute('src') != ''
        # Проверяем, что у питомцев есть имя
        assert names[i].text != ''
        # Проверяем, что у питомцев есть порода и возраст
        assert descriptions[i].text != ''
        # Чтобы убедиться, что у питомцев есть и порода и возраст, ищем в тексте этого элемента
        # запятую,как разделитель между этими сущностями
        assert ', ' in descriptions[i].text
        # Разделяем строку по запятой
        parts = descriptions[i].text.split(", ")
        # Проверяем, что в каждой части разделеного текста присутствуют символы
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
