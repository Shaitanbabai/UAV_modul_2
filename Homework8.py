from abc import ABC, abstractmethod


# Интерфейс SomeObject с методами для доступа к данным
class SomeObject(ABC):
    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def perform_action(self, action):
        pass


# Реализация реального объекта, который предоставляет доступ к данным
class RealObject(SomeObject):
    def __init__(self):
        self.data = "Sensitive Data"  # Пример защищённых данных

    def get_data(self):
        return self.data

    def perform_action(self, action):
        return f"Action {action} performed on {self.data}"


# Класс Proxy для добавления проверки прав доступа
class Proxy(SomeObject):
    def __init__(self, real_object, user_role):
        self._real_object = real_object
        self._user_role = user_role

    def has_access(self):
        # Простая проверка прав доступа
        return self._user_role in ['admin', 'superuser']

    def get_data(self):
        if self.has_access():
            return self._real_object.get_data()
        else:
            return "Access Denied"  # Отказ в доступе при отсутствии прав

    def perform_action(self, action):
        if self.has_access():
            return self._real_object.perform_action(action)
        else:
            return "Access Denied"  # Отказ в доступе при отсутствии прав


# Класс SecureProxy для добавления дополнительных проверок безопасности
class SecureProxy(SomeObject):
    def __init__(self, real_object, user_role, security_token):
        self._real_object = real_object
        self._user_role = user_role
        self._security_token = security_token

    def has_access(self):
        # Проверка прав доступа с дополнительной проверкой токена
        return self._user_role == 'admin' and self.is_valid_token()

    def is_valid_token(self):
        # Проверка валидности токена
        return self._security_token == "valid_token"

    def get_data(self):
        if self.has_access():
            return self._real_object.get_data()
        else:
            return "Access Denied"  # Отказ в доступе при отсутствии прав или невалидном токене

    def perform_action(self, action):
        if self.has_access():
            return self._real_object.perform_action(action)
        else:
            return "Access Denied"  # Отказ в доступе при отсутствии прав или невалидном токене


# Реализация
def main():
    real_object = RealObject()

    # Использование Proxy без прав доступа
    proxy = Proxy(real_object, 'user')
    print(proxy.get_data())  # Access Denied

    # Использование Proxy с правами администратора
    proxy_admin = Proxy(real_object, 'admin')
    print(proxy_admin.get_data())  # Sensitive Data

    # Использование SecureProxy с валидным токеном
    secure_proxy = SecureProxy(real_object, 'admin', 'valid_token')
    print(secure_proxy.get_data())  # Sensitive Data

    # Использование SecureProxy с невалидным токеном
    secure_proxy_invalid = SecureProxy(real_object, 'admin', 'invalid_token')
    print(secure_proxy_invalid.get_data())  # Access Denied


if __name__ == '__main__':
    main()
