from abc import ABC, abstractmethod
import sqlite3


# pattern Abstract factory
class DBFactory(ABC):
    @abstractmethod
    def connect(self):
        pass  # пока нет реализации, она будет в конкретных фабриках


class SQLiteDBFactory(DBFactory):
    def connect(self):  # подключение к базе данных
        return sqlite3.connect(':memory:')
        # в реальной ситуации мы бы прописали путь к файлу с базой, сейчас обращение к ОЗУ


# pattern Builder
class QueryBuilder:  # построитель запросов к базе
    def __init__(self):
        # создаем словарь с основными ключами
        self._query = {
            "select": None,
            "from": None,
            "where": None,
            "order_by": None,
            "insert_into": None,
            "values": None
        }

        self._params = []  # protecting database

    def select(self, table, columns="*"):  # "*" - means select all columns
        self._query["select"] = f"SELECT {columns} "
        self._query["from"] = f" FROM {table} "
        return self

# Варианты обращений к базе SQL
# tbl_drone -> id, model, manufacturer
# SELECT * FROM tbl_drone
# SELECT manufacturer FROM tbl_drone

    def where(self, condition, parameters=None):
        self._query["where"] = f"WHERE {condition} "
        if parameters:
            self._params.extend(parameters)
        return self

    def order_by(self, order):
        self._query["order_by"] = f"ORDER BY {order}"
        return self

    def add_params(self, *parameters):
        self._params.extend(parameters)
        return self

    def insert_into(self, table, columns):
        cols = ",".join(columns)
        # columns = ["model", "manufacturer"]
        # cols = ",".join(columns)
        # рез-т объединения - список превратили в строку с разделителем
        # cols >>> "model, manufacturer
        placeholders = ",".join(["?"] * len(columns))  # определяем число столбцов
        self._query["insert_into"] = f"INSERT INTO {table} ({cols})"
        self._query["values"] = f"VALUES ({placeholders})"
        return self

        # INSERT INTO название_таблицы (список_столбцов) VALUES (значения_столбцов)
        # INSERT INTO tbl_drones (model, manufacturer) VALUES ("model x", "FlyCorp")
        # INSERT INTO tbl_drones (model, manufacturer) VALUES (?, ?)", ("model x", "FlyCorp")
    def values(self, *values):
        self._params.extend(values)
        return self

    def get_query(self):
        query = ""
        if self._query["select"]:
            query = f"{self._query['select']} {self._query['from']}"
        if self._query["where"]:
            query += f" {self._query['where']}"
        if self._query["order_by"]:
            query += f" {self._query['order_by']}"
        if self._query["insert_into"]:
            query = f" {self._query['insert_into']} {self._query['values']}"
        return query

    def get_params(self):
        return self._params


if __name__ == "__main__":
    sql = SQLiteDBFactory()  # creating factory for requests
    connection = sql.connect()  # creating object of connection
    cursor = connection.cursor()  # creates db cursor

    cursor.execute("""
    CREATE TABLE tbl_drones (
        id INTEGER PRIMARY KEY,
        model TEXT,
        manufacturer TEXT,
        year INTEGER
    )
    """)

    drone = {
        "id": "1",
        "model": "x",
        "manufacturer": "SkyCorp",
        "year": "2024",
    }

    query_builder = QueryBuilder()
    insert_into = query_builder.insert_into("tbl_drones", ["model", "manufacturer", "year"]).values(drone["model"],
                                                                                                    drone[
                                                                                                        "manufacturer"],
                                                                                                    drone[
                                                                                                        "year"]).get_query()
    print(insert_into)
    params = query_builder.get_params()
    cursor.execute(insert_into, params)
    connection.commit()

    select_query = QueryBuilder()
    select_query = select_query.select("tbl_drones").get_query()
    cursor.execute(select_query)
    results = cursor.fetchall()
    for row in results:
        print(row)

    connection.close()
