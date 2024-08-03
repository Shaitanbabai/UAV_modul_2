import requests
import cv2
import json
import time

base_url = 'http://127.0.0.1:5000/'


def send_telemetry(latitude, longitude, altitude):
    json_data = {
        'latitude': latitude,
        'longitude': longitude,
        'altitude': altitude
    }
    response = requests.post(f"{base_url}telemetry", json=json_data)
    print(response.json())


def send_video(video_frame):
    _, buffer = cv2.imencode('.jpg', video_frame)
    response = requests.post(f"{base_url}video", data=buffer.tobytes())
    if response.status_code == 204:
        print("Кадр успешно отправлен")
    else:
        print("Ошибка при отправке кадра")


if __name__ == '__main__':
    send_telemetry(55.5555, 37.7777, 100.0)
    cap = cv2.VideoCapture(0)
    fps = 60
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        send_video(frame)
        time.sleep(1/fps)
    cap.release()
    cv2.destroyAllWindows()
