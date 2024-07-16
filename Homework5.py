# Создание Singleton
class MySingleton:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    @staticmethod
    def get_instance():
        if MySingleton.instance is None:
            MySingleton.instance = MySingleton()
        return MySingleton.instance


singleton1 = MySingleton.get_instance()
singleton2 = MySingleton.get_instance()

print(singleton1 is singleton2)  # True


# Создание Adapter
class MyClass:
    @staticmethod
    def test() -> None:
        print("MyClass.test()")


class MyClassAdapter:
    def __init__(self, obj):
        self.obj = obj

    def test(self):
        self.obj.test()


my_class = MyClass()
my_adapter = MyClassAdapter(my_class)

my_adapter.test()  # MyClass.test()


# Создание Decorator
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@my_decorator
def my_function():
    print("my_function")


my_function()  # Calling function: my_function
