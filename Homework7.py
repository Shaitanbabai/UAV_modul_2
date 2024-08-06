from abc import ABC, abstractmethod
import mysql.connector  # Импорт библиотек MySQL
from mysql.connector import connection
import psycopg2  # импорт библиотек PostgresSQL
from psycopg2 import connect
import sqlite3  # Импорт библиотек SQLite


# Создание интерфейса абстрактной фабрики
class DBFactory(ABC):
    @abstractmethod
    def create_connection(self):
        pass

    @abstractmethod
    def create_cursor(self, connection):
        pass

    @abstractmethod
    def create_query_builder(self):
        pass

    @abstractmethod
    def execute_query(self, connection, query):
        pass


# Реализация фабрики для MySQL
class MySQLFactory(DBFactory):
    def create_connection(self):
        return mysql.connector.connect(
            host="your_host",
            user="your_username",
            password="your_password",
            database="your_database"
        )

    def create_cursor(self, connection):
        return connection.cursor(dictionary=True)  # Используем dictionary=True для удобного маппинга

    def create_query_builder(self):
        return QueryBuilder()


# Реализация фабрики для PostgresSQL
class PostgresFactory(DBFactory):
    def create_connection(self):
        return psycopg2.connect(
            host="your_host",
            user="your_username",
            password="your_password",
            dbname="your_database"
        )

    def create_cursor(self, connection):
        return connection.cursor()

    def create_query_builder(self):
        return QueryBuilder()


# Реализация фабрики для SQLite
class SQLiteFactory(DBFactory):
    def create_connection(self):
        return sqlite3.connect("your_database.db")

    def create_cursor(self, connection):
        return connection.cursor()

    def create_query_builder(self):
        return QueryBuilder()


# Реализация паттерна Строитель для поэтапного построения SQL-запросов.
class QueryBuilder:
    def __init__(self):
        self._query = ""

    def select(self, table, columns):
        self._query = f"SELECT {', '.join(columns)} FROM {table}"
        return self

    def where(self, condition):
        self._query += f" WHERE {condition}"
        return self

    def order_by(self, column, order='ASC'):
        self._query += f" ORDER BY {column} {order}"
        return self

    def get_query(self):
        return self._query


# Реализация объектно-реляционного Отображение для маппинга объектов на таблицы базы данных,
# преобразование объектов в запросы SQL и обратно
class ORM:
    def __init__(self, factory: DBFactory):
        self._connection = factory.create_connection()
        self._cursor = factory.create_cursor(self._connection)
        self._query_builder = factory.create_query_builder()

    def save(self, table, obj):
        columns = ', '.join(obj.keys())
        values = ', '.join(f"'{v}'" for v in obj.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self._cursor.execute(query)
        self._connection.commit()

    def get(self, table, obj_class, condition):
        query = self._query_builder.select(table, ["*"]).where(condition).get_query()
        self._cursor.execute(query)
        row = self._cursor.fetchone()
        if row:
            return obj_class(**dict(zip([column[0] for column in self._cursor.description], row)))
        return None

    def close(self):
        self._cursor.close()
        self._connection.close()


# Класс, который будет маппиться на таблицу в базе данных
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"


def main():
    # Использование MySQLFactory
    mysql_factory = MySQLFactory()
    mysql_connection = mysql_factory.create_connection()
    mysql_cursor = mysql_factory.create_cursor(mysql_connection)
    mysql_query_builder = mysql_factory.create_query_builder()

    query = mysql_query_builder.select("your_table", ["*"]).get_query()
    mysql_cursor.execute(query)
    print("MySQL query result:", mysql_cursor.fetchone())

    mysql_cursor.close()
    mysql_connection.close()

    # Использование PostgresFactory
    postgres_factory = PostgresFactory()
    postgres_connection = postgres_factory.create_connection()
    postgres_cursor = postgres_factory.create_cursor(postgres_connection)
    postgres_query_builder = postgres_factory.create_query_builder()

    query = postgres_query_builder.select("your_table", ["*"]).get_query()
    postgres_cursor.execute(query)
    print("PostgresSQL query result:", postgres_cursor.fetchone())

    postgres_cursor.close()
    postgres_connection.close()

    # Использование SQLiteFactory
    sqlite_factory = SQLiteFactory()
    sqlite_connection = sqlite_factory.create_connection()
    sqlite_cursor = sqlite_factory.create_cursor(sqlite_connection)
    sqlite_query_builder = sqlite_factory.create_query_builder()

    query = sqlite_query_builder.select("your_table", ["*"]).get_query()
    sqlite_cursor.execute(query)
    print("SQLite query result:", sqlite_cursor.fetchone())

    sqlite_cursor.close()
    sqlite_connection.close()


if __name__ == "__main__":
    main()
