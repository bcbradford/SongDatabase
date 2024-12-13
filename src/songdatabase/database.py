''' Database wrapper class for an sqlite database '''

import os
import sqlite3
from songdatabase.errors.database_error import *

class Database():

    def __init__(self, db_path: str, config: dict, logger: "logger") -> "Database":
        self._db_path = db_path
        self._config = config
        self._logger = logger
        self._connection = None

    def _lazy_connect(self):
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(self._db_path)
            except Exception as e:
                desc = "Failed to connect to the database."
                logger_output = f"Lazy connect failed: {e}"
                raise DatabaseConnectionError(desc, logger_output)

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute(self, query, params=None):
        self._lazy_connect()
        if params is None: params = ()

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
            self._connection.commit()
        except Exception as e:
            self._raise_query_error(query, params, e)

    def select_all(self, query, params=None):
        self._lazy_connect()
        if params is None: params = ()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
            return results
        except Exception as e:
            self._raise_query_error(query, params, e)

    def _raise_query_error(self, query, params, e):
        desc = "Failed to execute query."
        logger_output = f"{query}\nFailed to execute with params: {params}\nException: {e}"
        raise DatabaseQueryError(desc, logger_output)


def init_database(config: dict, logger: "logger") -> None:
    db_path = config['database']
    try:
        if not __database_exists(db_path):
            __create_tables(config, db_path, logger)

        db = Database(db_path, config, logger)
        return db
    except Exception as e:
        desc = "Failed to init the database."
        logger_output = f"Database {db_path} init failed: {e}"
        raise DatabaseInitError(desc, logger_output)

def __database_exists(db_path) -> bool:
    if not os.path.exists(db_path): return False
    return True

def __create_tables(config: dict, db_path, logger) -> None:
    with sqlite3.connect(db_path) as cursor:
        for _, table_dict in config['database_tables'].items():
            query = __create_table_query(table_dict)
            logger.info(f"Executing Query:\n{query}")
            cursor.execute(query)

def __create_table_query(table_dict):
    table_name = table_dict['name']
    query_string = f"CREATE TABLE {table_name} (\n"

    columns = []
    for _, param_list in table_dict['columns'].items():
        col = f"{' '.join(param_list)}"
        columns.append(col)

    # remove , \n
    query_string += ",\n".join(columns)
    query_string += "\n);"
    return query_string

if __name__ == '__main__':
    print('Usage: python3 app.py')
