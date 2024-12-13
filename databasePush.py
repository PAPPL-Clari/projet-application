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

def format_city_name(city_name):
    city_name = unidecode(city_name)
    city_name = city_name.lower()
    city_name = city_name.replace('-', ' ')
    city_name = ' '.join(city_name.split())
    normalized_name = city_name.title()
    normalized_name = normalized_name.replace("'", "''")
    normalized_name = "'" + normalized_name + "'"

    return normalized_name

def format_code_postal(code_postal):
    code_postal = unidecode(code_postal)
    str = str.replace("'", "''")
    str = "'" + str + "'"

    return str

def format(str):
    str = unidecode(str)
    str = str.replace("'", "''")
    str = "'" + str + "'"

    return str

def init():
    print("Établissement de la connexion à la base de données...")
    connection = psycopg2.connect(database=config.database,
                                user= config.login,
                                password=config.password,
                                host="localhost", port=5432)
    cursor = connection.cursor() # Open a cursor to perform database operations
    print("Connexion à la base de données établi.")

    return connection, cursor

# Adds data to the table "specialisation"
def push_specialisation(infosDiploma, connection, cursor):
    print("Ajout des specialisations à la base de données...")
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
    print("Succès à l'ajout des specialisations à la base de données.")

# Adds data to the table "type_utilisateur"
def push_type_utilisateur(infosUser, connection, cursor):
    print("Ajout des types d'utilisateur à la base de données...")
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
    print("Succès à l'ajout des types d'utilisateur à la base de données.")

#Adds data type_mail to table "type"
def push_type_mail(infosUser, connection, cursor, types):
    print("Ajout des types de mail à la base de données...")
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
    print("Succès à l'ajout des types de mail à la base de données.")
    return types

#Add data type_adress to table "type"
def push_type_adress(infosUser, connection, cursor, types):
    print("Ajout des types d'adresse à la base de données...")
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
    print("Succès à l'ajout des types d'adresse à la base de données.")
    return types

# Add data mail to table mail
def push_mail(infosUser, connection, cursor, types):
    print("Ajout des données de mail à la base de données...")
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

    print("Succès à l'ajout des mails à la base de données.")
    connection.commit()

# Add city data to table ville
def push_ville(infosUser, connection, cursor):
    print("Ajout des villes à la base de données...")
    villes = []
    for info in infosUser: 
        if '_embedded' in info:
            if 'address' in info["_embedded"]:
                #jprint(info)

                adresses = getAdressesInfo(info["_embedded"]["address"])

                for adresse in adresses:
                    ville = adresses[adresse]["ville"]
                    nom_pays = adresses[adresse]["nomPays"]

                    ville = format_city_name(ville)
                    nom_pays = "'" + nom_pays + "'"

                    if ville != "''" and ville not in villes:
                        villes.append(ville)
                        
                        # Check if the city already exists
                        check_sql = f"""
                        SELECT id_ville FROM ville WHERE nom_ville = {ville};
                        """
                        cursor.execute(check_sql)
                        result = cursor.fetchone()

                        #Check if the country exists
                        check_sql = f"""
                        SELECT acronyme_pays FROM pays WHERE nom_pays = {nom_pays};
                        """
                        cursor.execute(check_sql)
                        result_pays = cursor.fetchone()

                        if not result and result_pays:  # Insert only if it does not exist
                            pays = format(result_pays[0])
  
                            sql = f"""
                            INSERT INTO ville (nom_ville, acronyme_pays)
                            VALUES ({ville}, {pays});
                            """
                            cursor.execute(sql)
                            connection.commit()
    print("Succès à l'ajout des villes à la base de données.")
    return villes

# Add address data to table adresse
def push_adresse(infosUser, connection, cursor):
    print("Ajout des adresses à la base de données...")
    list_adresses = []

    for info in infosUser: 
        if '_embedded' in info:
            if 'address' in info["_embedded"]:
                #jprint(info)

                adresses = getAdressesInfo(info["_embedded"]["address"])

                for adresse in adresses:
                    
                    adresse1 = adresses[adresse]["adresse_1"]
                    adresse2 = adresses[adresse]["adresse_2"]
                    adresse3 = adresses[adresse]["adresse_3"]
                    adresse4 = adresses[adresse]["adresse_4"]
                    code_postal = adresses[adresse]["code_postal"]
                    npai = adresses[adresse]["npai"]
                    nom_ville = adresses[adresse]["ville"]
                    nom_pays = adresses[adresse]["nomPays"]
                    
                    type = format(adresse)
                    adresse1 = format_city_name(adresse1)
                    adresse2 = format_city_name(adresse2)
                    adresse3 = format_city_name(adresse3)
                    adresse4 = format_city_name(adresse4)
                    #code_postal = format_code_postal(code_postal)
                    nom_ville = format_city_name(nom_ville)

                    nom_pays = "'" + nom_pays + "'"
                    #print(adresse1, adresse2, adresse3, adresse4, code_postal, npai, nom_ville, nom_pays)
                    condition = (adresse1 != "''" and adresse1 not in list_adresses) and (adresse2 != "''" and adresse2 not in list_adresses) and (adresse3 != "''" and adresse3 not in list_adresses) and (adresse4 != "''" and adresse4 not in list_adresses) and code_postal != ''
                    
                    if condition:
                        list_adresses.append(adresse1)
                        list_adresses.append(adresse2)
                        list_adresses.append(adresse3)
                        list_adresses.append(adresse4)
                        
                        # Check if the adress already exists
                        '''check_sql = f"""
                        SELECT adresse_id FROM adresse WHERE adresse_1 = {adresse1};
                        """
                        cursor.execute(check_sql)
                        result_adress = cursor.fetchone()'''

                        #Check if the city exists
                        check_sql = f"""
                        SELECT id_ville FROM ville WHERE nom_ville = {nom_ville};
                        """
                        cursor.execute(check_sql)
                        result_city = cursor.fetchone()

                        #Check if the type exists
                        check_sql = f"""
                        SELECT id_type FROM type WHERE nom_type = {type};
                        """
                        cursor.execute(check_sql)
                        result_type = cursor.fetchone()

                        #print(result_adress, result_city, result_type)

                        if result_city != None and result_type != None:  # Insert only if it does not exist
                            result_city = result_city[0]
                            result_type = result_type[0]
                            type_adresse = format(adresse)
                            sql = f"""
                            INSERT INTO adresse (adresse_1, adresse_2, adresse_3, adresse_4, id_ville, npai, code_postal, type_adresse, id_type)
                            VALUES ({adresse1}, {adresse2}, {adresse3}, {adresse4}, {result_city}, {npai}, {code_postal}, {type_adresse}, {result_type});
                            """
                            #print(sql)
                            cursor.execute(sql)
                            connection.commit()
    print("Succès à l'ajout des adresses à la base de données.")
    return adresses

#Add school data to table ecole
def push_ecoles(infosDiploma, connection, cursor):
    print("Ajout des écoles à la base de données...")
    ecoles = []

    for info in infosDiploma: 
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            # Prepare school name and country's acronymn
            nom_ecole = DiplomaInfo[0]["nom_ecole"]
            acronyme_pays = DiplomaInfo[0]["acronyme_pays_ecole"]

            nom_ecole = format_city_name(nom_ecole)
            acronyme_pays = format(acronyme_pays)

            if nom_ecole != "''" and nom_ecole not in ecoles:
                # Check if the school already exists
                check_sql = f"""
                SELECT id_ecole FROM ecole WHERE nom_ecole = {nom_ecole};
                """
                cursor.execute(check_sql)
                result = cursor.fetchone()

                # Check if the country already exists
                check_sql = f"""
                SELECT nom_pays FROM pays WHERE acronyme_pays = {acronyme_pays};
                """
                cursor.execute(check_sql)
                result_pays = cursor.fetchone()

                if not result and result_pays:  # Insert only if it does not exist
                    sql = f"""
                            INSERT INTO ecole (nom_ecole, acronyme_pays)
                            VALUES ({nom_ecole}, {acronyme_pays});
                            """
                    cursor.execute(sql)
                    connection.commit()

                    ecoles.append(nom_ecole)
    print("Succès à l'ajout des ecoles à la base de données.")

#%% Charge data from API
import nest_asyncio
nest_asyncio.apply()
start_time = datetime.now()

infosDiploma = asyncio.run(fetchData_async("diploma"))
infosUser = asyncio.run(fetchData_async("profile"))

end_time = datetime.now()
print('Duration recuperation de donnees de l''API: {}'.format(end_time - start_time))

#%% Push data in database

connection, cursor = init()
types = []
villes = []
adresses = []

start_time = datetime.now()

push_specialisation(infosDiploma, connection, cursor)
push_type_utilisateur(infosUser, connection, cursor)
types = push_type_mail(infosUser, connection, cursor, types)
types = push_type_adress(infosUser, connection, cursor, types)
push_mail(infosUser, connection, cursor, types)
villes = push_ville(infosUser, connection, cursor)
adresses= push_adresse(infosUser, connection, cursor)
push_ecoles(infosDiploma, connection, cursor)
cursor.close()

end_time = datetime.now()
print('Duration de la mise en base de donnees: {}'.format(end_time - start_time))


# %%
