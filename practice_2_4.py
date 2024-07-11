# реализация отправки дроном оповещений
# организация структуры декоратора
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):  # метод отправки данных всегда в формате строки
        pass


class SMSNotiifier(Notifier):  # базовый метод
    def __init__(self, phone: str):
        self.phone = phone  # attribute phone stores phone

    def send(self, message: str):  # Справка: сервис дл отправки смс с поддержкой пайтон
        print(f"SMS sent to number {self.phone}, message: {message}")


class NotifierDecorator(Notifier):  # наследование от Нотифайер
    def __init__(self, wrapper: Notifier):  #
        self._wrapper = wrapper  # _wrapped - protected argument

    def send(self, message: str):
        self._wrapper.send(message)


class WhatsappNotifierDecorator(NotifierDecorator):
    def __init__(self, wrapper: Notifier, whatsapp_id: str):
        super().__init__(wrapper)
        self.whatsapp_id = whatsapp_id

    def send(self, message: str):
        super().send(message)
        print(f"Sent WhatsApp to {self.whatsapp_id}, message: {message}")  # найти конкретную реализацию отправки
        # print(f"Attached photo {self.photo}") #для корректной работы нужно сделать надстройку
        # и место хранения фото в абстрактном классе Notifier, прописав путь


class TelegramNotifierDecorator(NotifierDecorator):
    def __init__(self, wrapper: Notifier, telegram_id: str):
        super().__init__(wrapper)
        self.telegram_id = telegram_id

    def send(self, message: str):
        super().send(message)
        print(f"Sent telegram_id to {self.telegram_id}, message: {message}")  # найти конкретную реализацию отправки


class RocketNotifierDecorator(NotifierDecorator):
    def __init__(self, wrapper: Notifier, rocket_number: int):
        super().__init__(wrapper)
        self.rocket_number = rocket_number

    def send(self, message: str):
        super().send(message)
        print(f"Launch signal rocket number {self.rocket_number}")


class PhotoNotifierDecorator(NotifierDecorator):
    def __init__(self, wrapper):
        super().__init__(wrapper)
        self.photo = "path_to_photo.jpg"

    def send(self, message: str):
        super().send(message)
        print(f"Photo made")

# realisation
notifier = SMSNotiifier(phone="+1234567890")
notifier = PhotoNotifierDecorator(notifier)
notifier = WhatsappNotifierDecorator(notifier, whatsapp_id="+1234567890")
notifier = TelegramNotifierDecorator(notifier, telegram_id="@realTLG_id")
notifier = RocketNotifierDecorator(notifier, rocket_number=1)


notifier.send("Текст оповещения")
