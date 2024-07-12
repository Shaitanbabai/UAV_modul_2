# pattern Observer
from abc import ABC, abstractmethod
import cv2


class Observer(ABC):
    @abstractmethod
    def update(self, message: str, image=None):
        pass


class Observable:  # realization for co-operation with observers
    # in more complicated systems here should be downer lvl of abstraction
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, message: str, image=None):
        for observer in self._observers:
            observer.update(message, image)


class DataLogger(Observer):  # realization, receives message and image
    def update(self, message: str, image=None):
        print(f"Logging system got a message: {message}.")
        if image is not None:
            self.save_image(image)

    @staticmethod
    def save_image(image):
        filename = "shot.png"
        cv2.imwrite(filename, image)
        print(f"Image done")


class AlertSystem(Observer):
    def update(self, message: str, image=None):
        print(f"Alert system got a message: {message}.")


class AnalysisSystem(Observer):
    def update(self, message: str, image=None):
        print(f"Analysis system got a message: {message}.")


class Camera(Observable):
    def __init__(self):
        super().__init__()
        self._zoom_lvl = 1.0

    def set_zoom(self, zoom_lvl: float):
        self._zoom_lvl = zoom_lvl
        self.notify_observers(f"Zoom changed to {zoom_lvl}.")

    def take_image(self):
        caption = cv2.VideoCapture(0)  # switch to system Camera 0
        ret, frame = caption.read()  # ret- metadata, frame - picture
        if ret:  # if ret isn't empty -> smth on the picture
            self.notify_observers("Image captured", frame)
        caption.release()  # work with camera finished


# Creating Observers examples of classes
data_logger = DataLogger()
alert_system = AlertSystem()
analysis_system = AnalysisSystem()

camera = Camera()

camera.add_observer(data_logger)
camera.add_observer(alert_system)
camera.add_observer(analysis_system)

camera.set_zoom(2.0)
camera.take_image()
