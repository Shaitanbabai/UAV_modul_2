from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)

# Константы для управления батареей
BATTERY_THRESHOLD = 70  # Минимальный уровень заряда для выполнения миссии
INITIAL_BATTERY = 100  # Начальный уровень заряда батареи
BATTERY_AFTER_PHOTO = 50  # Уровень заряда после выполнения фотосъемки


class Observer:
    """
    Класс наблюдателя, который получает сообщения о состоянии дрона.
    """

    def update(self, message):
        logging.info(message)


class Drone:
    """
    Класс дрона, который выполняет миссии и уведомляет наблюдателей
    о своем состоянии.
    """

    def __init__(self):
        self.battery_level = INITIAL_BATTERY  # Уровень заряда батареи
        self.is_connected = True
        self.observers = []
        self.mission_iterator = None

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def check_battery(self):
        """
        Проверяет уровень заряда батареи и отправляет сообщение наблюдателям.

        Returns:
            bool: True, если уровень заряда выше порогового значения, False - иначе.
        """
        self.notify_observers(f"Battery level: {self.battery_level}%")
        return self.battery_level >= BATTERY_THRESHOLD

    def execute_mission(self):
        """
        Выполняет заданную миссию, контролируя уровень заряда батареи.
        """

        if not self.check_battery():
            self.notify_observers("Battery level is below threshold. Mission aborted.")
            return

        while self.mission_iterator and self.check_battery():
            try:
                task = next(self.mission_iterator)
                task.execute()
            except StopIteration:
                break

        if not self.check_battery():
            self.notify_observers("Battery low. Returning to base.")
        else:
            self.notify_observers("Mission complete. Battery level is above threshold. Requesting new flight plan.")
            self.notify_observers("Entering standby mode.")
            # break  # Раскомментировать для завершения программы после миссии


class Mission(ABC):
    """
    Абстрактный базовый класс для миссий, выполняемых дроном.
    """

    def __init__(self, drone):
        self._drone = drone

    @abstractmethod
    def execute(self):
        pass


class TakeoffMission(Mission):
    """
    Класс миссии по взлету.
    """

    def execute(self):
        self._drone.notify_observers("Taking off...")


class MoveToMission(Mission):
    """
    Класс миссии по перемещению к цели.
    """

    def execute(self):
        self._drone.notify_observers("Moving to target...")


class TakePhotoMission(Mission):
    """
    Класс миссии по фотографированию.
    """

    def execute(self):
        self._drone.notify_observers("Taking photo...")
        self._drone.battery_level = BATTERY_AFTER_PHOTO
        self._drone.check_battery()


class ReturnToBaseMission(Mission):
    """
    Класс миссии по возвращению на базу.
    """

    def execute(self):
        self._drone.notify_observers("Returning to base...")


if __name__ == "__main__":
    drone = Drone()
    drone.add_observer(Observer())

    mission = iter([TakeoffMission(drone), MoveToMission(drone), TakePhotoMission(drone), ReturnToBaseMission(drone)])
    drone.mission_iterator = mission

    drone.execute_mission()
