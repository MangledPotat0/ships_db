# -*- coding: utf-8 -*-
"""
app/db/schema.py
Handles database table creation and management
"""

# 3rd party imports
from psycopg2.extensions import connection

# Table creation strings

CREATE_SHIPS_TABLE = """
CREATE TABLE IF NOT EXISTS  (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    builder_id INTEGER NOT NULL REFERENCES builders(id),
    owner_id INTEGER NOT NULL REFERENCES owners(id),
    ship_type_id INTEGER NOT NULL REFERENCES ship_types(id),
    ship_class_id INTEGER NOT NULL REFERENCES ship_classes(id),
    date_built DATE,
    date_comissioned DATE,
    date_decomissioned DATE,
    date_scrapped_or_sunk DATE,
    ship_status_id INTEGER NOT NULL REFERENCES ship_statuses(id)
    length_m DOUBLE PRECISION,
    beam_m DOUBLE PRECISION,
    draft_m DOUBLE PRECISION,
    gross_tonnage DOUBLE PRECISION,
    displacement_std_t DOUBLE PRECISION,
    displacement_full_t DOUBLE PRECISION,
    engine_type_id INTEGER NOT NULL REFERENCES engine_types(id),
    engine_count INTEGER,
    screws_count INTEGER,
    engine_shp DOUBLE PRECISION,
    speed_knts DOUBLE PRECISION,
    complement_std INTEGER
);
"""

CREATE_SHIP_TYPES_TABLE = """
CREATE TABLE IF NOT EXISTS ship_types (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

CREATE_SHIP_CLASSES_TABLE = """
CREATE TABLE IF NOT EXISTS ship_classes (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

CREATE_ENGINE_TYPES_TABLE = """
CREATE TABLE IF NOT EXISTS engine_types (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

CREATE_BUILDERS_TABLE = """
CREATE TABLE IF NOT EXISTS builders (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(id),
    founded DATE,
    shutdown DATE
);
"""

CREATE_OWNERS_TABLE = """
CREATE TABLE IF NOT EXISTS owners (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(id)
);
"""

CREATE_STATUSES_TABLE = """
CREATE TABLE IF NOT EXISTS ship_statuses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
);
"""

CREATE_COUNTRIES_TABLE = """
CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
);
"""

def table_exists(conn: connection, table_name: str) -> bool:
    """
    Checks whether or not specified table exists in the database connected to
    the current connection handle.

    Args:
        conn (connection): psql database connection handle.
        table_name (str): Name of the table being checked.

    Returns:
        
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            ) as exists;
            """,
            (table_name,)
        )
        return cur.fetchone()["exists"]

def create_table(conn: connection, table_name: str, create_sql: str) -> None:
    """
    Checks for table in the database. if it exists, nothing happens. If it
    doesn't, then creates the table.

    Args:
        conn (connection): psql database connection handle.
        table_name (str): Name of the table to create.
        create_sql (str): sql query string to create the table.

    Returns:
        None
    """
    if table_exists(conn, table_name):
        print(f"Table \"{table_name}\" already exists.")
        return

    print(f"Table \"{table_name}\" does not exist. Creating it now.")
    with conn.cursor() as cur:
        cur.execute(create_sql)
    conn.commit()
    print(f"Table \"{table_name}\" created.")

def index_exists(conn: connection, index_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM pg_indexes
                WHERE schemaname = 'public'
                AND indexname = %s
            ) AS exists;
        """, (index_name,))
        return cur.fetchone()["exists"]

def create_index(conn: connection, index_name: str, index_sql: str) -> None:
    """
    Create an index that apply to the database.

    Args:
        conn (connection): psql database connection handle.
        index_sql (str): sql string to apply the trigger.
    """
    if index_exists(conn, index_name):
        print(f"Index {index_name} already exists.")
        return
    with conn.cursor() as cur:
        cur.execute(index_sql)
    conn.commit()
    print(f"Index {index_name }created")

def initialize_schema(conn) -> None:
    """
    Ensures that all required tables exist. It should be called once at
    service initialization step.

    Args:
        conn (connection): psql connection handle.
    """

    create_table(conn, "ships", CREATE_SHIPS_TABLE)
    create_table(conn, "ship_types", CREATE_SHIP_TYPES_TABLE)
    create_table(conn, "ship_classes", CREATE_SHIP_CLASSES_TABLE)
    create_table(conn, "engine_types", CREATE_ENGINE_TYPES_TABLE)
    create_table(conn, "builders", CREATE_BUILDERS_TABLE)
    create_table(conn, "owners", CREATE_OWNERS_TABLE)
    create_table(conn, "ship_statuses", CREATE_STATUSES_TABLE)
    create_table(conn, "countries", CREATE_COUNTRIES_TABLE)

# EOF
