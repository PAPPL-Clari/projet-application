from sphinx.ext.apidoc import main
import os

# Diretórios
output_dir = "source"  # Onde os arquivos .rst serão gerados
module_dir = "."  # Diretório com os módulos Python

# Argumentos para o apidoc
args = [
    "-o", output_dir,  # Diretório de saída
    module_dir,        # Diretório com os módulos a serem documentados
    "--force",         # Sobrescrever arquivos existentes
    "--no-toc",        # Não criar arquivos de sumário separados
]

# Executa o comando equivalente ao sphinx-apidoc
main(args)
