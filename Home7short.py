import abc
import sqlite3
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
        return QueryBuilder("sqlite")

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
    def __init__(self, db_type):
        self.query = ""
        self.params = []
        self.db_type = db_type

    def select(self, table, columns):
        columns_str = ', '.join(columns)
        self.query = f"SELECT {columns_str} FROM {table}"
        return self

    def where(self, condition):
        self.query += f" WHERE {condition}"
        return self

    def insert(self, table, columns):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?' if self.db_type == 'sqlite' else '%s' for _ in columns])
        self.query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        return self

    def get_query(self):
        return self.query

    def get_params(self):
        return self.params


# Класс для представления дрона
class Drone:
    def __init__(self, drone_id, manufacturer, model, battery_capacity):
        self.drone_id = drone_id
        self.manufacturer = manufacturer
        self.model = model
        self.battery_capacity = battery_capacity

    def __repr__(self):
        return (f"Drone(drone_id={self.drone_id}, manufacturer='{self.manufacturer}', "
                f"model='{self.model}', battery_capacity='{self.battery_capacity}')")


# Использует фабрику для создания соединения и поиска дрона по ID.
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
        cursor.close()
        if result:
            drone = Drone(result["id"], result["manufacturer"], result["model"], result["battery_capacity"])
            return drone
        return None

    def insert_drone(self, drone):
        # Проверка на существование записи
        query_builder = self.factory.create_query_builder()
        check_query = query_builder.select("drones", ["id"]) \
            .where("manufacturer = ? AND model = ? AND battery_capacity = ?") \
            .get_query()
        cursor = self.factory.execute_query(self.connection, check_query,
                                            (drone.manufacturer, drone.model, drone.battery_capacity))
        result = cursor.fetchone()
        cursor.close()

        if result:
            logger.info(f"Drone {drone.manufacturer} {drone.model} already exists in database.")
        else:
            # Вставка новой записи
            query_builder = self.factory.create_query_builder()
            query = query_builder.insert("drones", ["manufacturer", "model", "battery_capacity"]).get_query()
            self.factory.execute_query(self.connection, query,
                                       (drone.manufacturer, drone.model, drone.battery_capacity))
            logger.info(f"Drone {drone.manufacturer} {drone.model} inserted into database.")

    def __del__(self):
        if self.connection:
            self.connection.close()
            logger.info(f"Connection closed for {type(self.factory).__name__}.")


# Контекстный менеджер для управления соединениями с базо данных
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


# Создает таблицы, используя контекстный менеджер для управления соединениями.
def create_tables(factory):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS drones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer VARCHAR(100),
        model VARCHAR(100),
        battery_capacity VARCHAR(100)
    );
    """
    with DBConnectionManager(factory) as connection:
        try:
            cursor = factory.execute_query(connection, create_table_query)
            cursor.close()
            logger.info(f"Table 'drones' created or already exists in {type(factory).__name__} database.")
        except Exception as e:
            logger.error(f"Failed to create table in {type(factory).__name__} database: {e}")


# Создает таблицы, затем создает `DroneMapper` и ищет дрона с ID 1.
def main():
    factory = SQLiteFactory()
    create_tables(factory)

    drone_mapper = DroneMapper(factory)

    drones = [
        Drone(None, "DJI", "Mavic Pro", "3830 mAh"),
        Drone(None, "Rafael", "Harop", "12000 mAh"),
        Drone(None, "Parrot", "Anafi", "2700 mAh")
    ]

    for drone in drones:
        drone_mapper.insert_drone(drone)

    for drone_id in range(1, 100):
        found_drone = drone_mapper.find_by_id(drone_id)
        if found_drone:
            logger.info(f"Found drone: {found_drone}")
        else:
            logger.info(f"Drone with ID {drone_id} not found.")


if __name__ == "__main__":
    main()
