import requests
import config

# URL para obter o token (verifique na documentação qual é o endpoint correto)
token_url = "https://www.centraliens-nantes.org/oauth/token"

# Suas credenciais OAuth2
client_id = config.key
client_secret = config.secret

# Parâmetros para a requisição do token (OAuth2 Client Credentials Grant)
data = {
    'grant_type': 'client_credentials'
}

# Fazendo a requisição para obter o token de acesso
response = requests.post(token_url, data=data, auth=(client_id, client_secret))

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    try:
        token_info = response.json()
        access_token = token_info['access_token']
        print(f"Token de Acesso: {access_token}")
    except requests.exceptions.JSONDecodeError:
        print("A resposta não é um JSON válido. Conteúdo da resposta:")
        print(response.text)
else:
    print(f"Erro ao obter o token: {response.status_code}, {response.text}")

# Defina a URL base da API
base_url = "https://www.centraliens-nantes.org/api/v2"

# ID da pessoa cujo perfil você deseja acessar
person_id = "255187"  # Substitua pelo ID desejado

# Endpoint para acessar o perfil da pessoa
url = f"{base_url}/users/{person_id}"

# Cabeçalhos de autenticação
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Fazendo a requisição GET para obter o perfil
response = requests.get(url, headers=headers)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    profile_data = response.json()
    print(profile_data)
else:
    print(f"Erro: {response.status_code}, {response.text}")
