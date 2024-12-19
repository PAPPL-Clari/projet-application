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
from extractInfo.format import format_str, format_name, format_adress, format_code_postal

def init():
    """
    Ouvre une nouvelle connexion avec la base de données locale.

    :param : None
    :return : connection : un objet de connexion à la base de données
    :return : cursor : curseur de la connexion
    """
    print("Établissement de la connexion à la base de données...")
    connection = psycopg2.connect(database=config.database,
                                user= config.login,
                                password=config.password,
                                host="localhost", port=5432)
    cursor = connection.cursor() # Ouvrir un curseur pour effectuer des opérations sur la base de données
    print("Connexion à la base de données établi.")

    return connection, cursor

# Ajoute des données à la table « specialisation »
def push_specialisation(infosDiploma, connection, cursor):
    """
    Insère toutes les spécialisations dans la table « spécialisation ».
    Vérifie la duplicité des données et ajoute si la spécialisation n'existe pas.

    :param infosDiplôme : Liste de toutes les informations relatives aux diplômes dans l'API
    :param connection : Objet de connexion à la base de données
    :param cursor : Objet curseur de la connexion à la base de données
    """
    print("Ajout des specialisations à la base de données...")
    specialisations = []

    for info in infosDiploma: 
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            # Prepare le nom de la specialisation 
            nom_specialisation = DiplomaInfo[0]["nom_specialisation"]
            nom_specialisation = format_str(nom_specialisation)

            if nom_specialisation != "''" and nom_specialisation not in specialisations:
                # Vérifier si la spécialisation existe déjà
                check_sql = f"""
                SELECT id_specialisation FROM specialisation WHERE nom_specialisation = {nom_specialisation};
                """
                cursor.execute(check_sql)
                result = cursor.fetchone()

                if not result:  # Insérer uniquement s'il n'existe pas
                    insert_sql = f"""
                    INSERT INTO specialisation (nom_specialisation)
                    VALUES ({nom_specialisation});
                    """
                    cursor.execute(insert_sql)
                    connection.commit()

                specialisations.append(nom_specialisation)
    print("Succès à l'ajout des specialisations à la base de données.")

# Ajoute des données à la table « type_utilisateur »
def push_type_utilisateur(infosUser, connection, cursor):
    """
    Insérer tous les types d'utilisateurs dans la table type_utilisateur.
    Vérifie la duplicité des données et ajoute si le type n'existe pas.

    param infosUser : Liste de toutes les infos des utilisateurs dans l'API
    :param connection : Objet de connexion à la base de données
    :param cursor : Objet curseur de la connexion à la base de données
    """
    print("Ajout des types d'utilisateur à la base de données...")
    type_utilisateurs = []

    for info in infosUser: 
        if '_embedded' in info:
        
        # Mettre l'information sur le type d'utilisateur dans la base de données
            if 'type' in info["_embedded"]:
                nom_type_utilisateur = getUtilisateurInfo(info)
                nom_type_utilisateur = nom_type_utilisateur.replace("'", "''")
                nom_type_utilisateur = "'" + nom_type_utilisateur + "'"

                if nom_type_utilisateur != "''" and nom_type_utilisateur not in type_utilisateurs:
                    # Vérifier si le type existe déjà
                    check_sql = f"""
                    SELECT id_type_utilisateur FROM type_utilisateur WHERE nom_type_utilisateur = {nom_type_utilisateur};
                    """
                    cursor.execute(check_sql)
                    result = cursor.fetchone()

                    if not result:  # Insérer uniquement s'il n'existe pas
                        
                        sql = f"""
                        INSERT INTO type_utilisateur (nom_type_utilisateur)
                        VALUES ({nom_type_utilisateur});
                        """
                        type_utilisateurs.append(nom_type_utilisateur)
                        
                        cursor.execute(sql)
                        connection.commit()

    print("Succès à l'ajout des types d'utilisateur à la base de données.")

# Ajoute les données type_mail à la table « type »
def push_type_mail(infosUser, connection, cursor, types):
    """
    Insère tous les types d'emails dans la table type.
    Vérifie la duplicité des données et ajoute si le type n'existe pas.

    param infosUser : Liste de toutes les informations sur les utilisateurs dans l'API
    :param connection : Objet de connexion à la base de données
    :param cursor : Objet curseur de la connexion à la base de données
    :param types : tableau liste des types déjà existants dans la base de données
    :return types : tableau liste des types sauvegardés dans la base de données
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
                        # Vérifier si le type existe déjà
                        check_sql = f"""
                        SELECT id_type FROM type WHERE nom_type = {nom};
                        """
                        cursor.execute(check_sql)
                        result = cursor.fetchone()

                        if not result:  # Insérer uniquement s'il n'existe pas
                            sql = f"""
                            INSERT INTO type (nom_type)
                            VALUES ({nom});
                            """
                            cursor.execute(sql)
                            connection.commit()
    print("Succès à l'ajout des types de mail à la base de données.")
    return types

# Ajouter les données type_adresse à la table « type »
def push_type_adress(infosUser, connection, cursor, types):
    """
    Insère tous les types d'adresses dans la table type.
    Vérifie la duplicité des données et ajoute si le type n'existe pas.

    param infosUser : Liste de toutes les informations sur les utilisateurs dans l'API
    :param connection : Objet de connexion à la base de données
    :param cursor : Objet curseur de la connexion à la base de données
    :param types : tableau liste des types déjà existants dans la base de données
    :return types : tableau liste des types sauvegardés dans la base de données
    """
    print("Ajout des types d'adresse à la base de données...")
    for info in infosUser: 
        if '_embedded' in info:
            if 'address' in info["_embedded"]:

                nom_type = getAdressesInfo(info["_embedded"]["address"]).keys()

                for nom in nom_type:
                    nom = nom.replace("'", "''")
                    nom = "'" + nom + "'"

                    if nom != "''" and nom not in types:
                        types.append(nom)
                        # Vérifier si le type existe déjà
                        check_sql = f"""
                        SELECT id_type FROM type WHERE nom_type = {nom};
                        """
                        cursor.execute(check_sql)
                        result = cursor.fetchone()

                        if not result:  # Insérer uniquement s'il n'existe pas
                            sql = f"""
                            INSERT INTO type (nom_type)
                            VALUES ({nom});
                            """
                            cursor.execute(sql)
                            connection.commit()
    print("Succès à l'ajout des types d'adresse à la base de données.")
    return types

# Ajouter les données mail au tableau mail
def push_mail(infosUser, connection, cursor, types):
    """
    Insère toutes les adresses électroniques dans la table mail.
    Vérifie la duplicité des données et ajoute si le type n'existe pas.
    Met à jour les données existantes si nécessaire.

    :param infosUser : Liste de toutes les infos des utilisateurs dans l'API
    :param connection : Objet de connexion à la base de données
    :param cursor : Objet curseur de la connexion à la base de données
    :param types : Liste des types existants dans la base de données
    """
    print("Ajout ou mise à jour des données de mail à la base de données...")
    mails = []

    # Récupérer tous les types d'id
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
                newMail = f"'{newMail}'"  # Entre guillemets
                infosMail[keyName] = newMail
                keyName = f"'{keyName}'"

                if newMail != "''" and newMail not in mails:
                    # Vérifier si le mail existe déjà
                    check_sql = f"SELECT adresse_mail FROM mail WHERE adresse_mail = {newMail};"
                    cursor.execute(check_sql)
                    exists = cursor.fetchone()

                    if exists:
                        # Met à jour l'id_type si l'email existe déjà
                        update_sql = f"""
                        UPDATE mail
                        SET id_type = {idTypes[keyName]}
                        WHERE adresse_mail = {newMail};
                        """
                        cursor.execute(update_sql)
                    else:
                        # Insérer le nouvel e-mail
                        insert_sql = f"""
                        INSERT INTO mail (adresse_mail, id_type)
                        VALUES ({newMail}, {idTypes[keyName]});
                        """
                        cursor.execute(insert_sql)

                    mails.append(newMail)

    print("Succès à l'ajout ou mise à jour des mails à la base de données.")
    connection.commit()

# Ajouter les données de la ville au tableau ville
def push_ville(infosUser, connection, cursor):
    """
    Insère toutes les villes présentes dans l'API dans la table ville.
    Vérifie la duplicité des données et ajoute si la ville n'existe pas.

    param infosUser : Liste de toutes les informations sur les utilisateurs de l'API
    :param connection : Objet de connexion à la base de données
    :param cursor : Objet curseur de la connexion à la base de données
    :return villes : Liste des villes présentes dans la base de données
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
                        
                        # Vérifier si la ville existe déjà
                        check_sql = f"""
                        SELECT id_ville FROM ville WHERE nom_ville = {ville};
                        """
                        cursor.execute(check_sql)
                        result = cursor.fetchone()

                        # Vérifier si le pays existe
                        check_sql = f"""
                        SELECT acronyme_pays FROM pays WHERE nom_pays = {nom_pays};
                        """
                        cursor.execute(check_sql)
                        result_pays = cursor.fetchone()

                        if not result and result_pays:  # Insérer uniquement si la ville n'existe pas et que le pays existe.
                            pays = format_str(result_pays[0])
  
                            sql = f"""
                            INSERT INTO ville (nom_ville, acronyme_pays)
                            VALUES ({ville}, {pays});
                            """
                            cursor.execute(sql)
                            connection.commit()
    print("Succès à l'ajout des villes à la base de données.")
    return villes

# Ajouter des adresses dans la table adresse
def push_adresse(infosUser, connection, cursor):
    """
    Insère toutes les adresses dans la table 'adresse'.
    Vérifie les doublons de données et ajoute l'adresse principale (adresse 1) si elle n'existe pas.
    Met à jour les données existantes si nécessaire.

    :param infosUser: Liste contenant toutes les informations des utilisateurs provenant de l'API.
    :param connection: Objet de connexion à la base de données.
    :param cursor: Objet curseur pour exécuter les requêtes SQL.
    :return list_adresses: Tableau contenant toutes les adresses sauvegardées dans la base de données (adresse 1 à 4).
    """
    print("Ajout ou mise à jour des adresses à la base de données...")

    for info in infosUser: 
        if '_embedded' in info:
            if 'address' in info["_embedded"]:

                # Récupération des informations d'adresse
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
                    
                    # Formatage des données
                    type = format_str(adresse)
                    adresse1 = format_adress(adresse1)
                    adresse2 = format_adress(adresse2)
                    adresse3 = format_adress(adresse3)
                    adresse4 = format_adress(adresse4)
                    nom_ville = format_name(nom_ville)
                    code_postal = format_code_postal(code_postal)

                    user_id = int(info["id"])

                    nom_pays = "'" + nom_pays + "'"

                    if adresse1 != "''":
                        # Vérifier si l'adresse principale existe déjà
                        check_sql = f"""
                        SELECT adresse_id FROM adresse WHERE id_personne = {user_id};
                        """
                        cursor.execute(check_sql)
                        result_adress1 = cursor.fetchone()
                        
                        # Vérifier si la ville existe déjà
                        check_sql = f"""
                        SELECT id_ville FROM ville WHERE nom_ville = {nom_ville};
                        """
                        cursor.execute(check_sql)
                        result_city = cursor.fetchone()

                        # Vérifier si le type d'adresse existe déjà
                        check_sql = f"""
                        SELECT id_type FROM type WHERE nom_type = {type};
                        """
                        cursor.execute(check_sql)
                        result_type = cursor.fetchone()
                    
                        if result_city and result_type:
                            result_city = result_city[0]
                            result_type = result_type[0]
                            type_adresse = format_str(adresse)

                            if not result_adress1 and code_postal != '':
                                # Insérer une nouvelle adresse si elle n'existe pas
                                sql = f"""
                                INSERT INTO adresse (adresse_1, adresse_2, adresse_3, adresse_4, id_ville, npai, code_postal, type_adresse, id_type, id_personne)
                                VALUES ({adresse1}, {adresse2}, {adresse3}, {adresse4}, {result_city}, {npai}, {code_postal}, {type_adresse}, {result_type}, {user_id});
                                """
                                cursor.execute(sql)
                            else:
                                # Mettre à jour l'adresse existante si elle existe déjà
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
    print("Succès à l'ajout ou mise à jour des adresses à la base de données.")

# Ajouter les données des écoles dans la table ecole
def push_ecoles(infosDiploma, connection, cursor):
    """
    Insère toutes les écoles dans la table 'ecole'.
    Vérifie les doublons de données et ajoute si l'école n'existe pas.

    :param infosDiploma: Liste contenant toutes les informations des diplômes depuis l'API.
    :param connection: Objet de connexion à la base de données.
    :param cursor: Objet curseur pour exécuter les requêtes SQL.
    """
    print("Ajout des écoles à la base de données...")
    ecoles = []

    for info in infosDiploma: 
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            # Préparer le nom de l'école et l'acronyme du pays
            nom_ecole = DiplomaInfo[0]["nom_ecole"]
            acronyme_pays = DiplomaInfo[0]["acronyme_pays_ecole"]

            nom_ecole = format_name(nom_ecole)
            acronyme_pays = format_str(acronyme_pays)

            if nom_ecole != "''" and nom_ecole not in ecoles:
                # Vérifier si l'école existe déjà
                check_sql = f"""
                SELECT id_ecole FROM ecole WHERE nom_ecole = {nom_ecole};
                """
                cursor.execute(check_sql)
                result = cursor.fetchone()

                # Vérifier si le pays existe déjà
                check_sql = f"""
                SELECT nom_pays FROM pays WHERE acronyme_pays = {acronyme_pays};
                """
                cursor.execute(check_sql)
                result_pays = cursor.fetchone()

                if not result and result_pays:  # Insérer uniquement si elle n'existe pas
                    sql = f"""
                            INSERT INTO ecole (nom_ecole, acronyme_pays)
                            VALUES ({nom_ecole}, {acronyme_pays});
                            """
                    cursor.execute(sql)
                    connection.commit()

                    ecoles.append(nom_ecole)
    print("Succès de l'ajout des écoles à la base de données.")


# Ajouter les données des personnes dans la table personne
def push_personne(infosUser, connection, cursor):
    """
    Insère ou met à jour les personnes dans la table 'personne'.
    Vérifie les doublons de données, ajoute les nouvelles personnes,
    et met à jour les données existantes si nécessaire.

    :param infosUser: Liste contenant toutes les informations des utilisateurs depuis l'API.
    :param connection: Objet de connexion à la base de données.
    :param cursor: Objet curseur pour exécuter les requêtes SQL.
    """
    print("Ajout ou mise à jour des personnes dans la base de données...")
    for info in infosUser: 
        if '_embedded' in info and 'civil' in info["_embedded"] and 'type' in info["_embedded"] and 'address' in info["_embedded"]:
            personneInfo = getPersonneInfo(info)
            
            user_id = personneInfo["id_personne"]

            # Vérifier si la personne existe déjà
            check_sql = f"""
            SELECT id_personne FROM personne WHERE id_personne = {user_id};
            """
            cursor.execute(check_sql)
            personne = cursor.fetchone()

            # Vérifier si le pays existe déjà
            check_sql = f"""
            SELECT acronyme_pays FROM pays WHERE UPPER(nom_pays) = UPPER({personneInfo["nationalite"]});
            """
            cursor.execute(check_sql)
            result_pays = cursor.fetchone()
            if result_pays:
                result_pays = result_pays[0]
                result_pays = format_str(result_pays)
            else:
                result_pays = 'NULL'

            # Vérifier si la ville existe déjà
            check_sql = f"""
            SELECT id_ville FROM ville WHERE nom_ville = {personneInfo["ville"]};
            """
            cursor.execute(check_sql)
            result_ville = cursor.fetchone()
            if result_ville:
                result_ville = result_ville[0]
            else:
                result_ville = 'NULL'

            # Vérifier l'id_type_utilisateur
            check_sql = f"""
            SELECT id_type_utilisateur FROM type_utilisateur WHERE nom_type_utilisateur = {personneInfo["nom_type_utilisateur"]};
            """
            cursor.execute(check_sql)
            result_type = cursor.fetchone()
            result_type = result_type[0]

            if not personne:  # Insérer uniquement si la personne n'existe pas
                sql = f"""
                        INSERT INTO personne (id_personne, prenom, nom, nom_usage, date_naissance, ref_school, civilite, id_ville, adresse_mail, id_type_utilisateur, acronyme_pays, derniere_mise_a_jour)
                        VALUES ({personneInfo['id_personne']}, {personneInfo['prenom']}, {personneInfo['nom']}, {personneInfo['nomUsage']}, {personneInfo['dateNaissance']}, {personneInfo['school_ref']}, 
                                {personneInfo['civilite']}, {result_ville}, {personneInfo['mail']}, {result_type}, {result_pays}, {personneInfo['miseAJour']});
                        """
                cursor.execute(sql)
            else:  # Mettre à jour les données si la personne existe
                sql = f"""
                        UPDATE personne
                        SET prenom = {personneInfo['prenom']},
                            nom = {personneInfo['nom']},
                            nom_usage = {personneInfo['nomUsage']},
                            date_naissance = {personneInfo['dateNaissance']},
                            ref_school = {personneInfo['school_ref']},
                            civilite = {personneInfo['civilite']},
                            id_ville = {result_ville},
                            adresse_mail = {personneInfo['mail']},
                            id_type_utilisateur = {result_type},
                            acronyme_pays = {result_pays},
                            derniere_mise_a_jour = {personneInfo['miseAJour']}
                        WHERE id_personne = {personneInfo['id_personne']};
                        """
                cursor.execute(sql)
            
            connection.commit()

    print("Succès de l'ajout ou mise à jour des personnes dans la base de données.")

# Ajouter les données des diplômes à la table diplome
def push_diplome(infosDiploma, connection, cursor):
    """
    Insère tous les diplômes dans la table diplome.
    Vérifie la duplication des données et ajoute si le diplôme n'existe pas.

    :param infosDiploma: Liste de toutes les informations sur les diplômes de l'API
    :param connection: Objet de connexion à la base de données
    :param cursor: Objet curseur de la connexion à la base de données
    """
    print("Ajout des diplômes à la base de données...")
    diplomes = []

    for info in infosDiploma: 
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)

            for i in range(len(DiplomaInfo)):
                # Préparation des noms d'école et acronymes de pays
                ref_diploma = DiplomaInfo[i]["ref_diplome"]
                nom_specialisation = DiplomaInfo[i]["nom_specialisation"]
                nom_ecole = DiplomaInfo[i]["nom_ecole"]
                nom_diplome = DiplomaInfo[i]["nom_diplome"] 
                parcours = DiplomaInfo[i]["parcours"]

                ref_diploma = format_str(ref_diploma)
                nom_ecole = format_name(nom_ecole)
                nom_diplome = format_name(nom_diplome)
                parcours = format_name(parcours)
                nom_specialisation = format_str(nom_specialisation)

                if nom_diplome != "''":
                    # Vérifie si le diplôme existe déjà
                    check_sql = f"""
                    SELECT id_diplome FROM diplome WHERE nom_diplome = {nom_diplome};
                    """
                    cursor.execute(check_sql)
                    result = cursor.fetchone()

                    # Recherche l'ID pour la spécialisation
                    check_sql = f"""
                    SELECT id_specialisation FROM specialisation WHERE nom_specialisation = {nom_specialisation};
                    """
                    cursor.execute(check_sql)
                    result_spec = cursor.fetchone()

                    if result_spec:
                        id_specialisation = result_spec[0]
                    else:
                        id_specialisation = 'NULL'

                    # Recherche l'ID pour l'école
                    check_sql = f"""
                    SELECT id_ecole FROM ecole WHERE nom_ecole = {nom_ecole};
                    """
                    cursor.execute(check_sql)
                    result_ecole = cursor.fetchone()

                    if not result and result_ecole:  # Insère uniquement s'il n'existe pas
                        id_ecole = result_ecole[0]
                        sql = f"""
                                INSERT INTO diplome (ref_diploma, id_specialisation, id_ecole, 
                                                    nom_diplome, parcours)
                                VALUES ({ref_diploma}, {id_specialisation}, {id_ecole}, {nom_diplome}, {parcours});
                                """
                        cursor.execute(sql)
                        connection.commit()

                        diplomes.append(nom_diplome)
    print("Succès à l'ajout des diplômes à la base de données.")

# Ajouter ou mettre à jour des liens entre diplômes et personnes via a_un_diplome
def push_a_un_diplome(infosDiploma, connection, cursor):
    """
    Relie la table diplome à la table personne via la table a_un_diplome.
    Vérifie la duplication des données, ajoute les nouveaux liens,
    et met à jour les données existantes si nécessaire.

    :param infosDiploma: Liste de toutes les informations sur les diplômes de l'API
    :param connection: Objet de connexion à la base de données
    :param cursor: Objet curseur de la connexion à la base de données
    """
    print("Ajout ou mise à jour des liens diplômes/personnes à la base de données...")

    for info in infosDiploma: 
        if '_embedded' in info and 'diplomas' in info["_embedded"]:
            DiplomaInfo = getDiplomaInfo(info)
            id_personne = info["id"]

            for i in range(len(DiplomaInfo)):
                # Préparation des données du lien
                est_diplome = DiplomaInfo[i]["estDiplome"]
                nom_diplome = format_name(DiplomaInfo[i]["nom_diplome"])

                dateDiplomation = DiplomaInfo[i]["dateDiplomation"]
                if dateDiplomation != '':
                    dateDiplomation = format_str(dateDiplomation)
                else:
                    dateDiplomation = 'NULL'
                
                dateIntegration = DiplomaInfo[i]["dateIntegration"]
                if dateIntegration != '':
                    dateIntegration = format_str(dateIntegration)
                else:
                    dateIntegration = 'NULL'

                # Vérifie si le diplôme existe
                check_sql = f"""
                SELECT id_diplome FROM diplome WHERE nom_diplome = {nom_diplome};
                """
                cursor.execute(check_sql)
                result_diplome = cursor.fetchone()

                # Vérifie si la personne existe
                check_sql = f"""
                SELECT id_personne FROM personne WHERE id_personne = {id_personne};
                """
                cursor.execute(check_sql)
                result_personne = cursor.fetchone()

                if result_diplome and result_personne:  # Vérifie que les données sont valides
                    id_diplome = result_diplome[0]
                    
                    # Vérifie si le lien existe déjà
                    check_sql = f"""
                    SELECT id_diplome FROM a_un_diplome WHERE id_diplome = {id_diplome} AND id_personne = {id_personne};
                    """
                    cursor.execute(check_sql)
                    result = cursor.fetchone()

                    if not result:  # Insère un nouveau lien si inexistant                   
                        sql = f"""
                                INSERT INTO a_un_diplome (id_diplome, id_personne, date_diplomation, date_integration, est_diplome)
                                VALUES ({id_diplome}, {id_personne}, {dateDiplomation}, {dateIntegration}, {est_diplome});
                                """
                    else:  # Met à jour le lien existant
                        sql = f"""
                                UPDATE a_un_diplome
                                SET date_diplomation = {dateDiplomation},
                                    date_integration = {dateIntegration},
                                    est_diplome = {est_diplome}
                                WHERE id_diplome = {id_diplome} AND id_personne = {id_personne};
                                """
                    cursor.execute(sql)
                    connection.commit()

    print("Succès à l'ajout ou mise à jour des liens diplômes/personnes dans la base de données.")

#%% 
# Charger les données depuis l'API

# Active les appels asynchrones aux requêtes API
import nest_asyncio
nest_asyncio.apply()

# Démarre le chronomètre
start_time = datetime.now()

# Charge les données nécessaires depuis l'API
infosDiploma = asyncio.run(fetchData_async("diploma"))
infosUser = asyncio.run(fetchData_async("profile"))

# Informe la durée totale de récupération des données
end_time = datetime.now()
print("Durée de récupération des données de l'API : {}".format(end_time - start_time))

#%% 
# Insérer les données dans la base de données

# Établit la connexion avec la base de données
connection, cursor = init()

# Démarre le chronomètre
start_time = datetime.now()

# Remplit les tables specialisation et type_utilisateur
push_specialisation(infosDiploma, connection, cursor)
push_type_utilisateur(infosUser, connection, cursor)

# Remplit les tables type et mail (doit être fait dans cet ordre)
types = []
types = push_type_mail(infosUser, connection, cursor, types)
types = push_type_adress(infosUser, connection, cursor, types)
push_mail(infosUser, connection, cursor, types)

# Remplit les tables ville, personne, adresse, ecole, diplome et a_un_diplome
push_ville(infosUser, connection, cursor)
push_personne(infosUser, connection, cursor)
push_adresse(infosUser, connection, cursor)
push_ecoles(infosDiploma, connection, cursor)
push_diplome(infosDiploma, connection, cursor)
push_a_un_diplome(infosDiploma, connection, cursor)

# Termine la connexion avec la base de données
cursor.close()

# Mesure le temps nécessaire pour insérer les données dans la base de données
end_time = datetime.now()
print('Durée de la mise à jour de la base de données : {}'.format(end_time - start_time))

# %%
