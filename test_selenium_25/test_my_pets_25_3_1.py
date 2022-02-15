import pytest
from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Строка для запуска теста
# python -m pytest -v --driver Chrome --driver-path c:/Chrome/chromedriver.exe  test_my_pets_25_3_1.py


def test_show_my_pets():
    """Проверяем, что количество питомцев из статистики пользователя соответствует отображаемым питомцам"""
    # Вводим email пользователя
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль пользователя
    pytest.driver.find_element_by_id('pass').send_keys(valid_pass)
    # Нажимаем кнопку "Войти"
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_xpath("(//div[contains(text(), 'Все питомцы наших пользователей')])")
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    WebDriverWait(pytest.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@class="nav-link" and @href="/my_pets"]'))).click()

    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))
    # Находим информацию о статистике пользователя, достаем из нее текст и разбиваем с переносом строки
    user_statistic_info = pytest.driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text.split("\n")
    # Достаем строку с индексом "1" в которой находится количество питомцев пользователя и разбиваем пробелом
    user_statistics_pets = user_statistic_info[1].split(" ")
    # Достаем из строки последний элемент в котором содержится число питомцев
    all_pets_from_statistic = int(user_statistics_pets[-1])
    # Сверяем количество питмцев отображенных на странице равно статистике
    assert len(locator_for_all_my_pets) == all_pets_from_statistic


def test_half_of_my_pets_has_photo():
    """Тест на проверку, что как минимум половина питомцев имеет фото"""
    # Вводим email пользователя
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль пользователя
    pytest.driver.find_element_by_id('pass').send_keys(valid_pass)
    # Нажимаем кнопку "Войти"
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_xpath("(//div[contains(text(), 'Все питомцы наших пользователей')])")
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    WebDriverWait(pytest.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@class="nav-link" and @href="/my_pets"]'))).click()

    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))
    # Выбираем все вебэлементы фотографий питомцев пользователя
    images = WebDriverWait(pytest.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//th/img')))
    # Назначаем новую переменную для подсчёта количества питомцев с фотографией
    number_of_pets_with_photo = 0

    # проверяем, что attribute 'src' != '', и определяем количество питомцев с фотографией
    for i in range(len(locator_for_all_my_pets)):
        if images[i].get_attribute('src') != '':
            number_of_pets_with_photo += 1
        else:
            number_of_pets_with_photo = number_of_pets_with_photo

    # Проверяем, что как минимум половина всех питомцев имеет фотографию
    assert number_of_pets_with_photo >= (len(locator_for_all_my_pets) / 2)


def test_all_my_pets_has_name_type_age():
    """Тест для проверки, что у всех питомцев есть имя, возраст и порода"""
    # Вводим email пользователя
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль пользователя
    pytest.driver.find_element_by_id('pass').send_keys(valid_pass)
    # Нажимаем кнопку "Войти"
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_xpath("(//div[contains(text(), 'Все питомцы наших пользователей')])")
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    WebDriverWait(pytest.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@class="nav-link" and @href="/my_pets"]'))).click()

    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))

    for i in range(len(locator_for_all_my_pets)):
        # для вебэлемента locator_for_all_my_pets (кнопка удаления питомца) находим все 3(три)
        # сосединие тэга "td" соответствующие имени, типу питомца и возрасту
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = WebDriverWait(pytest.driver, 5).until(EC.visibility_of(pet[2])).text
        # находим текст тэга "td" с индексом 1 соответсвующий типу питомца
        # и присваеваем переменной "animal_type"
        animal_type = WebDriverWait(pytest.driver, 5).until(EC.visibility_of(pet[1])).text
        # находим текст тэга "td" с индексом 0 соответсвующий возрасту питомца
        # и присваеваем переменной "age"
        age = WebDriverWait(pytest.driver, 5).until(EC.visibility_of(pet[0])).text
        # проверяем, что у каждого питомца есть имя, тип питомца и возраст
        assert name != ''
        assert animal_type != ''
        assert age != ''


def test_all_my_pets_has_different_names():
    """Тест на прверку, что у всех питомцев разные имена"""
    # Вводим email пользователя
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль пользователя
    pytest.driver.find_element_by_id('pass').send_keys(valid_pass)
    # Нажимаем кнопку "Войти"
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_xpath("(//div[contains(text(), 'Все питомцы наших пользователей')])")
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    WebDriverWait(pytest.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@class="nav-link" and @href="/my_pets"]'))).click()

    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))

    # Создаем пустой список для имён питомцев пользователя
    list_of_pets_names = []
    for i in range(len(locator_for_all_my_pets)):
        # для вебэлемента locator_for_all_my_pets (кнопка удаления питомца) находим все 3(три)
        # сосединие тэга "td" соответствующие имени, типу питомца и возрасту
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = WebDriverWait(pytest.driver, 5).until(EC.visibility_of(pet[2])).text
        # добавляем имя питомца в список list_of_pets_names
        list_of_pets_names.append(name)
    # для проверки уникальности имени питомца, проверяем количество вхождений каждого
    # имени в списке имён питомцев
    for name in list_of_pets_names:
        assert list_of_pets_names.count(name) == 1


def test_all_my_pets_are_unique():
    """Тест что в списке нет повторяющихся питомцев"""
    # Вводим email пользователя
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль пользователя
    pytest.driver.find_element_by_id('pass').send_keys(valid_pass)
    # Нажимаем кнопку "Войти"
    WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_xpath("(//div[contains(text(), 'Все питомцы наших пользователей')])")
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    WebDriverWait(pytest.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@class="nav-link" and @href="/my_pets"]'))).click()
    # Создаем пустой список для полного описания питомцев пользователя
    list_of_pets_with_text_description = []
    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))

    for i in range(len(locator_for_all_my_pets)):
        # для вебэлемента locator_for_all_my_pets (кнопка удаления питомца) находим все 3(три)
        # сосединие тэга "td" соответствующие имени, типу питомца и возрасту
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = WebDriverWait(pytest.driver, 5).until(EC.visibility_of(pet[2])).text
        # находим текст тэга "td" с индексом 1 соответсвующий типу питомца
        # и присваеваем переменной "animal_type"
        animal_type = WebDriverWait(pytest.driver, 5).until(EC.visibility_of(pet[1])).text
        # находим текст тэга "td" с индексом 0 соответсвующий возрасту питомца
        # и присваеваем переменной "age"
        age = WebDriverWait(pytest.driver, 5).until(EC.visibility_of(pet[0])).text
        # создаем список для переменных name, animal_type, age
        pet_list_type = [name, animal_type, age]
        # объединяем строковые переменные name, animal_type, age в одну pet_text
        pet_text = "".join(pet_list_type)
        # строковое описание питомца pet_text добавляем в список питомцев list_of_pets_with_text_description
        list_of_pets_with_text_description.append(pet_text)

    # для проверки уникальности каждого питомца, проверяем количество вхождений каждого
    # тескотового описания в списке всех питомцев
    for pet in list_of_pets_with_text_description:
        assert list_of_pets_with_text_description.count(pet) == 1
