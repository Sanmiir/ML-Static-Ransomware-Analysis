#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import subprocess
import argparse
import pefile

# =========================================================
# 1. DEFINIR CAMINHOS ABSOLUTOS (CORREÇÃO FINAL)
# =========================================================
# Define o diretório onde ESTE SCRIPT (extractor.py) está
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define os caminhos para os arquivos de dependência
MALWARE_FUNCTIONS_FILE_PATH = os.path.join(SCRIPT_DIR, "ransomware_functions.txt")
MALWARE_STRINGS_FILE_PATH = os.path.join(SCRIPT_DIR, "ransomware_strings.txt")
STRINGS_EXECUTABLE_PATH = os.path.join(SCRIPT_DIR, "strings64.exe")
# =========================================================

def extract_imported_functions(file: str) -> list[str] | None:
    """
    Extrai funções importadas de um executável PE (Windows).
    VERSÃO CORRIGIDA: Garante o fechamento do 'pe.close()'
    """
    pe = None  # Inicializa fora do try
    try:
        pe = pefile.PE(file)  # 1. ARQUIVO ABERTO
        functions = []

        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        functions.append(imp.name.decode().lower())
        
        return list(set(functions))  # 2. RETORNO

    except Exception as e:
        # Mesmo se falhar, o finally será chamado
        print(f"[ERRO PEFILE] Falha ao ler {file}: {e}")
        return None
    
    finally:
        # 3. GARANTE O FECHAMENTO DO ARQUIVO
        if pe:
            pe.close()


def extract_strings(file: str) -> list[str] | None:
    """
    Extrai strings legíveis de um binário usando 'strings64.exe'.
    VERSÃO CORRIGIDA: Usa caminho absoluto.
    """
    try:
        result = subprocess.run(
            [STRINGS_EXECUTABLE_PATH, file],  # <-- USA O CAMINHO ABSOLUTO
            capture_output=True,
            text=True,
            check=True,
            errors="ignore"
        )
        strings = result.stdout.lower().split("\n")
        return list(set(strings))
    except subprocess.CalledProcessError:
        return None


def check_functions(file: str) -> list[int]:
    """
    Compara funções importadas com a lista de malware.
    VERSÃO CORRIGIDA: Usa caminho absoluto.
    """
    results = []
    file_functions = extract_imported_functions(file)

    # <-- USA O CAMINHO ABSOLUTO
    with open(MALWARE_FUNCTIONS_FILE_PATH, "r", encoding="utf-8") as f:
        malware_functions = f.read().lower().split("\n")

    for mf in malware_functions:
        feature_name = mf.strip()
        if feature_name:  # Ignora linhas em branco
            results.append(1 if file_functions and feature_name in file_functions else 0)

    return results


def check_strings(file: str) -> list[int]:
    """
    Compara strings do arquivo com a lista de malware.
    VERSÃO CORRIGIDA: Usa caminho absoluto.
    """
    results = []
    file_strings = extract_strings(file)

    # <-- USA O CAMINHO ABSOLUTO
    with open(MALWARE_STRINGS_FILE_PATH, "r", encoding="utf-8") as f:
        malware_strings = f.read().lower().split("\n")

    for ms in malware_strings:
        feature_name = ms.strip()
        if feature_name:  # Ignora linhas em branco
            results.append(1 if file_strings and feature_name in file_strings else 0)

    return results


def check_file(file: str) -> list[int]:
    """
    Combina funções e strings do arquivo em uma única lista de atributos.
    """
    return check_functions(file) + check_strings(file)


def create_database(directory: str, output_csv: str, file_class: int) -> None:
    """
    Cria um CSV com os atributos de todos os arquivos de um diretório.
    VERSÃO ROBUSTA: Pula arquivos corrompidos.
    """
    with open(output_csv, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        print(f"\n[INFO] Processando diretório: {directory} (Classe: {file_class})")
        processed_count = 0
        failed_count = 0

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                try:
                    # Tenta processar o arquivo
                    attributes = check_file(filepath)
                    row = [filename, file_class] + attributes
                    writer.writerow(row)
                    processed_count += 1

                except Exception as e:
                    # Se falhar (ex: pefile não lê, etc), imprime o erro e CONTINUA
                    print(f"[AVISO] Falha ao processar {filename}: {e}. Pulando.")
                    failed_count += 1
        
        print(f"[INFO] Diretório concluído. Processados: {processed_count}, Falhas: {failed_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ransomware Feature Extractor (PE)"
    )

    parser.add_argument("--file", type=str, help="Arquivo único para extrair atributos.")
    parser.add_argument("--directory", type=str, help="Diretório contendo arquivos para processar.")
    parser.add_argument("--csv", type=str, help="Arquivo CSV de saída.")
    parser.add_argument(
        "--fileclass", type=int, choices=[0, 1],
        help="Classe dos arquivos do diretório (0=benigno, 1=malware)."
    )

    args = parser.parse_args()

    if args.file:
        print(check_file(args.file))
    elif args.directory and args.csv and args.fileclass is not None:
        create_database(args.directory, args.csv, args.fileclass)
    else:
        print(
            "Use --file para um único arquivo OU --directory, --csv e --fileclass para um diretório."
        )