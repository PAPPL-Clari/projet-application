import psycopg2
import config

connection = psycopg2.connect(database="PAPPL", user= config.login, password=config.password, host="localhost", port=5432)

cursor = connection.cursor()

cursor.execute("SELECT * from diplome;")

# Fetch all rows from database
record = cursor.fetchall()

print("Data from Database:- ", record)
