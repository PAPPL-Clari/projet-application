#%%
import asyncio
import psycopg2
import config as config
from unidecode import unidecode
import json
from extractInfo.fetchData import fetchData_async
from extractInfo.getDiplomaInfo import getDiplomaInfo
from extractInfo.getUtilisateurInfo import getUtilisateurInfo
from extractInfo.getMailsInfo import getMailsInfo
from extractInfo.getAdressesInfo import getAdressesInfo
from datetime import datetime

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
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            # Prepare specialization name
            nom_specialisation = DiplomaInfo[0]["nom_specialisation"]
            nom_specialisation = nom_specialisation.replace("'", "''")  # Escape single quotes
            nom_specialisation = "'" + nom_specialisation + "'"

            if nom_specialisation != "''" and nom_specialisation not in specialisations:
                # Check if the specialization already exists
                check_sql = f"""
                SELECT id_specialisation FROM specialisation WHERE nom_specialisation = {nom_specialisation};
                """
                cursor.execute(check_sql)
                result = cursor.fetchone()

                if not result:  # Insert only if it does not exist
                    insert_sql = f"""
                    INSERT INTO specialisation (nom_specialisation)
                    VALUES ({nom_specialisation});
                    """
                    cursor.execute(insert_sql)
                    connection.commit()

                specialisations.append(nom_specialisation)

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
                    # Check if the specialization already exists
                    check_sql = f"""
                    SELECT id_type_utilisateur FROM type_utilisateur WHERE nom_type_utilisateur = {nom_type_utilisateur};
                    """
                    cursor.execute(check_sql)
                    result = cursor.fetchone()

                    if not result:  # Insert only if it does not exist
                        
                        sql = f"""
                        INSERT INTO type_utilisateur (nom_type_utilisateur)
                        VALUES ({nom_type_utilisateur});
                        """
                        type_utilisateurs.append(nom_type_utilisateur)
                        
                        cursor.execute(sql)
                        connection.commit()

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
                        types.append(nom)
                        # Check if the specialization already exists
                        check_sql = f"""
                        SELECT id_type FROM type WHERE nom_type = {nom};
                        """
                        cursor.execute(check_sql)
                        result = cursor.fetchone()

                        if not result:  # Insert only if it does not exist
                            sql = f"""
                            INSERT INTO type (nom_type)
                            VALUES ({nom});
                            """
                            cursor.execute(sql)
                            connection.commit()
    return types

#Add data type_adress to table "type"
def push_type_adress(infosUser, connection, cursor, types):
    for info in infosUser: 
        if '_embedded' in info:
            if 'address' in info["_embedded"]:
                #jprint(info)

                nom_type = getAdressesInfo(info["_embedded"]["address"]).keys()

                for nom in nom_type:
                    nom = nom.replace("'", "''")
                    nom = "'" + nom + "'"

                    if nom != "''" and nom not in types:
                        types.append(nom)
                        # Check if the specialization already exists
                        check_sql = f"""
                        SELECT id_type FROM type WHERE nom_type = {nom};
                        """
                        cursor.execute(check_sql)
                        result = cursor.fetchone()

                        if not result:  # Insert only if it does not exist
                            sql = f"""
                            INSERT INTO type (nom_type)
                            VALUES ({nom});
                            """
                            cursor.execute(sql)
                            connection.commit()
    return types

# Add data mail to table mail
def push_mail(infosUser, connection, cursor, types):
    mails = []

    # Recupera todos os tipos de ID
    idTypes = {}
    for type in types:
        sqlRecup = f"SELECT id_type FROM type WHERE nom_type={type}"
        cursor.execute(sqlRecup)
        result = cursor.fetchone()
        if result:
            idTypes[type] = result[0]

    for info in infosUser: 
        if '_embedded' in info and 'emails' in info["_embedded"]:
            infosMail = getMailsInfo(info["_embedded"]["emails"])

            for keyName in infosMail.keys():
                newMail = infosMail[keyName].replace("'", "''")  # Escape single quotes
                newMail = f"'{newMail}'"  # Wrap in quotes
                infosMail[keyName] = newMail
                keyName = f"'{keyName}'"

                if newMail != "''" and newMail not in mails:
                    # Verifica se o email já existe
                    check_sql = f"SELECT adresse_mail FROM mail WHERE adresse_mail = {newMail};"
                    cursor.execute(check_sql)
                    exists = cursor.fetchone()

                    if exists:
                        # Atualiza id_type se o email já existir
                        update_sql = f"""
                        UPDATE mail
                        SET id_type = {idTypes[keyName]}
                        WHERE adresse_mail = {newMail};
                        """
                        cursor.execute(update_sql)
                    else:
                        # Insere novo email
                        insert_sql = f"""
                        INSERT INTO mail (adresse_mail, id_type)
                        VALUES ({newMail}, {idTypes[keyName]});
                        """
                        cursor.execute(insert_sql)

                    mails.append(newMail)

    connection.commit()

# Add data mail to table ville
#def push_ville(infosUser, connection, cursor)


#%%
import nest_asyncio
nest_asyncio.apply()
#start_time = datetime.now()

infosDiploma = asyncio.run(fetchData_async("diploma"))
infosUser = asyncio.run(fetchData_async("profile"))

#end_time = datetime.now()

#%%
#print('Duration: {}'.format(end_time - start_time))

connection, cursor = init()
types = []

#push_specialisation(infosDiploma, connection, cursor)
#push_type_utilisateur(infosUser, connection, cursor)
types = push_type_mail(infosUser, connection, cursor, types)
types = push_type_adress(infosUser, connection, cursor, types)
push_mail(infosUser, connection, cursor, types)
cursor.close()