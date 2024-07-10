import xml.etree.ElementTree as ET
import json


class SensorXML:
    def __init__(self, path: str):
        self.path = path  # transferring path to the file

    def get_data(self):
        with open(self.path, "r", encoding="utf-8") as file:
            data = file.read()
        return data


class JSONAdapter:
    def __init__(self, sensor_xml: SensorXML):
        self.sensor_xml = sensor_xml

    def get_data(self):
        xml_data = self.sensor_xml.get_data()
        root = ET.fromstring(xml_data)  # create xml object from sting
        return self.xml_to_json(root)

    @staticmethod
    def xml_to_json(root):
        # Метод адаптера для статического метода self не работает.
        # Указали декоратор статического метода и обратились прямо в root
        # статический метод ускоряет работу кода
        dict_data = {}
        for element in root:
            dict_data[element.tag] = int(element.text)  # извлекаем название тега и значение элемента
        # {"altitude": 1000, "speed": 150} - вот, что получится в json на выходе
        return dict_data


sensor_data = SensorXML("sensor.xml")  # создание переменной данных сенсора
adapter = JSONAdapter(sensor_data)  # создан экземль класса
json_data = adapter.get_data()  # переменная обращается к гет_дата и получает в джейсон словарь
print(json.dumps(json_data, indent=4))
