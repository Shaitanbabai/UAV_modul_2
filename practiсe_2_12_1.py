"""
Таблица "Дроны"
    ID: Уникальный идентификатор для каждого дрона. Это может быть Primary Key.
    Максимальная высота: Максимальная высота полета дрона. Полезно для определения границ использования.
    Максимальная скорость: Максимальная скорость полета. Важно для планирования миссий и оценки возможностей дрона.
    Максимальное время полета: Указывает на автономность дрона.
    Серийный номер: Уникальный серийный номер дрона для идентификации.
    Грузоподъемность: Максимальный вес, который дрон может нести. Важно для планирования миссий с грузом.
    Модель дрона: Название модели.
    Производитель: Компания-производитель дрона.
    Дата покупки: Дата приобретения дрона, полезно для отслеживания возраста и состояния оборудования.
    Версия ПО: Текущая версия программного обеспечения, установленного на дроне.
    Емкость аккумулятора: Емкость батареи, выраженная в мАч, определяет, как долго дрон может летать без подзарядки.
    Налет в моточасах: Общее время полета дрона, важный показатель для планирования технического обслуживания.

Таблица "Статус"
    ID: Уникальный идентификатор статуса. Primary Key.
    Название статуса: Описание статуса, например, "активен", "в ремонте" и т.д.

Таблица "Статус Дронов"
    ID: Идентификатор статуса дрона
    Дрон_ID: Идентификатор дрона (Foreign Key на таблицу "Дроны").
    Статус_ID: Идентификатор статуса (Foreign Key на таблицу "Статус").
    Миссия_ID: Идентификатор миссии, в которой участвует дрон (Foreign Key на таблицу "Миссии").
    Оператор_ID: Идентификатор оператора, управляющего дроном (Foreign Key на таблицу "Оператор").
    Время обновления статуса: Дата и время последнего обновления статуса.
    Уровень заряда батареи: Текущий уровень заряда батареи.
    Широта:GPS-координаты текущего местоположения дрона.
    Долгота:GPS-координаты текущего местоположения дрона.
    Высота:в метрах
    Направление:в градусахНаходится ли в полете: Boolean-поле, указывающее, находится ли дрон в данный момент в воздухе.

Таблица "Техническое обслуживание"
    ID: Уникальный идентификатор записи ТО. Primary Key.
    Дрон_ID: Идентификатор дрона, проходящего ТО (Foreign Key на таблицу "Дроны").
    Дата последнего ТО: Дата последнего проведенного технического обслуживания.
    Описание работ: Подробное описание выполненных работ.

Таблица "Миссии"
    ID: Уникальный идентификатор миссии. Primary Key.
    Описание миссии: Краткое описание целей и задач миссии.
    Название: Название миссии.
    Тип: Тип миссии, например, "доставка", "мониторинг" и т.д.
    Статус миссии: Статус выполнения миссии, например, "запланирована", "выполняется", "завершена".
    Дата начала: Дата и время начала миссии.
    Дата завершения: Дата и время завершения миссии.

Таблица "Оператор"
    ID: Уникальный идентификатор оператора. Primary Key.
    Имя: Имя оператора.
    Контакты: Контактная информация оператора, может включать телефон, email и т.д.
    Комментарий: Дополнительная информация о операторе, например, квалификация, опыт и т.д.
"""

