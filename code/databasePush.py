#%%
import asyncio
import config
from unidecode import unidecode
import json
from extractInfo.fetchData import fetchData_async
from extractInfo.getDiplomaInfo import getDiplomaInfo
from extractInfo.getUtilisateurInfo import getUtilisateurInfo
from extractInfo.getMailsInfo import getMailsInfo
from extractInfo.getAdressesInfo import getAdressesInfo
from extractInfo.getPersonneInfo import getPersonneInfo
from datetime import datetime
import psycopg2

def jprint(obj):
    """
    Print JSON objet with identation.

    :param obj: A string in format JSON
    :return: returns nothing
    """

    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def format_name(city_name):
    """
    Format names in order to normalise data.
    Removes special characters, hifens and substitues single '' to double,
    Put every first character of a word with majuscule and the other minuscule.
    Ex: SUCE-SUR-ERDRE turns to Suce Sur Erdre

    :param name: A string
    :return: normalized_name: String 
    """
    city_name = unidecode(city_name)
    city_name = city_name.lower()
    city_name = city_name.replace('-', ' ')
    city_name = ' '.join(city_name.split())
    normalized_name = city_name.title()
    normalized_name = normalized_name.replace("'", "''")
    normalized_name = "'" + normalized_name + "'"

    return normalized_name

def format_adress(adress):
    """
    Format adress names in order to fit in 128 characters.
    :param adress: A string
    :return: adress: String with 128 characters

    """
    adress = format_name(adress)
    if (len(adress)> 127):
        adress = adress[:128]+ "'"
    return adress

def format_code_postal(code):
    """
    Format zip code in order to normalise data.
    Verifies if its an integer, if not, defines it as zero.

    :param name: A zip code, string format
    :return: modified code 
    """
    try:
        code = int(code[0:5])
        return code
    except ValueError:
        code = 0

    return code

def format(str):
    """
    Format a string in order to avoid SQL query errors.
    Remove special characters, replace single quotes to double ' -> ''
    and puts an initial ' in the beginning and end of the string.
    Ex: Côte d'Ivoire -> 'Cote d''Ivoire'

    :param str: A string
    :return: str: Modified string 
    """
    str = unidecode(str)
    str = str.replace("'", "''")
    str = "'" + str + "'"

    return str

def init():
    """
    Open a new connection with the local database.

    :param: None
    :return: connection: a connection objet to the database
    :return: cursor: cursor of the connexion
    """
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
    """
    Insert all specialisations in the table specialisation.
    Verifies duplicity of data and add if the specialisation doesn't exist.

    :param infosDiploma: List of all infos of Diploma in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    """
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
    """
    Insert all type of users in the table type_utilisateur.
    Verifies duplicity of data and add if the type doesn't exist.

    :param infosUser: List of all infos of Users in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    """
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
    """
    Insert all type of emails in the table type.
    Verifies duplicity of data and add if the type doesn't exist.

    :param infosUser: List of all infos of Users in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    :param types: array list of types already existing in the database
    :return types: array list of the types saved in the database
    """
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
    """
    Insert all type of adress in the table type.
    Verifies duplicity of data and add if the type doesn't exist.

    :param infosUser: List of all infos of Users in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    :param types: array list of types already existing in the database
    :return types: array list of the types saved in the database
    """
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
    """
    Insert all emails adress in the table mail.
    Verifies duplicity of data and add if the type doesn't exist.
    Doesn't update data.

    :param infosUser: List of all infos of Users in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    :param types: array list of types already existing in the database
    """
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
    """
    Insert all cities present in the API in the table ville.
    Verifies duplicity of data and add if the city doesn't exist.

    :param infosUser: List of all infos of Users in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    :return villes: List of cities present in the database
    """
    print("Ajout des villes à la base de données...")
    villes = []
    for info in infosUser: 
        if '_embedded' in info:
            if 'address' in info["_embedded"]:
                adresses = getAdressesInfo(info["_embedded"]["address"])

                for adresse in adresses:
                    ville = adresses[adresse]["ville"]
                    nom_pays = adresses[adresse]["nomPays"]

                    ville = format_name(ville)
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
    """
    Insert all adresses in the table adresse.
    Verifies duplicity of data and add if the main adress (adress 1) doesn't exist.

    :param infosUser: List of all infos of Users in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    :return list_adresses: array list of all adresses saved in the database (adress 1 to 4)
    """
    print("Ajout des adresses à la base de données...")

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
                    adresse1 = format_adress(adresse1)
                    adresse2 = format_adress(adresse2)
                    adresse3 = format_adress(adresse3)
                    adresse4 = format_adress(adresse4)
                    nom_ville = format_name(nom_ville)
                    code_postal = format_code_postal(code_postal)

                    user_id = int(info["id"])

                    nom_pays = "'" + nom_pays + "'"

                    if adresse1 != "''":
                        # Check if the main adress already exists
                        check_sql = f"""
                        SELECT adresse_id FROM adresse WHERE id_personne = {user_id};
                        """
                        cursor.execute(check_sql)
                        result_adress1 = cursor.fetchone()
                        
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
                    
                        if result_city and result_type:
                            result_city = result_city[0]
                            result_type = result_type[0]
                            type_adresse = format(adresse)

                            if not result_adress1 and code_postal != '':
                                # Insert new address if it does not exist
                                sql = f"""
                                INSERT INTO adresse (adresse_1, adresse_2, adresse_3, adresse_4, id_ville, npai, code_postal, type_adresse, id_type, id_personne)
                                VALUES ({adresse1}, {adresse2}, {adresse3}, {adresse4}, {result_city}, {npai}, {code_postal}, {type_adresse}, {result_type}, {user_id});
                                """
                                cursor.execute(sql)
                            else:
                                # Update existing address if it exists
                                sql = f"""
                                UPDATE adresse
                                SET adresse_1 = {adresse1}, 
                                    adresse_2 = {adresse2}, 
                                    adresse_3 = {adresse3}, 
                                    adresse_4 = {adresse4}, 
                                    id_ville = {result_city}, 
                                    npai = {npai}, 
                                    code_postal = {code_postal}, 
                                    type_adresse = {type_adresse}, 
                                    id_type = {result_type}
                                WHERE id_personne = {user_id};
                                """
                                cursor.execute(sql)

                            connection.commit()
    print("Succès à l'ajout des adresses à la base de données.")

#Add school data to table ecole
def push_ecoles(infosDiploma, connection, cursor):
    """
    Insert all schools in the table ecole.
    Verifies duplicity of data and add if the school doesn't exist.

    :param infosDiploma: List of all infos of Diplomas in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    """
    print("Ajout des écoles à la base de données...")
    ecoles = []

    for info in infosDiploma: 
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            # Prepare school name and country's acronymn
            nom_ecole = DiplomaInfo[0]["nom_ecole"]
            acronyme_pays = DiplomaInfo[0]["acronyme_pays_ecole"]

            nom_ecole = format_name(nom_ecole)
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


def push_personne(infosUser, connection, cursor):
    """
    Insert all users in the table personne.
    Verifies duplicity of data and add if the person doesn't exist.
    If the person already exists, updates the data.

    :param infosUser: List of all infos of Users in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    """
    print("Ajout des personnes à la base de données...")
    for user in infosUser:
        user_infos = user["_embedded"]["civil"]
        user_id = int(user_infos["id"])
        user_prenom = user_infos["firstname"]
        nom = user_infos["lastname"]
        nomUsage = user_infos["name_used"]
        if ( nomUsage == "lastname"):
            nomUsage = nom
        birthdate = user_infos["birthdate"]


#Add diplome data to table diplome
def push_diplome(infosDiploma, connection, cursor):
    """
    Insert all diplomas in the table diplome.
    Verifies duplicity of data and add if the diplome doesn't exist.

    :param infosDiploma: List of all infos of Diplomas in the API
    :param connection: Connection object to the database
    :param cursor: Cursor object of connection to the database
    """
    print("Ajout des diplomes à la base de données...")
    diplomes = []

    for info in infosDiploma: 
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            # Prepare school name and country's acronymn
            id_diplome = DiplomaInfo[0]["id_diplome"]
            ref_diploma = DiplomaInfo[0]["ref_diplome"]
            nom_specialisation = DiplomaInfo[0]["nom_specialisation"]
            nom_ecole = DiplomaInfo[0]["nom_ecole"]
            nom_diplome = DiplomaInfo[0]["nom_diplome"] 
            parcours = DiplomaInfo[0]["parcours"]

            ref_diploma = format(ref_diploma)
            nom_ecole = format_name(nom_ecole)
            nom_diplome = format_name(nom_diplome)
            parcours = format_name(parcours)

            nom_specialisation = format(nom_specialisation)

            if nom_diplome != "''" and nom_diplome not in diplomes:
                # Check if the diplome already exists
                check_sql = f"""
                SELECT id_diplome FROM diplome WHERE nom_diplome = {nom_diplome};
                """
                cursor.execute(check_sql)
                result = cursor.fetchone()

                # Search id for specialisation
                check_sql = f"""
                SELECT id_specialisation FROM specialisation WHERE nom_specialisation = {nom_specialisation};
                """
                cursor.execute(check_sql)
                result_spec = cursor.fetchone()

                #Search id for school
                check_sql = f"""
                SELECT id_ecole FROM ecole WHERE nom_ecole = {nom_ecole};
                """
                cursor.execute(check_sql)
                result_ecole = cursor.fetchone()

                if not result and result_spec and result_ecole:  # Insert only if it does not exist
                    id_specialisation = result_spec[0]
                    id_ecole = result_ecole[0]
                    sql = f"""
                            INSERT INTO diplome (id_diplome, ref_diploma, id_specialisation, id_ecole, 
                                                 nom_diplome, parcours)
                            VALUES ({id_diplome}, {ref_diploma}, {id_specialisation}, {id_ecole}, {nom_diplome}, {parcours});
                            """
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()

                    diplomes.append(nom_diplome)
    print("Succès à l'ajout des diplomes à la base de données.")

#%% Charge data from API

# Enables async calls to API requests
import nest_asyncio
nest_asyncio.apply()

# Starts timer
start_time = datetime.now()

# Charges needed data from API
infosDiploma = asyncio.run(fetchData_async("diploma"))
infosUser = asyncio.run(fetchData_async("profile"))

# Informs total duration of data gathering
end_time = datetime.now()
print("Duration recuperation de donnees de l'API: {}".format(end_time - start_time))

#%% Push data in database

# Establishes connection with database
connection, cursor = init()

# Starts timer
start_time = datetime.now()

# Populates tpecialisation and type_utilisateur tables 
push_specialisation(infosDiploma, connection, cursor)
push_type_utilisateur(infosUser, connection, cursor)

# Populates type and mail tables (this must be done in this order)
types = []
types = push_type_mail(infosUser, connection, cursor, types)
types = push_type_adress(infosUser, connection, cursor, types)
push_mail(infosUser, connection, cursor, types)

# Populates ville, adresse, ecole and diplome tables
push_ville(infosUser, connection, cursor)
# put push_personne here
push_adresse(infosUser, connection, cursor)
push_ecoles(infosDiploma, connection, cursor)
push_diplome(infosDiploma, connection, cursor)

# Ends connection with database
cursor.close()

# Mesures time needed to insert data into the database
end_time = datetime.now()
print('Durée de la mise à jour de la base de donnees: {}'.format(end_time - start_time))

# %%
