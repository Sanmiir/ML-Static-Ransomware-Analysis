import os

# Nomes dos arquivos de features
MALWARE_FUNCTIONS_FILE = "ransomware_functions.txt"
MALWARE_STRINGS_FILE = "ransomware_strings.txt"

# Listas para guardar os nomes das features
features = []

try:
    # Ler as funções
    with open(MALWARE_FUNCTIONS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            feature_name = line.strip()
            if feature_name: # Evita linhas em branco
                features.append(f"func_{feature_name}") # Adiciona prefixo para evitar colisão

    # Ler as strings
    with open(MALWARE_STRINGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            feature_name = line.strip()
            if feature_name: # Evita linhas em branco
                # Limpa o nome da feature para ser um nome de coluna válido
                clean_name = ''.join(e for e in feature_name if e.isalnum() or e == '_')
                features.append(f"str_{clean_name}")

    # Criar a string de cabeçalho
    # O separador é ';' como definido no seu extractor.py
    header = "filename;fileclass;" + ";".join(features)

    # Imprimir o cabeçalho para o stdout (para o .sh pegar)
    print(header)

except FileNotFoundError as e:
    print(f"Erro: Arquivo de feature não encontrado. {e}", file=os.sys.stderr)
except Exception as e:
    print(f"Erro ao processar arquivos de feature: {e}", file=os.sys.stderr)