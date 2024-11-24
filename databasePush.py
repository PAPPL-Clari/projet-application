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

infos = fetchData()

specialisations = []
for info in infos: 
    if '_embedded' in info:
        if 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            nom_specialisation = DiplomaInfo[0]["nom_specialisation"]
            nom_specialisation = nom_specialisation.replace("'", "''")
            nom_specialisation = "'" + nom_specialisation + "'"
            
            if nom_specialisation != "''" and nom_specialisation not in specialisations:
                id_diplome = "\"" + DiplomaInfo[0]["id_diplome"] + "\""
                sql = f"INSERT INTO specialisation (nom_specialisation) VALUES ({nom_specialisation});"
                print(sql)
                
                cur = connection.cursor()
                specialisations.append(nom_specialisation)

                cursor.execute(sql)
                connection.commit()
                cur.close()

# Make the changes to the database persistent
#conn.commit()
# Close cursor and communication with the database

connection.close()
