import json
from unidecode import unidecode

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

def format_str(str):
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
