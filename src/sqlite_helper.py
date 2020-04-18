import logging
import os
import sqlite3
from sqlite3 import Error

from src.database_resources import DDL


def get_connection(path=None):
    if not path:
        path = os.path.join(os.path.dirname(__file__), "sample.sqlite")

    connection = None
    try:
        connection = sqlite3.connect(path)
        logging.info("Connection to SQLite is successful")
    except Error as err:
        logging.error(f"Connection to SQLite failed with {err} ")

    return connection


def exeute_query(sql_cmd):
    conn = get_connection()
    this_cursor = conn.cursor()
    result_set = None
    try:
        this_cursor.execute(sql_cmd)
        conn.commit()
        logging.info("The SQL command runs successfully")
        result_set = this_cursor.fetchall()
        return result_set
    except Error as err:
        logging.error(f"The SQL command fails with {err}")

def drop_message_table():
    exeute_query(DDL.drop_message_table)

def create_message_table():
    exeute_query(DDL.create_message_table)
