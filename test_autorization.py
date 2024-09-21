import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()  # или другой браузерный драйвер
    driver.get("https://b2c.passport.rt.ru/")
    yield driver
    driver.quit()

# заголовок страницы содержит "Ростелеком"
def test_page_title(driver):
    assert "Ростелеком" in driver.title

# форма для входа на страницу присутствует
def test_login_form_present(driver):
    login_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-login"))
    )
    assert login_form is not None

# появляется сообщение об ошибке при попытке входа с пустыми полями логина и пароля.
def test_login_with_empty_credentials(driver):
    login_button = driver.find_element(By.ID, "t-btn-tab-login")
    login_button.click()

    submit_button = driver.find_element(By.ID, "kc-login")
    submit_button.click()

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rt-input-container__meta--error"))
    )
    assert error_message is not None
    assert "Введите логин и пароль" in error_message.text

# при нажатии на ссылку восстановления пароля открывается соответствующая страница
def test_password_recovery_link(driver):
    recovery_link = driver.find_element(By.ID, "forgot_password")
    recovery_link.click()

    recovery_page_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Восстановление пароля" in recovery_page_heading.text

# при нажатии на ссылку регистрации открывается соответствующая страница
def test_registration_link(driver):
    registration_link = driver.find_element(By.ID, "kc-register")
    registration_link.click()

    registration_page_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Регистрация" in registration_page_heading.text

# вкладка для входа по номеру телефона присутствует.
def test_phone_tab_present(driver):
    phone_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-phone"))
    )
    assert phone_tab is not None

# вкладка для входа по email присутствует
def test_email_tab_present(driver):
    email_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "t-btn-tab-mail"))
    )
    assert email_tab is not None

# при вводе неверных учетных данных появляется сообщение об ошибке "Неверный логин или пароль"
def test_login_with_invalid_credentials(driver):
    login_button = driver.find_element(By.ID, "t-btn-tab-login")
    login_button.click()

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "kc-login")

    username_field.send_keys("invalid_user")
    password_field.send_keys("invalid_pass")
    submit_button.click()

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rt-input-container__meta--error"))
    )
    assert "Неверный логин или пароль" in error_message.text

# чекбокс "Запомнить меня" присутствует, может быть выбран и остается выбранным
def test_remember_me_checkbox(driver):
    login_button = driver.find_element(By.ID, "t-btn-tab-login")
    login_button.click()

    remember_me_checkbox = driver.find_element(By.ID, "t-remember-me")
    assert remember_me_checkbox is not None
    remember_me_checkbox.click()
    assert remember_me_checkbox.is_selected()

# наличие ссылок на социальные сети и подтверждает, что все
# ожидаемые платформы (vk, ok, mail, google, yandex) имеют ссылки
def test_social_media_links_present(driver):
    social_media_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".social-icon"))
    )
    assert len(social_media_links) > 0

    expected_social_media_platforms = ['vk', 'ok', 'mail', 'google', 'yandex']
    for platform in expected_social_media_platforms:
        link = driver.find_element(By.CLASS_NAME, f"social-icon-{platform}")
        assert link is not None