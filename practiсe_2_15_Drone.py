import jwt
import practiсe_2_15_Server
import time

SECRET_KEY = 'myKEY-111'

def request_token(user_id):
    return practiсe_2_15_Server.generate_token(user_id)

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        print("Токен истек")
        return None
    except jwt.InvalidTokenError:
        print("Токен не валиден")
        return None

user_id = "Egor1"
token = request_token(user_id)
print(f"{user_id} получили токен:\n{token}")

time.sleep(7)

user_id_from_token = verify_token(token)
if user_id_from_token:
    print(f"Пользователь {user_id_from_token} авторизирован")
else:
    print("Ошибка авторизации")

