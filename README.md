# TCC: Análise Estática de Ransomware com Machine Learning

Este projeto é uma aplicação web full-stack (React + FastAPI) projetada para detectar ransomware usando análise estática e um modelo de Regressão Logística L1.

## Estrutura do Projeto

* `/tcc-frontend`: Aplicação React (Frontend).
* `main.py`: Backend FastAPI (API).
* `extractor.py`: Script principal de extração de features (PEfile, strings).
* `create_header.py`: Script utilitário para criar o cabeçalho do dataset.
* `*.joblib`: Modelos de ML (Gerados pela Missão 2).
* `base/`: Diretório onde os dados de treinamento devem ser colocados.

---

## Aviso de Dataset (IMPORTANTE)

Este repositório **NÃO** contém as amostras de malware ou benignas necessárias para o treinamento, devido ao seu tamanho e natureza maliciosa.

Para reproduzir este projeto, você deve obter o dataset referenciado:

* **Fonte:** [https://github.com/refade/Ransomware]
* **Composição Esperada:**
    * `1174` amostras benignas
    * `1025` amostras de ransomware

Você deve criar a seguinte estrutura de pastas na raiz do projeto:

tcc-malware-analysis/ 
├── base/ │ 
├── benignos/ │ │ ├── (1174 arquivos .exe benignos aqui) │ 
└── malwares/ │ ├── (1025 arquivos .exe maliciosos aqui) 
└── ... (resto dos arquivos do projeto)


---

## Guia de Execução (Do Zero à Demo)

### 1. Setup do Ambiente

O projeto usa **Conda** para gerenciamento de ambiente.

```bash
# 1. Crie um novo ambiente Conda (recomendado)
conda create -n tcc-env python=3.10

# 2. Ative o ambiente
conda activate tcc-env

# 3. Instale todas as dependências (Conda e Pip)
conda install --file requirements.txt

# 4. Instale o Node.js para o frontend
conda install -c conda-forge nodejs


### 2. Missão 1: Geração do Dataset

Gere o arquivo base.csv a partir das amostras que você baixou.

python create_header.py > base/base.csv
python extractor.py --directory "./base/benignos/" --csv base/base.csv --fileclass 0
python extractor.py --directory "./base/malwares/" --csv base/base.csv --fileclass 1


### 3. Missão 2: Treinamento do Modelo

Execute o Jupyter Notebook (ex: TCC_Notebook.ipynb) para treinar o modelo.
jupyter lab

Rode todas as células do notebook. Isso irá gerar os artefatos (malware_model.joblib, malware_scaler.joblib, matriz_confusao.png) necessários para a API.

### 4. Missão 3: Executando a Aplicação (Demo)

Você precisará de dois terminais.

Terminal 1: Backend (API)

conda activate tcc-env
uvicorn main:app --reload

Terminal 2: Frontend (React)

conda activate tcc-env
cd tcc-frontend
npm install
npm start

Acesse http://localhost:3000 no seu navegador.
