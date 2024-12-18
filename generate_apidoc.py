import os
from sphinx.ext.apidoc import main as sphinx_apidoc
import subprocess
import sys

# Diretórios
source_dir = os.path.abspath('documentation/source')  # Ajuste ao caminho correto
project_dir = os.path.abspath(".")  # Diretório principal do projeto
output_dir = os.path.join(source_dir, "modules")

# Garantir que o diretório de saída exista
os.makedirs(output_dir, exist_ok=True)

# Comando para gerar os arquivos rst
command = [
    sys.executable, "-m", "sphinx.ext.apidoc",
    "-o", output_dir,  # Diretório de saída
    project_dir,       # Diretório do código
    "--force",         # Sobrescreve arquivos existentes
    "--separate"       # Cria arquivos separados por módulo
]

# Executar o comando
try:
    subprocess.run(command, check=True)
    print(f"Arquivos .rst gerados com sucesso em {output_dir}")
except Exception as e:
    print(f"Erro ao gerar os arquivos .rst: {e}")
