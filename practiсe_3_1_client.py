import requests
import json

base_url = 'http://127.0.0.1:5000'

response = requests.post(f"{base_url}/drone/takeoff")
print(f"Статус код: {response.status_code}")
print(f"Ответ: {response.json()}")