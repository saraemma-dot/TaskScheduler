import sqlite3 
from typing import Generator


def get_db()->Generator [sqlite3.Connection,None,None]:
    connection=sqlite3.connect('eventscheduler.db')
    try:       
        print('connection to db has been established')
        yield connection #gives the resource to the endpoint

    finally :
        connection.close()
        print('db connection has been closed')