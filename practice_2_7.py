# Работа с паттерном Command
# 1. Создаем интерфейс команды
from abc import ABC, abstractmethod


# создаем команды для абстракции
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# создаем команды для абстракции
class Drone:
    def take_off(self):
        # execute command logic
        print("Drone takes off")

    def land(self):
        print("Drone lands")

    def change_route(self, new_route):
        print(f"Drone changed route {new_route}")


class TakeOff(Command):
    def __init__(self, drone: Drone):
        self._drone = drone  # created temp variable

    def execute(self):
        self._drone.take_off()  # передача события для объекта

    def undo(self):
        self._drone.land()


class Land(Command):
    def __init__(self, drone: Drone):
        self._drone = drone

    def execute(self):
        self._drone.land()

    def undo(self):
        print("Landing cancellation impossible")


class ChangeRoute(Command):
    def __init__(self, drone: Drone, route):
        self._drone = drone
        self._route = route
        self._previous_route = None

    def execute(self):
        self._previous_route = "Previous route"
        self._drone.change_route(self._route)  # меняем предыдущий курс и записываем новый

    def undo(self):  # если есть предыдущий курс - мы к нему возвращаемся при отмене нового
        if self._previous_route:
            self._drone.change_route(self._previous_route)


class RemoteControl:
    def __init__(self):
        self._commands = []
        self._history = []  # история команд с возможностью отмены

    def add_command(self, command: Command):
        self._commands.append(command)  # добавляем команды

    def execute_command(self):
        for command in self._commands:
            command.execute()
            self._history.append(command)
        self._commands.clear()

    def undo(self):
        if self._history:
            command = self._history.pop()  # отмена команд с удалением из истории
            command.undo()


drone = Drone()

land = Land(drone)
take_off = TakeOff(drone)
change_route = ChangeRoute(drone, "New route")

remote_control = RemoteControl()
remote_control.add_command(take_off)
remote_control.add_command(change_route)
remote_control.add_command(land)

remote_control.execute_command()
