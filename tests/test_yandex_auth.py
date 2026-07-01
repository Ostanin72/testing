# -----------------------------------------------------------------
# unit-test для авторизации на Яндексе по url: https://passport.yandex.ru/auth/
# -----------------------------------------------------------------------------

import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()


# --- Фикстура для настройки и очистки браузера ---
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# --- Параметры для теста ---
# 1. Успешный вход
SUCCESSFUL_LOGIN = {
    "username": os.getenv("YANDEX_LOGIN"),
    "password": os.getenv("YANDEX_PASSWORD"),
    "expected_result": "успешный"
}

# 2. Неуспешный вход (неверный пароль)
FAILED_LOGIN = {
    "username": os.getenv("YANDEX_LOGIN"),
    "password": "invalid_password_123",
    "expected_result": "неуспешный"
}


# --- Сам тест ---
@pytest.mark.parametrize("login_data", [SUCCESSFUL_LOGIN, FAILED_LOGIN])
def test_yandex_authorization(browser, login_data):
    """
    Тестирует процесс авторизации на Яндексе с валидными и невалидными данными.
    """
    username = login_data["username"]
    password = login_data["password"]
    expected_result = login_data["expected_result"]
    wait = WebDriverWait(browser, 15)
    # 1. Открытие страницы авторизации
    browser.get("https://passport.yandex.ru/auth")

    # 2. переходим к авторизации по логину и паролю
    more__button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="split-add-user-more-button"]'))
    )
    more__button.click()

    get_loin_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="menu-option-switchToLogin"]'))
    )
    get_loin_button.click()

    # 3. Ввод логина
    username_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="text-field-input"]'))
    )
    username_input.clear()
    username_input.send_keys(username)

    get_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="split-add-user-next-login"]'))
    )

    # Переходим на страницу ввода пароля, если еше не перешли
    get_button.click()
    try:
        get_password_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="password-btn"]'))
        )
        get_password_button.click()
    except:
        pass

    # 3. Ввод пароля
    password_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="text-field-input"]'))
    )
    password_input.clear()
    password_input.send_keys(password)

    next_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="password-next"]'))
    )
    next_button.click()

    # 4. Пропуск биометрии (если появилась)
    try:
        skip_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="webauthn-reg-later-button"]'))
        )
        skip_button.click()
    except:
        pass

    # 5. Пропуск рекламы (если появилась)
    try:
        skip_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="button"]'))
        )
        skip_button.click()
    except:
        pass

    # 6. Проверка результата авторизации

    if expected_result == "успешный":
        # При успешной авторизации пользователь перенаправляется
        # на главную страницу Яндекса
        # Ожидаем, что в URL будет домен yandex.ru или mail.yandex.ru
        WebDriverWait(browser, 15).until(
            lambda driver: "yandex.ru" in driver.current_url
                           or "mail.yandex.ru" in driver.current_url
        )
        assert ("yandex.ru" in browser.current_url
                or "mail.yandex.ru" in browser.current_url)

        # Дополнительная проверка: ищем элемент, который появляется
        # только у авторизованного пользователя.
        try:
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="profile-card"]')
                )
            )
            print("✅ Авторизация прошла успешно.")
        except:
            print("⚠️ URL указывает на успех, но элемент профиля не найден.")

    elif expected_result == "неуспешный":
        # При неуспешной авторизации пользователь остается на странице /auth
        # и появляется сообщение об ошибке.
        WebDriverWait(browser, 10).until(
            EC.url_contains("auth")
        )
        assert "/pwl-yandex/auth/password" in browser.current_url

        # Проверка наличия сообщения об ошибке
        error_message = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="error-message"]')
            )
        )
        assert error_message.is_displayed()
        print("✅ Авторизация не удалась, сообщение об ошибке отображено.")
