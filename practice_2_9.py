# Паттерн Легковес
class DroneFlyweight:
    def __init__(self, model, manufacturer, sensors):
        self._model = model
        self._manufacturer = manufacturer
        self._sensors = sensors

    def operation(self, unique_state):
        print(f"""
        Drone: model {self._model} , manufacturer {self._manufacturer}
        Sensors: {self._sensors}
        Coordinates: {unique_state["coordinates"]}
        Speed: {unique_state["speed"]}
        Mission: {unique_state["mission"]}
        Height: {unique_state["height"]}
        Battery charge: {unique_state["battery"]}
              """)

    @property  # Позволяет обратиться к инкапсулированным атрибутам и добавлять доп. логику
    # getter, позволяющий получить данные об атрибутах
    def model(self):
        return self._model

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def sensors(self):
        return self._sensors


class DroneFactory:
    def __init__(self):
        self._drones = {}

    # Метод получения дрона, принимает те же параметры, что и класс для создания
    def get_drone(self, model, manufacturer, sensors):
        key = (model, manufacturer, sensors)
        if key not in self._drones:
            self._drones[key] = DroneFlyweight(model, manufacturer, sensors)
        return self._drones[key]

    def list_drones(self):
        print(f"Total drones {len(self._drones)}")
        for key in self._drones:
            print(f""")
                  Key: 
                  model {key[0]} , 
                  manufacturer {key[1]}, 
                  sensors {key[2]}
            """)


def client_code():
    factory = DroneFactory()

    drone_1 = factory.get_drone("ModelX", "Drone Corp.", "Camera, GPS")
    drone_1.operation({
        "coordinates": "10, 20, 30",
        "speed": "10, 20, 30",
        "mission": "Surveillance",
        "height": "100",
        "battery": "80"

    })

    drone_2 = factory.get_drone("ModelY", "SkyX.", "lidar, GPS")
    drone_2.operation({
        "coordinates": "10, 40, 60",
        "speed": "50, 30, 10",
        "mission": "Surveillance",
        "height": "100",
        "battery": "85"

    })

    factory.list_drones()


if __name__ == "__main__":
    client_code()
