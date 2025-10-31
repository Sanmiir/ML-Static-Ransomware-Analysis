#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import extractor  # Importa o módulo extractor.py

# =========================================================
# 1. Definir Caminhos Absolutos
# =========================================================
# CORREÇÃO 1: Usar caminhos absolutos para que o Uvicorn encontre os arquivos.
# Define o diretório onde ESTE SCRIPT (main.py) está
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos para os artefatos de ML (baseado no SCRIPT_DIR)
MODEL_PATH = os.path.join(SCRIPT_DIR, "malware_model.joblib")
SCALER_PATH = os.path.join(SCRIPT_DIR, "malware_scaler.joblib")

# Caminho para a pasta de uploads (baseado no SCRIPT_DIR)
UPLOAD_FOLDER = os.path.join(SCRIPT_DIR, "temp_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Garante que a pasta exista

# =========================================================
# 2. Carregar os Artefatos de Machine Learning
# =========================================================
# CORREÇÃO 2: Carregar o SCALER e o MODELO separadamente, 
# exatamente como o seu notebook (Fase 7) os salvou.
model = None
scaler = None

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    print("[INFO] Carregando artefatos de modelo e scaler...")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("[INFO] Modelos carregados com sucesso.")
else:
    print(f"[AVISO] Arquivos '{MODEL_PATH}' ou '{SCALER_PATH}' não encontrados.")
    print("A API só funcionará após o treinamento (Missão 2).")

# =========================================================
# 3. Criar a Aplicação FastAPI
# =========================================================
app = FastAPI(title="API de Detecção de Ransomware (TCC)")

# Configurar CORS (Seu código original está correto)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Endereço do app React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# 4. Endpoint de Predição (Análise Estática)
# =========================================================
@app.post("/predict_upload")
async def predict_malware_upload(file: UploadFile = File(...)):
    """
    Recebe um arquivo PE, salva temporariamente, extrai features com 'extractor.py'
    e retorna a predição do modelo treinado.
    """
    # Checagem de robustez
    if not model or not scaler:
        raise HTTPException(status_code=503, detail="Modelo(s) não carregado(s). Execute o notebook de treinamento.")

    # Caminho absoluto para o arquivo temporário
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        # 1. Salvar o arquivo no disco
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Extrair features (depende do extractor.py corrigido)
        features_list = extractor.check_file(filepath)
        
        # Se o extractor falhar (ex: pefile), ele pode retornar None
        if features_list is None:
             raise Exception("Extração de features falhou (provavelmente pefile).")

        # 3. Converter para numpy array
        features_array = np.array(features_list).reshape(1, -1)
        
        # 4. Aplicar o SCALER (Etapa que faltava no seu código)
        scaled_features = scaler.transform(features_array)

        # 5. Fazer predição
        prediction = model.predict(scaled_features) # Agora sim, no modelo
        classe = int(prediction[0])
        label = "Ransomware (Malicious)" if classe == 1 else "Benign"

        return {
            "filename": file.filename,
            "prediction_label": label,
            "prediction_class": classe
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro na análise estática. O arquivo é um PE (Windows) válido? Erro: {e}"
        )

    finally:
        # 6. Limpar o arquivo temporário
        if os.path.exists(filepath):
            os.remove(filepath)

# =========================================================
# 5. Endpoint Raiz (Status da API)
# =========================================================
@app.get("/")
def root():
    return {"message": "API do TCC de Ransomware está online."}