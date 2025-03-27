import mysql.connector
import credentials
from mysql.connector import Error
from sqlstuffs import create_connection
from sqlstuffs import execute_query
from sqlstuffs import execute_read_query

#creating connection to mysql db
myCreds = credentials.Credentials()
conn = create_connection(myCreds.constring, myCreds.username,myCreds.password, myCreds.dbname)
