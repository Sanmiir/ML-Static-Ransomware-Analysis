## ML-Static-Ransomware-Analysis

**Projeto de TCC – Detecção de Ransomware usando Análise Estática e Machine Learning**

Este projeto propõe uma aplicação **web full-stack** para classificar executáveis (PE) do Windows como **"Benignos"** ou **"Ransomware"**, utilizando **análise estática** (funções de API e strings) e **Machine Learning**.

A abordagem evita a execução do arquivo, baseando-se apenas em **features estáticas** extraídas do binário e alimentadas em um modelo de **Regressão Logística L1**, treinado para identificar padrões maliciosos com alta precisão.

---

## Resultados do Modelo

O modelo foi treinado em um dataset balanceado com **2.199 amostras**  
(1.174 benignas e 1.025 ransomware).

**📊 Desempenho Final (Conjunto de Teste Cego):**
- **Taxa de Detecção de Ransomware:** 93,7%
- **Falsos Negativos (FN):** 13  
- **Verdadeiros Positivos (TP):** 192  

O objetivo principal foi **minimizar falsos negativos**, garantindo alta segurança na detecção.

---

##  Métricas de Performance (Validação Cruzada 5-Folds)

| Métrica | Resultado (Média ± Desvio Padrão) |
|:--------|:----------------------------------:|
| **Acurácia** | 0.8562 ± 0.0152 |
| **Precisão (Weighted)** | 0.8764 ± 0.0124 |
| **Recall (Weighted)** | 0.8562 ± 0.0152 |
| **F1-Score (Weighted)** | 0.8554 ± 0.0155 |
| **ROC AUC** | 0.8728 ± 0.0165 |

Esses resultados (registrados em `metricas_cv.txt`) demonstram a **robustez e estabilidade** do modelo.

---

##  Tecnologias Utilizadas

**Backend (API):**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)

**Frontend (UI):**
- [React](https://react.dev/)
- [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)

**Machine Learning:**
- [Scikit-learn](https://scikit-learn.org/)
  - `LogisticRegression`, `StandardScaler`, `Pipeline`

**Análise Estática (PE):**
- [pefile](https://pypi.org/project/pefile/)

**Ambiente:**
- [Conda](https://docs.conda.io/en/latest/)

---

##  Estrutura do Repositório
ML-Static-Ransomware-Analysis/
├── main.py # Backend FastAPI (API principal)
├── extractor.py # Extração de features (PEfile + strings)
├── create_header.py # Criação do cabeçalho do dataset
├── TCC_Notebook.ipynb # Notebook Jupyter com o pipeline completo de ML
├── ransomware_functions.txt # Lista de funções de API observadas em ransomware
├── ransomware_strings.txt # Lista de strings características (.locked, etc.)
├── features_selecionadas.txt # Relatório final das 168 features selecionadas
├── metricas_cv.txt # Métricas finais de performance
├── requirements.txt # Dependências Conda/Pip
├── base/ # Diretório de datasets locais (ignorado pelo Git)
└── tcc-frontend/ # Aplicação React (Frontend)


---

## ⚠️ Aviso sobre o Dataset

Este repositório **NÃO contém** as amostras de malware ou benignas usadas no treinamento,  
devido à sua natureza **maliciosa e restrições legais**.

Para reproduzir os experimentos:

- **Fonte recomendada:** [github.com/refade/Ransomware](https://github.com/refade/Ransomware)  
- **Composição esperada:**
  - 1.174 amostras benignas  
  - 1.025 amostras ransomware

**Estrutura de diretórios esperada:**

tcc-malware-analysis/
├── base/
│ ├── benignos/
│ │ └── (1174 arquivos .exe benignos)
│ └── malwares/
│ └── (1025 arquivos .exe maliciosos)
└── ...


---

## ⚙️ Guia de Execução (Do Zero à Demo)

### 1️⃣ Setup do Ambiente

```bash
# 1. Criar ambiente Conda
conda create -n tcc-env python=3.10 -y

# 2. Ativar o ambiente
conda activate tcc-env

# 3. Instalar dependências Python
conda install --file requirements.txt -y

# 4. Instalar Node.js (para o frontend React)
conda install -c conda-forge nodejs -y

# 5. Instalar dependências do frontend
cd tcc-frontend
npm install
cd ..


2️⃣ Missão 1: Geração do Dataset

Gerar o arquivo base.csv a partir das amostras baixadas:

# Geração e extração de features
python create_header.py > base/base.csv
python extractor.py --directory "./base/benignos/" --csv base/base.csv --fileclass 0
python extractor.py --directory "./base/malwares/" --csv base/base.csv --fileclass 1

3️⃣ Missão 2: Treinamento do Modelo

Treine o modelo executando o notebook Jupyter:

jupyter lab

No notebook TCC_Notebook.ipynb:

Execute todas as células.

Isso gerará:

malware_model.joblib

malware_scaler.joblib

Relatórios como matriz_confusao.png, etc.

4️⃣ Missão 3: Executando a Aplicação (Demo)

Você precisará de dois terminais rodando simultaneamente.

🖥️ Terminal 1 – Backend (FastAPI):

conda activate tcc-env
uvicorn main:app --reload

🌐 Terminal 2 – Frontend (React):

conda activate tcc-env
cd tcc-frontend
npm start


Abra no navegador:

http://localhost:3000

🧩 Créditos e Autores

Desenvolvido por Sanmir Gabriel como parte do Trabalho de Conclusão de Curso (TCC) em Ciência da Computação.

Orientação: Detecção de ransomware via aprendizado de máquina com análise estática de binários.

