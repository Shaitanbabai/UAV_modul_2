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

    def execute_query(self, connection, query):
        cursor = self.create_cursor(connection)
        cursor.execute(query)
        connection.commit()
        return cursor


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
        return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  # DictCursor для удобного маппинга

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query):
        cursor = self.create_cursor(connection)
        cursor.execute(query)
        connection.commit()
        return cursor


# Реализация фабрики для SQLite
class SQLiteFactory(DBFactory):
    def create_cursor(self, connection):
        connection.row_factory = sqlite3.Row  # Используем sqlite3.Row для удобного маппинга
        return connection.cursor()

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query):
        cursor = self.create_cursor(connection)
        cursor.execute(query)
        connection.commit()
        return cursor


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


# Метод для выполнения SQL-запросов в фабрики
class UserMapper:
    @staticmethod
    def to_sql(user):
        return f"INSERT INTO users (id, name, email) VALUES ({user.user_id}, '{user.name}', '{user.email}')"

    @staticmethod
    def from_sql(row):
        return User(row['id'], row['name'], row['email'])


def main():
    # Использование MySQLFactory
    mysql_factory = MySQLFactory()
    mysql_connection = mysql_factory.create_connection()
    mysql_query_builder = mysql_factory.create_query_builder()

    user = User(1, 'John Doe', 'john.doe@example.com')
    insert_query = UserMapper.to_sql(user)

    mysql_factory.execute_query(mysql_connection, insert_query)

    select_query = mysql_query_builder.select("users", ["*"]).where("id = 1").get_query()
    cursor = mysql_factory.execute_query(mysql_connection, select_query)
    row = cursor.fetchone()
    fetched_user = UserMapper.from_sql(row)
    print(f"Fetched MySQL User: {fetched_user.name}, {fetched_user.email}")

    mysql_connection.close()

    # Использование PostgresFactory
    postgres_factory = PostgresFactory()
    postgres_connection = postgres_factory.create_connection()
    postgres_query_builder = postgres_factory.create_query_builder()

    user = User(1, 'John Doe', 'john.doe@example.com')
    insert_query = UserMapper.to_sql(user)

    postgres_factory.execute_query(postgres_connection, insert_query)

    select_query = postgres_query_builder.select("users", ["*"]).where("id = 1").get_query()
    cursor = postgres_factory.execute_query(postgres_connection, select_query)
    row = cursor.fetchone()
    fetched_user = UserMapper.from_sql(row)
    print(f"Fetched Postgres User: {fetched_user.name}, {fetched_user.email}")

    postgres_connection.close()

    # Использование SQLiteFactory
    sqlite_factory = SQLiteFactory()
    sqlite_connection = sqlite_factory.create_connection()
    sqlite_query_builder = sqlite_factory.create_query_builder()

    user = User(1, 'John Doe', 'john.doe@example.com')
    insert_query = UserMapper.to_sql(user)

    sqlite_factory.execute_query(sqlite_connection, insert_query)

    select_query = sqlite_query_builder.select("users", ["*"]).where("id = 1").get_query()
    cursor = sqlite_factory.execute_query(sqlite_connection, select_query)
    row = cursor.fetchone()
    fetched_user = UserMapper.from_sql(row)
    print(f"Fetched SQLite User: {fetched_user.name}, {fetched_user.email}")


if __name__ == "__main__":
    main()
