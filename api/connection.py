import mysql.connector
import os

host = os.getenv("HOST", "localhost")

port = int(os.getenv("PORT", "3306"))
user = os.getenv("USER", "root")
password = os.getenv("PASSWORD", "root")
database = os.getenv("DATABASE", "digital_hunter")

config = {
  "host": host,
  "port": port,
  "user": user,
  "password": password,
  "database": database
}

def get_conn():
  return mysql.connector.connect(**config)