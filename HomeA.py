import abc
import sqlite3
import psycopg2
import mysql.connector


class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def create_connection(self):
        pass

    @abc.abstractmethod
    def create_query_builder(self):
        pass

    @abc.abstractmethod
    def execute_query(self, connection, query):
        pass


class MySQLFactory(AbstractFactory):
    def create_connection(self):
        return mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_user",
            password="your_mysql_password",
            database="your_mysql_database"
        )

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query):
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        return cursor


class PostgresFactory(AbstractFactory):
    def create_connection(self):
        return psycopg2.connect(
            host="your_postgres_host",
            user="your_postgres_user",
            password="your_postgres_password",
            dbname="your_postgres_database"
        )

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor


class SQLiteFactory(AbstractFactory):
    def create_connection(self):
        return sqlite3.connect("your_sqlite_database.db")

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor


class QueryBuilder:
    def __init__(self):
        self.query = ""

    def select(self, table, columns):
        columns_str = ', '.join(columns)
        self.query = f"SELECT {columns_str} FROM {table}"
        return self

    def where(self, condition):
        self.query += f" WHERE {condition}"
        return self

    def get_query(self):
        return self.query


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(user_id={self.user_id}, name='{self.name}', email='{self.email}')"


class UserMapper:
    @staticmethod
    def to_sql(user):
        return f"INSERT INTO users (id, name, email) VALUES ({user.user_id}, '{user.name}', '{user.email}')"

    @staticmethod
    def from_sql(row):
        return User(row['id'], row['name'], row['email'])


class DBConnectionManager:
    def __init__(self):
        self._connections = {}

    def get_connection(self, factory):
        factory_name = type(factory).__name__
        if factory_name not in self._connections:
            connection = factory.create_connection()
            self._connections[factory_name] = connection
        return self._connections[factory_name]

    def close_connection(self, factory):
        factory_name = type(factory).__name__
        if factory_name in self._connections:
            self._connections[factory_name].close()
            del self._connections[factory_name]


def main():
    db_manager = DBConnectionManager()

    # MySQL Example
    mysql_factory = MySQLFactory()
    mysql_connection = db_manager.get_connection(mysql_factory)
    mysql_query_builder = mysql_factory.create_query_builder()

    user = User(1, 'John Doe', 'john.doe@example.com')
    insert_query = UserMapper.to_sql(user)
    mysql_factory.execute_query(mysql_connection, insert_query)
    mysql_connection.commit()

    select_query = mysql_query_builder.select("users", ["*"]).where("id = 1").get_query()
    cursor = mysql_factory.execute_query(mysql_connection, select_query)
    row = cursor.fetchone()
    if row:
        fetched_user = UserMapper.from_sql(row)
        print(f"Fetched MySQL User: {fetched_user.name}, {fetched_user.email}")

    db_manager.close_connection(mysql_factory)

    # PostgreSQL Example
    postgres_factory = PostgresFactory()
    postgres_connection = db_manager.get_connection(postgres_factory)
    postgres_query_builder = postgres_factory.create_query_builder()

    user = User(2, 'Jane Doe', 'jane.doe@example.com')
    insert_query = UserMapper.to_sql(user)
    postgres_factory.execute_query(postgres_connection, insert_query)
    postgres_connection.commit()

    select_query = postgres_query_builder.select("users", ["*"]).where("id = 2").get_query()
    cursor = postgres_factory.execute_query(postgres_connection, select_query)
    row = cursor.fetchone()
    if row:
        fetched_user = UserMapper.from_sql(row)
        print(f"Fetched PostgreSQL User: {fetched_user.name}, {fetched_user.email}")

    db_manager.close_connection(postgres_factory)

    # SQLite Example
    sqlite_factory = SQLiteFactory()
    sqlite_connection = db_manager.get_connection(sqlite_factory)
    sqlite_query_builder = sqlite_factory.create_query_builder()

    user = User(3, 'Alice', 'alice@example.com')
    insert_query = UserMapper.to_sql(user)
    sqlite_factory.execute_query(sqlite_connection, insert_query)
    sqlite_connection.commit()

    select_query = sqlite_query_builder.select("users", ["*"]).where("id = 3").get_query()
    cursor = sqlite_factory.execute_query(sqlite_connection, select_query)
    row = cursor.fetchone()
    if row:
        fetched_user = UserMapper.from_sql(row)
        print(f"Fetched SQLite User: {fetched_user.name}, {fetched_user.email}")

    db_manager.close_connection(sqlite_factory)


if __name__ == "__main__":
    main()
