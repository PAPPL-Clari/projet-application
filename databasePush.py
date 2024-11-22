import psycopg2
import config
from unidecode import unidecode
import json
from extractInfo.fetchData import fetchData
from extractInfo.getDiplomaInfo import getDiplomaInfo

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

connection = psycopg2.connect(database=config.database,
                              user= config.login,
                              password=config.password,
                              host="localhost", port=5432)
cursor = connection.cursor()


# Open a cursor to perform database operations
cur = connection.cursor()

infos = fetchData(21)
jprint(infos)
DiplomaInfo = getDiplomaInfo(infos)

print("DiplomaInfo:", DiplomaInfo)

nom_specialisation = "\"" + DiplomaInfo[0]["nom_specialisation"] + "\""
sql = f"INSERT INTO specialisation (id_specialisation, nom_specialisation) VALUES (0, {nom_specialisation});"
print(sql)

cursor.execute(sql)
connection.commit()

# Make the changes to the database persistent
#conn.commit()
# Close cursor and communication with the database
cur.close()
connection.close()
