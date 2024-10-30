from http.client import responses
from faker import Faker

fake = Faker
import response
from urllib3 import request
import requests


base_url = 'https://api.clickup.com/api/v2'
head = {
    "authorization": 'pk_2144434058_74WQSRIORR0V0XWNQDOT6DSL9UN45KXU'
}

space_id = '90121435817'

def test_get_lists():
    response = requests.get(f'{base_url}/space/{space_id}/list', headers=head)
    assert response.status_code == 200, f"Request failed with bode {response.text}"


# def test_post_folders():
#     body = {"name": fake.first_kana_name()}
#     print(body)
#     response = requests.post(f'{base_url}/space/{space_id}/folder', headers=head, data=body)
#     assert response.status_code == 200, f"Request failed with bode {response.text}"
