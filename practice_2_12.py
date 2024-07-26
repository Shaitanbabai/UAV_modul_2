import sqlite3

connection = sqlite3.connect('test.db')
cursor = connection.cursor()

# Table "Drones"
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tbl_drones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    max_altitude INTEGER,
    max_speed INTEGER,
    max_flight_time INTEGER,
    serial_number TEXT UNIQUE NOT NULL,
    payload INTEGER
    model TEXT UNIQUE NOT NULL,
    manufacturer TEXT UNIQUE NOT NULL,
    purchase_date DATE,
    software_version TEXT,
    battery_capacity INTEGER,
    flight_hours INTEGER  
)
""")

# Table "Status"
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tbl_drones_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    drone_ID INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    mission_id INTEGER NOT NULL,
    operator_id INTEGER NOT NULL,
    status_update_time DATETIME NOT NULL,
    battery_level INTEGER NOT NULL,
    latitude REAL,
    longitude REAL,
    altitude REAL,
    direction REAL
    is_flying BOOLEAN,
    FOREIGN KEY (drone_id) REFERENCES tbl_drones(id)
    FOREIGN KEY (status_id) REFERENCES tbl_status(id)
    FOREIGN KEY (mission_id) REFERENCES tbl_missions(id)
    FOREIGN KEY (operator_id) REFERENCES tbl_operators(id)
)
""")

# Table "Maintenance"
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tbl_maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drone_id INTEGER NOT NULL,
    last_maintenance DATE,
    description TEXT,
    FOREIGN KEY (drone_id) REFERENCES tbl_drones(id) 
)
""")

# Table "Missions"
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tbl_missions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_mission TEXT NOT NULL,
    name_mission TEXT UNIQUE NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    start_date DATETIME,
    end_date DATETIME
)
""")

# Table "Operators"
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tbl_operators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_operator TEXT TEXT UNIQUE NOT NULL,
    contact TEXT,
    comment TEXT
)
""")

connection.commit()
connection.close()
