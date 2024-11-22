import psycopg2
import config
import getDiplomaInfo
from unidecode import unidecode

#Creation d'une nouvelle connection
connection = psycopg2.connect(database=config.database, user= config.login, password=config.password, host="localhost", port=5432)
cursor = connection.cursor()

#Demande des resultats
id = 21 ##Correspond a M Gautier

(id_diplome, ref_diplome, nom_diplome, parcours,
 nom_specialisation,
 nom_ecole, acronyme_pays_ecole) = getDiplomaInfo.getDiplomaInfo(id)

# Execute a insert command
val = unidecode(nom_specialisation) #Remove the accents from the word
sql = f"INSERT INTO specialisation (id_specialisation, nom_specialisation) VALUES (0, {val});"
print(sql)

cursor.execute(sql)
connection.commit()


#Execute a SELECT command
cursor.execute("SELECT * from specialisation;")
record = cursor.fetchall()
print("Data from Database:- ", record)