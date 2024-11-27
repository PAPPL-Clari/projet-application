import psycopg2
import config
from unidecode import unidecode
import json
from extractInfo.fetchData import fetchData
from extractInfo.getDiplomaInfo import getDiplomaInfo
from extractInfo.getUtilisateurInfo import getUtilisateurInfo
from extractInfo.getMailsInfo import getMailsInfo
from extractInfo.getAdressesInfo import getAdressesInfo

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

connection = psycopg2.connect(database=config.database,
                              user= config.login,
                              password=config.password,
                              host="localhost", port=5432)
cursor = connection.cursor() # Open a cursor to perform database operations


#Add data to the table "type utilisateur"
infosDiploma = fetchData("diploma")
infosUser = fetchData("profile")

specialisations = []

for info in infosDiploma: 
    if '_embedded' in info:
        if 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            #Put specialisation info in database
            nom_specialisation = DiplomaInfo[0]["nom_specialisation"]
            nom_specialisation = nom_specialisation.replace("'", "''")
            nom_specialisation = "'" + nom_specialisation + "'"
            
            if nom_specialisation != "''" and nom_specialisation not in specialisations:
                id_diplome = "\"" + DiplomaInfo[0]["id_diplome"] + "\""
                sql = f"INSERT INTO specialisation (id_specialisation, nom_specialisation) VALUES ({i},{nom_specialisation});"
                print(sql)
                
                cur = connection.cursor()
                specialisations.append(nom_specialisation)

                cursor.execute(sql)
                connection.commit()
                cur.close()

#Add data to the table "type utilisateur"

type_utilisateurs = []

for info in infosUser: 
    if '_embedded' in info:
     
     #Put type utilisateur info in database
        if 'type' in info["_embedded"]:
            nom_type_utilisateur = getUtilisateurInfo(info)
            nom_type_utilisateur = nom_type_utilisateur.replace("'", "''")
            nom_type_utilisateur = "'" + nom_type_utilisateur + "'"

            if nom_type_utilisateur != "''" and nom_type_utilisateur not in type_utilisateurs:
                sql = f"INSERT INTO type_utilisateur (id_type_utilisateur, nom_type_utilisateur) VALUES ({i},{nom_type_utilisateur});"
                print(sql)
                
                cur = connection.cursor()
                type_utilisateurs.append(nom_type_utilisateur)

                cursor.execute(sql)
                connection.commit()
                cur.close()

#Add data type_mail to table type (we need also to add type of address yet)
types = []

for info in infosUser: 
    if '_embedded' in info:
        if 'emails' in info["_embedded"]:
        
            nom_type = getMailsInfo(info["_embedded"]["emails"]).keys()

            for nom in nom_type:
                nom = nom.replace("'", "''")
                nom = "'" + nom + "'"

                if nom != "''" and nom not in types:
                    sql = f"INSERT INTO type (nom_type) VALUES ({nom});"
                    print(sql)
                    types.append(nom)

                    cur = connection.cursor()
                    cursor.execute(sql)
                    connection.commit()
                    cur.close()

# Close cursor and communication with the database
connection.close()
