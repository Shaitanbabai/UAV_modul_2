# pattern Bridge
from abc import ABC, abstractmethod


# flight control
class Drone(ABC):
    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    def flight(self):
        pass


# realisation for the abstract class Engine
class Engine(ABC):
    @abstractmethod
    def start(self):
        pass

    def stop(self):
        pass

    def status(self):
        pass

    def set_rotation_speed(self, speed: int):
        pass


class SingleEngine(Engine):
    def start(self):
        return "Engine launch"

    def stop(self):
        return "Engine's shutdown"

    def status(self):
        return "Status for single engine"

    def set_rotation_speed(self, speed: int):
        power = speed * 10  # Every 1% of speed consumes 10mA
        print(f"Set single engine speed to {speed} turns/min.")
        return power  # returning consumable power


class MultiEngineAdapter(Engine):
    def start(self):
        return "Engines launch"

    def stop(self):
        return "Engines shutdown"

    def status(self):
        return "Status for number of engines"

    def set_rotation_speed(self, speed: int):
        power = speed * 40  # Every 1% of speed consumes 10mA per 4 engines
        print(f"Set multiple engine speed to {speed} turns/min.")
        return power  # returning consumable power


class StandardDrone(Drone):
    def flight(self):
        print("Standard drone in flight")
        speed = 50  # engine launched at 50% of power
        print(self.engine.start())
        print(f"consumable electric current {self.engine.set_rotation_speed(speed)} mA")
        print(self.engine.status())
        print(self.engine.stop())


class AdvancedDrone(Drone):
    def flight(self):
        print("Advanced drone in flight")
        speed = 50  # engine launched at 50% of power
        print(self.engine.start())
        print(f"consumable electric current {self.engine.set_rotation_speed(speed)} mA")
        print(self.engine.status())
        print(self.engine.stop())

    def get_status(self):
        print(self.engine.status())

    def set_speed(self, speed: int):
        current = self.engine.set_rotation_speed(speed)
        print(f"Set speed: {speed} %, \n consumable electric current {self.engine.set_rotation_speed(speed)} mA")


# creating entry point
if __name__ == "__main__":
    single_engine = SingleEngine()
    multiple_engine = MultiEngineAdapter()

    standard_drone = StandardDrone(single_engine)
    advanced_drone = AdvancedDrone(multiple_engine)

    standard_drone.flight()
    print()

    advanced_drone.flight()
    advanced_drone.set_speed(75)
    advanced_drone.get_status()
    print()

    print("Замена двигателя")
    advanced_drone.engine = multiple_engine
    advanced_drone.flight()
    advanced_drone.get_status()
