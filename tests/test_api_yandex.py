from uuid import uuid4

import pytest
import requests
from dotenv import load_dotenv
from os import getenv


BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"


@pytest.fixture
def token():
    load_dotenv()
    token = getenv("TOKEN")

    if not token:
        pytest.fail("YANDEX_TOKEN не установлен в переменных окружения")
    return token

@pytest.fixture
def headers(token):
    return {
        'Authorization': f'OAuth {token}'
    }

@pytest.fixture
def temp_folder():
    """Генерирует уникальное имя папки"""
    return f"test-folder-{uuid4()}"

@pytest.fixture
def create_and_cleanup_folder(headers, temp_folder):
    """Создаёт папку и удаляет её после теста"""
    folder_path = f"disk:/{temp_folder}"
    # Создание
    response = requests.put(BASE_URL, headers=headers, params={'path': folder_path})
    assert response.status_code in [201, 409], f"Ошибка при создании: {response.text}"

    yield temp_folder  # передаём управление в тест

    # Удаление после теста
    requests.delete(BASE_URL, headers=headers, params={'path': folder_path, 'permanently': 'true'})


# Тест на попытку авторизоваться без токена
def test_create_folder_without_auth():
    response = requests.put(BASE_URL, params={'path': 'disk:/no-auth-folder'})
    assert response.status_code == 401


# Тест на попытку авторизоваться с невалидным токеном
def test_create_folder_with_invalid_token():
    invalid_headers = {'Authorization': 'OAuth invalid_token'}
    response = requests.put(BASE_URL, headers=invalid_headers, params={'path': 'disk:/invalid-token-folder'})
    assert response.status_code == 401


# Тест на успешное создание новой папки
def test_create_folder_success(headers, temp_folder):
    response = requests.put(BASE_URL, headers=headers, params={'path': f'disk:/{temp_folder}'})
    assert response.status_code in [201, 409]


# Тест на попытку создать существующую папку
def test_create_existing_folder(headers, create_and_cleanup_folder):
    folder = create_and_cleanup_folder
    response = requests.put(BASE_URL, headers=headers, params={'path': f'disk:/{folder}'})
    assert response.status_code == 409


# Тест на попытку создать папку по некорректному пути
def test_create_folder_invalid_path(headers):
    response = requests.put(BASE_URL, headers=headers, params={'path': 'disk://///'})
    assert response.status_code == 404


# Тест на успешное удаление устой папки
def test_delete_empty_folder(headers, create_and_cleanup_folder):
    folder_to_delete = create_and_cleanup_folder
    path = f"disk:/{folder_to_delete}"
    # Фикстура уже создала папку, теперь мы ее удаляем
    response = requests.delete(BASE_URL, headers=headers, params={'path': path, 'permanently': 'true'})
    assert response.status_code == 204


# Тест на недопустимо длинное название папки
def test_create_folder_with_too_long_name(headers):
    long_name = 'a' * 500
    path = f"disk:/{long_name}"
    response = requests.put(BASE_URL, headers=headers, params={'path': path})
    assert response.status_code == 404
