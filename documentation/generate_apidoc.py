import os
from sphinx.ext.apidoc import main

def generate_apidoc():
    # Caminho para o diretório com os módulos Python
    modules_path = os.path.abspath("../projet-application/code")  # Ajuste o caminho conforme necessário
    # Caminho para o diretório onde serão gerados os arquivos .rst
    output_path = os.path.abspath("source")
    
    # Argumentos para o sphinx-apidoc
    args = [
        "--force",            # Sobrescreve arquivos existentes
        "--output-dir", output_path,  # Diretório de saída
        modules_path          # Diretório com os módulos Python
    ]
    
    # Executa o apidoc
    print("Gerando arquivos .rst...")
    main(args)
    print("Arquivos .rst gerados com sucesso!")

if __name__ == "__main__":
    generate_apidoc()
