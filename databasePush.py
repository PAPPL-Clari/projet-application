import psycopg2
import config as config
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

def init():
    connection = psycopg2.connect(database=config.database,
                                user= config.login,
                                password=config.password,
                                host="localhost", port=5432)
    cursor = connection.cursor() # Open a cursor to perform database operations
    return connection, cursor

# Adds data to the table "specialisation"
def push_specialisation(infosDiploma, connection, cursor):
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

# Adds data to the table "type_utilisateur"
def push_type_utilisateur(infosUser, connection, cursor):
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

#Adds data type_mail to table "type"
def push_type_mail(infosUser, connection, cursor, types):
    
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
    return types

#Add data type_adress to table "type"
def push_type_adress(infosUser, connection, cursor, types):
    types = []
    for info in infosUser: 
        if '_embedded' in info:
            if 'address' in info["_embedded"]:
                #jprint(info)

                nom_type = getAdressesInfo(info["_embedded"]["address"]).keys()

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
    return types


#Add data mail to table mail
def push_mail(infosUser, connection, cursor, types):
    mails = []

    #Recupera all types id
    idTypes = dict()

    for type in types:
        cur = connection.cursor()
        
        sqlRecup = f"SELECT id_type from type WHERE nom_type={type}"

        cur.execute(sqlRecup)
        index = cur.fetchall()

        for id in index:
            id = id[0]
            idTypes.update({type: id})

        cur.close()

    print(idTypes)


    for info in infosUser: 
        if '_embedded' in info:
            if 'emails' in info["_embedded"]:

                infosMail = getMailsInfo(info["_embedded"]["emails"])
                print(infosMail)

                for keyName in infosMail.keys():
                    newMail = infosMail[keyName].replace("'", "''")
                    newMail = "'" + newMail + "'"
                    infosMail.update({keyName: newMail})

                    keyName = "'" + keyName + "'"

                    if newMail != "''" and newMail not in mails:
                        sql = f"INSERT INTO mail (adresse_mail, id_type) VALUES ({newMail}, {idTypes[keyName]});"
                        print(sql)
                        mails.append(newMail)

                        cur = connection.cursor()
                        cursor.execute(sql)
                        connection.commit()
                        cur.close()



def main():
    infosDiploma = fetchData("diploma")
    infosUser = fetchData("profile")
    connection, cursor = init()
    types = []
    
    #push_type_utilisateur(infosUser, connection, cursor)
    types = push_type_mail(infosUser, connection, cursor, types)
    types = push_type_adress(infosUser, connection, cursor, types)
    push_mail(infosUser, connection, cursor, types)
    cursor.close()
    
if __name__ == "__main__":
    main()