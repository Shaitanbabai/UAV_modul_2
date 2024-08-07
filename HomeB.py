import abc
import sqlite3
import psycopg2
import mysql.connector
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Абстрактная фабрика
class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def create_connection(self):
        pass

    @abc.abstractmethod
    def create_query_builder(self):
        pass

    @abc.abstractmethod
    def execute_query(self, connection, query, params=None):
        pass


class MySQLFactory(AbstractFactory):
    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root_password",
                database="mysql_test_db"
            )
            logger.info("MySQL connection established.")
            return connection
        except mysql.connector.Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            raise

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query, params=None):
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            connection.commit()
            logger.info(f"MySQL query executed: {query}")
            return cursor
        except mysql.connector.Error as e:
            logger.error(f"Error executing MySQL query: {e}")
            raise


class PostgresFactory(AbstractFactory):
    def create_connection(self):
        try:
            connection = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="postgres_password",
                dbname="postgresql_test_db"
            )
            logger.info("PostgresSQL connection established.")
            return connection
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgresSQL: {e}")
            raise

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query, params=None):
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
            logger.info(f"PostgresSQL query executed: {query}")
            return cursor
        except psycopg2.Error as e:
            logger.error(f"Error executing PostgresSQL query: {e}")
            raise


class SQLiteFactory(AbstractFactory):
    def create_connection(self):
        try:
            connection = sqlite3.connect("sqlite_test_db.db")
            logger.info("SQLite connection established.")
            connection.row_factory = sqlite3.Row  # Позволяет использовать имена колонок
            return connection
        except sqlite3.Error as e:
            logger.error(f"Error connecting to SQLite: {e}")
            raise

    def create_query_builder(self):
        return QueryBuilder()

    def execute_query(self, connection, query, params=None):
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            logger.info(f"SQLite query executed: {query}")
            return cursor
        except sqlite3.Error as e:
            logger.error(f"Error executing SQLite query: {e}")
            raise


# Строитель для SQL-запросов
class QueryBuilder:
    def __init__(self):
        self.query = ""
        self.params = []

    def select(self, table, columns):
        columns_str = ', '.join(columns)
        self.query = f"SELECT {columns_str} FROM {table}"
        return self

    def where(self, condition):
        self.query += f" WHERE {condition}"
        return self

    def insert(self, table, columns):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in columns])
        self.query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        return self

    def get_query(self):
        return self.query

    def get_params(self):
        return self.params


# Класс для представления пользователя
class Drone:
    def __init__(self, drone_id, manufacturer, model, battery_capacity):
        self.drone_id = drone_id
        self.manufacturer = manufacturer
        self.model = model
        self.battery_capacity = battery_capacity

    def __repr__(self):
        return (f"Drone(drone_id={self.drone_id}, manufacturer='{self.manufacturer}', \n"
                f"model='{self.model}', battery_capacity='{self.battery_capacity}')")


# Использует фабрику для создания соединения и поиска объекта по ID.
class DroneMapper:
    def __init__(self, factory):
        self.factory = factory
        self.connection = self.factory.create_connection()

    def find_by_id(self, drone_id):
        query_builder = self.factory.create_query_builder()
        query = query_builder.select("drones", ["id", "manufacturer", "model", "battery_capacity"]) \
            .where(f"id = ?") \
            .get_query()
        cursor = self.factory.execute_query(self.connection, query, (drone_id,))
        result = cursor.fetchone()
        if result:
            drone = Drone(result["id"], result["manufacturer"], result["model"],  result["battery_capacity"])
            return drone
        return None

    def insert_drone(self, drone):
        query_builder = self.factory.create_query_builder()
        query = query_builder.insert("drones", ["manufacturer", "model", "battery_capacity"]).get_query()
        self.factory.execute_query(self.connection, query, (drone.manufacturer, drone.model, drone.battery_capacity))
        logger.info(f"Drone {drone.manufacturer} inserted into database.")

    def __del__(self):
        if self.connection:
            self.connection.close()
            logger.info(f"Connection closed for {type(self.factory).__name__}.")


# Контекстный менеджер для управления соединениями с базой данных.
class DBConnectionManager:
    def __init__(self, factory):
        self.factory = factory

    def __enter__(self):
        self.connection = self.factory.create_connection()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            logger.info(f"Connection closed for {type(self.factory).__name__} database.")


# Создает таблицы в каждой базе данных, используя контекстный менеджер для управления соединениями.
def create_tables(factories):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS drones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer VARCHAR(100),
        model VARCHAR(100),
        battery_capacity VARCHAR(100)
    );
    """

    for factory in factories:
        with DBConnectionManager(factory) as connection:
            try:
                cursor = factory.execute_query(connection, create_table_query)
                cursor.close()
                logger.info(f"Table 'drones' created or already exists in {type(factory).__name__} database.")
            except Exception as e:
                logger.error(f"Failed to create table in {type(factory).__name__} database: {e}")


# Создает таблицы, затем создает `DroneMapper` для каждой базы данных и ищет объект с ID 1.
def main():
    factories = [SQLiteFactory(), MySQLFactory(), PostgresFactory()]  #
    create_tables(factories)

    # Вставка данных в SQLite
    sqlite_factory = SQLiteFactory()
    drone_mapper = DroneMapper(sqlite_factory)
    drone_mapper.insert_drone(Drone(None, "DJI", "Mavic", "10000"))
    drone_mapper.insert_drone(Drone(None, "Heron", "2000A", "20000"))
    drone_mapper.insert_drone(Drone(None, "Baba Yaga", "R2D2", "5000"))

    for factory in factories:
        drone_mapper = DroneMapper(factory)
        drone = drone_mapper.find_by_id(1)
        if drone:
            logger.info(f"Drone found in {type(factory).__name__}: {Drone}")
        else:
            logger.info(f"No drone found with ID 1 in {type(factory).__name__} database.")


if __name__ == "__main__":
    main()
