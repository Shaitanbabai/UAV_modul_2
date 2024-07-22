import time
import math
import matplotlib.pyplot as plt

# паттерн Flyweight
class CoordinateFlyweight:
    _coordinates = {}

    @staticmethod
    def get_coordinate(lat, lon):
        key = (lat, lon)
        if key not in CoordinateFlyweight._coordinates:
            CoordinateFlyweight._coordinates[key] = key
        return CoordinateFlyweight._coordinates[key]


# паттерн Proxy
class DJIDroneProxy:
    def __init__(self, real_drone):
        self._real_drone = real_drone

    def global_position_control(self, lat=None, lon=None, alt=None):
        # Логирование
        print(f"Запрос на перемещение к широте: {lat}, долготе: {lon}, высоте: {alt}")
        # обращаемся к SDK дрона
        self._real_drone.global_position_control(lat, lon, alt)
        # задержка на выполнение операции дроном
        # time.sleep(1)

    def connect(self):
        print("Запрос на подключение к дрону через SDK")
        self._real_drone.request_sdk_permission_control()

    def takeoff(self):
        print("Взлет инициирован")
        self._real_drone.takeoff()

    def land(self):
        print("Посадка инициирована")
        self._real_drone.land()

    def arm(self):
        print("Армирование дрона инициировано")
        self._real_drone.arm()



class DJIDrone:
    def global_position_control(self, lat=None, lon=None, alt=None):
        print(f"Перемещение к широте: {lat}, долготе: {lon}, высоте: {alt}")

    def request_sdk_permission_control(self):
        print("Запрос на управление через SDK")

    def takeoff(self):
        print("Выполняем взлет")

    def land(self):
        print("Выполняем приземление")

    def arm(self):
        print("Армирование дрона")


min_lat = 57.826873
min_lon = 55.475823

max_lat = 57.922174
max_lon = 55.671439

begin_lat = min_lat + (max_lat - min_lat) / 2
begin_lon = min_lon + (max_lon - min_lon) / 2

step = 0.00005
altitude = 50

real_drone = DJIDrone()
drone = DJIDroneProxy(real_drone)

coordinates = []

def spiral(drone):
    radius = 0
    angle = 0
    while radius <= (max_lon - min_lon)/2:
        radius += step
        angle += math.pi / 180
        x = math.sin(angle) * radius
        y = math.cos(angle) * radius
        lat_current = begin_lat + x
        lon_current = begin_lon + y
        # Используем паттерн Flyweight
        coordinate = CoordinateFlyweight.get_coordinate(lat_current, lon_current)
        coordinates.append(coordinate)
        drone.global_position_control(lat=lat_current, lon=lon_current, alt=altitude)
        # time.sleep(1)


drone.connect()
time.sleep(2)
drone.arm()
time.sleep(2)
drone.takeoff()
time.sleep(4)
# Отправляем дрон на выполенние миссии
spiral(drone)
# Возврат на базу
drone.global_position_control(begin_lat, begin_lon, alt=altitude)
time.sleep(2)
drone.land()

latitudes, longitudes = zip(*coordinates)
plt.plot(latitudes, longitudes)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Движение дрона по спирали")
plt.show()

