# реализация отправки дроном оповещений
# организация структуры
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):  # метод отправки данных всегда в формате строки
        pass


class SMS_Notiifier(Notifier):  # базовый метод
    def __init__(self, phone: str):
        self.phone = phone  # attribute phone stores phone

    def send(self, message: str):  # Справка: сервис дл отправки смс с поддержкой пайтон
        print(f"SMS sent to number {self.phone}, message: {message}")


class NotifierDecorator:

