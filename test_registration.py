import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()  # Используйте соответствующий драйвер для вашего браузера
    driver.get(
        "https://b2c.passport.rt.ru/")
    yield driver
    driver.quit()

# Заголовок страницы регистрации содержит "Ростелеком"
def test_registration_page_title(driver):
    assert "Ростелеком" in driver.title

# форма регистрации присутствует на странице
def test_registration_form_present(driver):
    registration_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "kc-register"))
    )
    assert registration_form is not None

# кнопка для отправки формы регистрации присутствует
def test_submit_button_present(driver):
    submit_button = driver.find_element(By.ID, "kc-register")
    assert submit_button is not None

# все обязательные поля формы регистрации помечены как обязательные
def test_required_fields(driver):
    required_fields = ["firstName", "lastName", "email", "password", "password-confirm"]
    for field in required_fields:
        field_element = driver.find_element(By.ID, field)
        assert field_element.get_attribute("required") == "true"

# при несовпадении паролей отображается соответствующее сообщение об ошибке
def test_password_confirmation_mismatch(driver):
    first_name = driver.find_element(By.ID, "firstName")
    last_name = driver.find_element(By.ID, "lastName")
    email = driver.find_element(By.ID, "email")
    password = driver.find_element(By.ID, "password")
    password_confirm = driver.find_element(By.ID, "password-confirm")
    submit_button = driver.find_element(By.ID, "kc-register")

    first_name.send_keys("Катя")
    last_name.send_keys("Катюша")
    email.send_keys("ekateryna20182018@gmail.com")
    password.send_keys("Kate1234")
    password_confirm.send_keys("password124")
    submit_button.click()

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rt-input-container__meta--error"))
    )
    assert "Пароли не совпадают" in error_message.text

# при отправке формы с пустыми обязательными полями отображаются ошибки для всех обязательных полей
def test_empty_fields_error(driver):
    submit_button = driver.find_element(By.ID, "kc-register")
    submit_button.click()

    error_messages = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "rt-input-container__meta--error"))
    )
    assert len(error_messages) == 5  # Ожидаем ошибки для всех обязательных полей

# при вводе некорректного email отображается соответствующее сообщение об ошибке
def test_email_field_validation(driver):
    email = driver.find_element(By.ID, "email")
    email.clear()
    email.send_keys("invalid-email")
    email.send_keys(Keys.TAB)

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rt-input-container__meta--error"))
    )
    assert "Введите корректный адрес электронной почты" in error_message.text

# при вводе слишком короткого пароля отображается соответствующее сообщение об ошибке
def test_password_strength(driver):
    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("123")
    password.send_keys(Keys.TAB)

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rt-input-container__meta--error"))
    )
    assert "Пароль слишком короткий" in error_message.text

# успешная регистрацию пользователя с корректными данными (предполагается,
# что этот тест будет выполняться на тестовом окружении, чтобы избежать создания реальных пользователей)
def test_successful_registration(driver):
    first_name = driver.find_element(By.ID, "firstName")
    last_name = driver.find_element(By.ID, "lastName")
    email = driver.find_element(By.ID, "email")
    password = driver.find_element(By.ID, "password")
    password_confirm = driver.find_element(By.ID, "password-confirm")
    submit_button = driver.find_element(By.ID, "kc-register")

    first_name.clear()
    first_name.send_keys("Катя")
    last_name.clear()
    last_name.send_keys("Катюша")
    email.clear()
    email.send_keys("ekateryna20182018@gmail.com")
    password.clear()
    password.send_keys("Kate1234")
    password_confirm.clear()
    password_confirm.send_keys("Kate1234")
    submit_button.click()

    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert "Регистрация прошла успешно" in success_message.text

# ссылка на пользовательское соглашение работает и открывает новое окно с соответствующей страницей
def test_terms_and_conditions_link(driver):
    terms_link = driver.find_element(By.LINK_TEXT, "Пользовательское соглашение")
    terms_link.click()

    WebDriverWait(driver, 10).until(
        EC.number_of_windows_to_be(2)
    )
    driver.switch_to.window(driver.window_handles[1])

    terms_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Пользовательское соглашение" in terms_heading.text
    driver.close()
    driver.switch_to.window(driver.window_handles[0])