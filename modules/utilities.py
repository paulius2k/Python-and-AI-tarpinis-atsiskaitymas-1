import mysql.connector
import my_secrets

def connect_to_db():
    conn = mysql.connector.connect(
    host = "localhost",
    user = "paulius",
    passwd = my_secrets.MY_SQL_PSSW,
    database= "library_db"
    )
    
    return conn


