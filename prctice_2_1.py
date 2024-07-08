class Sensor:
    def get_data(self):
        pass


class Camera(Sensor):
    def get_data(self):
        return "Data from camera"


class Lidar(Sensor):
    def get_data(self):
        return "Data from lidar"

class SensorFactory:  # creating factory for the sensors
    # createa differen types of sensors
    def create_sensor(self):
        pass


class CameraFactory(SensorFactory):
    def create_sensor(self):
        return Camera()
    print()


class LidarFactory(SensorFactory):
    def create_sensor(self):
        return Lidar()


sensor_factory = CameraFactory()
sensor = sensor_factory.create_sensor()
data = sensor.get_data()
