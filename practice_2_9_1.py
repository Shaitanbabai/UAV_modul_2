import time
import math
import matplotlib.pyplot as plt


# lightweight
class CoordinatesFlyWeight:
    _coordinates = {}

    @staticmethod
    def get_coordinates(lat, lon):
        key = (lat, lon)
        if key not in CoordinatesFlyWeight._coordinates:
            CoordinatesFlyWeight._coordinates[key] = key
        return CoordinatesFlyWeight._coordinates[key]


# combining patterns Lightweight and Proxy
class DJIProxy:
    def __init__(self, real_drone):
        self._real_drone = real_drone

    def global_position_control(self, lat=None, lon=None, alt=None):
        # Logging (later replace prints with db file record
        print(f"Request om deployment to lat {lat}, lon {lon}, alt {alt}")
        self._real_drone.global_position_control(lat, lon, alt)
        # time.sleep(1)

    def request_control(self):
        print("Request for connection to drone via SDK")

    def take_off(self):
        print("Take-off initiated")
        self._real_drone.takeoff()

    def land(self):
        print("Landing initiated")
        self._real_drone.land()

    def arm(self):
        print("Arming initiated")
        self._real_drone.arm()


class DJIDrone:
    def global_position_control(self, lat=None, lon=None, alt=None):
        print(f"Redeployment to lat {lat}, lon {lon}, alt {alt}")

    def request_sdk_permission_control(self):
        print("Request on control via SDK")

    def takeoff(self):
        print("Executing takeoff")

    def land(self):
        print("Executing landing")

    def arm(self):
        print("Arming engines")


# Setting initial coordinates for the spiral search in quarter
min_lat = 57.826873
min_lon = 55.475823

max_lat = 57.922174
max_lon = 55.671439

begin_lat = min_lat + (max_lat - min_lat) / 2
begin_lon = min_lon + (max_lon - min_lon) / 2

step = 0.00005
altitude = 50

# Initializing drone
real_drone = DJIDrone()
drone = DJIProxy(real_drone)

coordinates = []


# cycle for spiral flight
def spiral_flight(drone):
    radius = 0
    angle = 0
    while radius <= (max_lon - min_lon)/2:
        radius += step
        angle += math.pi / 180
        x = math.sin(angle) * radius  # shift by lat
        y = math.cos(angle) * radius  # shift by lon
        lat_current = begin_lat + x
        lon_current = begin_lon + y

        # Using pattern FlyWeight for getting unique coordinate
        coordinate = CoordinatesFlyWeight.get_coordinates(lat_current, lon_current)
        coordinates.append(coordinate)
        drone.global_position_control(lat=lat_current, lon=lon_current, alt=altitude)
        # time.sleep(1)


# simulation of redeployment
drone.request_control()
time.sleep(2)

drone.arm()
time.sleep(2)

drone.take_off()
time.sleep(2)

# Redeploying for mission
spiral_flight(drone)

# Return on base
drone.global_position_control(begin_lat, begin_lon, alt=altitude)
time.sleep(2)
drone.land()

# print(*coordinates)
# print("-----------")
# print(*coordinates)
# print("-----------")
latitudes, longitudes = zip(*coordinates)
plt.plot(latitudes, longitudes)
plt.xlabel("lon")
plt.ylabel("lat")
plt.title("Drone spiral route")
plt.show()
