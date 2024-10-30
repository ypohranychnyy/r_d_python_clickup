import requests
import json
import uuid
import time
import pytest
from pytest_steps import test_steps
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TOKEN = os.getenv("CLICKUP_API_TOKEN")
FOLDER_ID = os.getenv("CLICKUP_FOLDER_ID")
HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

@pytest.fixture(scope="module")
def list_id():
    # Create a list and yield its ID for use in other tests
    list_id = create_list()
    yield list_id
    # Clean up by deleting the list after tests are done
    delete_list(list_id)

def create_list():
    # Генерація унікального імені для списку
    unique_name = f"Test {uuid.uuid4().hex[:6]}"
    url = f"{BASE_URL}/folder/{FOLDER_ID}/list"
    payload = {
        "name": unique_name,
        "content": "This is a test list",
        "due_date": None,
        "due_date_time": False,
        "priority": None,
    }

    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    # Збереження list_id для подальшого використання
    list_data = response.json()
    list_id = list_data.get("id")

    # Перевірка, що list_id був створений
    assert list_id is not None, "List ID was not created"

    # Додаткові перевірки (наприклад, що ім'я списку відповідає очікуваному)
    assert list_data.get("name") == unique_name, "List name does not match expected value"

    # Збереження list_id для подальших тестів
    return list_id

@test_steps("create", "get", "update", "delete")
def test_list_operations():
    # Step 1: Create List
    list_id = create_list()
    yield "create", list_id

    # Step 2: Get List
    url = f"{BASE_URL}/list/{list_id}"
    response = requests.get(url, headers=HEADERS)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    list_data = response.json()
    assert list_data.get("id") == list_id, "Retrieved list ID does not match expected value"
    yield "get", list_id

    # Step 3: Update List
    updated_name = f"Updated {uuid.uuid4().hex[:6]}"
    url = f"{BASE_URL}/list/{list_id}"
    payload = {
        "name": updated_name,
        "content": "This is an updated test list",
        "due_date": None,
        "due_date_time": False,
        "priority": 2,
    }
    response = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    list_data = response.json()
    assert list_data.get("name") == updated_name, "List name was not updated correctly"
    yield "update", list_id

    # Step 4: Delete List
    delete_list(list_id)
    yield "delete", list_id

def delete_list(list_id):
    url = f"{BASE_URL}/list/{list_id}"
    response = requests.delete(url, headers=HEADERS)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    # Зачекати кілька секунд перед повторним отриманням списку, щоб дати час серверу обробити видалення
    time.sleep(5)

    # Спроба отримати видалений список для перевірки, що його було видалено
    retry_count = 3
    for _ in range(retry_count):
        get_response = requests.get(url, headers=HEADERS)
        if get_response.status_code in [404, 400]:
            break
        time.sleep(2)
    else:
        assert False, "List was not deleted successfully"

# Add pytest_steps to the requirements.txt for installation
# requirements.txt
# pytest
# pytest-steps
# python-dotenv
