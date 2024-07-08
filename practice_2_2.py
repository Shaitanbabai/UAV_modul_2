from abc import ABC, abstractmethod  # calling abstract class


# single responsibility principle
# every class response only for one functionality


class NavigationSysten:
    def calc_route(self, start, end):
        print(f"Route calculation from {start} to {end}")
        # logic for metod to be realised
        pass


class CommunicationSystem:
    def send_data(self, data):
        print(f"Data sending {data}")
        # logic
        pass


# Open-Closed principle
# классы должны быть открыты для расширения, но закрыты для модификации
class FlightMode(ABC):  # basic class
    @abstractmethod
    def execute(self):
        pass


class ManualMode(FlightMode):
    def execute(self):
        print("Manual guidance")
        # logic
        pass


class AutoMode(FlightMode):
    def execute(self):
        print("Automatice guidance")
        # logic
        pass


class EmergencyMode(FlightMode):
    def execute(self):
        print("Emergency mode")
        # logic
        pass


class DestructionMode(FlightMode):
    def execute(self):
        print("Self-termination")
        # logic
        pass


class Drone:
    def __init__(self, mode: FlightMode):
        self.__mode = mode

    def change_mode(self, mode: FlightMode):
        self.__mode = mode

    def fly(self):
        self.__mode.execute()


manual_mode = ManualMode()
destruction_mode = DestructionMode()

drone = Drone(manual_mode)
drone.fly()
drone.change_mode(destruction_mode)
drone.fly()
print("\n ================ \n")

# Liskov


class Sensor(ABC):
    @abstractmethod
    def get_data(self):
        pass


class Camera(Sensor):
    def get_data(self):
        print("")
        return "Read data from camera"


class Lidar(Sensor):
    def get_data(self):
        print("")
        return "Read data from lidar"


class Battery(Sensor):
    def get_data(self):
        print("")
        return "Read left charge"


class Drone2:
    def __init__(self, sensor: Sensor):
        self.__sensor = sensor

    def gather_data(self):
        data = self.__sensor.get_data()
        print(f"Gathered data: {data}")


battery = Battery()
drone_2 = Drone2(battery)
drone_2.gather_data()
