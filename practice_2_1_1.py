# Фабричеый метод, абстрактные классы

from abc import ABC, abstractmethod  # calling abstract class


class Mission(ABC):
    @abstractmethod  # added decorator for abstract method
    def execute(self):
        pass


class BackMission(Mission):
    def execute(self):  # создали метод класса
        return "Выполнение миссии возврат на базу"


class MappingMission(Mission):  # наследование класса от Mission
    def execute(self):
        return "Выполнение картографирования"


class PatrolMission(Mission):
    def execute(self):
        return "Выполнение патрулирования"


class EvacuationMission(Mission):
    def execute(self):
        return "Выполнение эвакуации"


# создаем абстрактный класс Фабрика Миссий
class MissionFactory(ABC):
    @abstractmethod  # абстрактный класс для создания методов миссий
    def create_mission(self):
        pass


class BackMissionFactory(MissionFactory):
    def create_mission(self):
        return BackMission()


class MappingMissionFactory(MissionFactory):
    def create_mission(self):
        return MappingMission()


class PatrolMissionFactory(MissionFactory):
    def create_mission(self):
        return PatrolMission()


class EvacuationMissionFactory(MissionFactory):
    def create_mission(self):
        return EvacuationMission()


def mission_planner(factory: MissionFactory):
    mission = factory.create_mission()  # создаем переменную mission и возвращаем экземпляр клласса
    return mission.execute()  # возвращаем результат выполнения метода


patrol_factory = PatrolMissionFactory()
print(mission_planner(patrol_factory))

mapping_factory = MappingMissionFactory()
print(mission_planner(mapping_factory))  # остается реализовать сам алгоритм выполнения метода

