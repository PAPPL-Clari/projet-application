import unittest
from unidecode import unidecode
import json
from extractInfo.format import jprint, format_name, format_adress, format_code_postal, format_str  

class TestFunctions(unittest.TestCase):

    def test_jprint(self):
        # Criando um exemplo de objeto JSON para passar para a função
        obj = {
            "name": "Alice",
            "age": 30,
            "city": "Paris"
        }

        # Chama a função jprint com o objeto
        output = jprint(obj)
        
        # Define o resultado esperado com a indentação e chaves ordenadas
        expected_output = json.dumps(obj, sort_keys=True, indent=4)
        
        # Verifica se a função print foi chamada com a saída formatada corretamente
        self.assertEqual(output, expected_output)


    def test_format_name(self):
            """
            Teste pour vérifier que la fonction format_name fonctionne correctement.
            """
            # Cas d'exemple de nom de ville
            city_name = "SUCE-SUR-ERDRE"
            result = format_name(city_name)
            expected = "'Suce Sur Erdre'"  # Format attendu
            self.assertEqual(result, expected)

            # Cas avec un apostrophe dans le nom
            city_name = "L'Île"
            result = format_name(city_name)
            expected = "'L''Ile'"  # Le guillemet simple doit être doublé
            self.assertEqual(result, expected)

    def test_format_adress(self):
        """
        Teste pour vérifier que la fonction format_adress formate correctement une adresse.
        """
        adress = "123 Rue de l'Université - Paris"
        result = format_adress(adress)
        expected = "'123 Rue De L''Universite Paris'"  # Format attendu
        self.assertEqual(result, expected)

        # Cas où l'adresse dépasse 128 caractères
        adress = "123 Rue de l'Université à Paris, très longue adresse qui dépasse 128 caractères, assurément une adresse trop longue"
        result = format_adress(adress)
        self.assertEqual(result, "'123 Rue De L''Universite A Paris, Tres Longue Adresse Qui Depasse 128 Caracteres, Assurement Une Adresse Trop Longue'")

    def test_format_code_postal(self):
        """
        Teste pour vérifier que la fonction format_code_postal formate correctement le code postal.
        """
        # Code postal valide
        code = "75001"
        result = format_code_postal(code)
        self.assertEqual(result, 75001)

        # Code postal invalide
        code = "ABCDE"
        result = format_code_postal(code)
        self.assertEqual(result, 0)

    def test_format_str(self):
        """
        Teste pour vérifier que la fonction format_str fonctionne correctement.
        """
        # Chaîne avec apostrophe
        input_str = "Côte d'Ivoire"
        result = format_str(input_str)
        expected = "'Cote d''Ivoire'"  # Guilles simples doivent être doublés
        self.assertEqual(result, expected)

        # Cas avec caractères spéciaux
        input_str = "Björk"
        result = format_str(input_str)
        expected = "'Bjork'"  # Les caractères spéciaux doivent être retirés
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
