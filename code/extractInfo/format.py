import json
from unidecode import unidecode

def jprint(obj):
    """
    Affiche un objet JSON avec indentation.

    :param obj: Une chaîne au format JSON
    :return: fichier json transformé en chaine de charactères
    """

    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    return text

def format_name(city_name):
    """
    Formate les noms afin de normaliser les données.
    Supprime les caractères spéciaux, les tirets et remplace les simples guillemets '' par des doubles.
    Met chaque première lettre d'un mot en majuscule et les autres en minuscule.
    Ex : SUCE-SUR-ERDRE devient Suce Sur Erdre

    :param city_name: Une chaîne de caractères
    :return: normalized_name: Chaîne de caractères normalisée
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
    Formate les adresses afin de s'adapter à 128 caractères.
    
    :param adress: Une chaîne de caractères
    :return: adress: Chaîne de caractères limitée à 128 caractères
    """
    adress = format_name(adress)
    if (len(adress) > 127):
        adress = adress[:128] + "'"
    return adress

def format_code_postal(code):
    """
    Formate le code postal afin de normaliser les données.
    Vérifie s'il s'agit d'un entier, sinon il le définit à zéro.

    :param code: Un code postal au format chaîne de caractères
    :return: code modifié
    """
    try:
        code = int(code[0:5])
        return code
    except ValueError:
        code = 0

    return code

def format_str(str):
    """
    Formate une chaîne afin d'éviter les erreurs dans les requêtes SQL.
    Supprime les caractères spéciaux, remplace les guillemets simples par des doubles ' -> ''
    et ajoute un guillemet initial et final à la chaîne.
    Ex : Côte d'Ivoire -> 'Cote d''Ivoire'

    :param str: Une chaîne de caractères
    :return: str: Chaîne modifiée
    """
    str = unidecode(str)
    str = str.replace("'", "''")
    str = "'" + str + "'"

    return str
