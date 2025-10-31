ML-Static-Ransomware-AnalysisProjeto de TCC para detecção de ransomware usando análise estática (funções de API, strings) e Machine Learning (React, FastAPI, Scikit-learn).Este projeto é uma aplicação web full-stack que classifica executáveis (PE) do Windows como "Benignos" ou "Ransomware". Ele extrai features estáticas do binário e os alimenta em um modelo de Regressão Logística L1 treinado, capaz de identificar padrões maliciosos sem executar o arquivo.🎯 Resultados do ModeloO modelo foi treinado em um dataset balanceado de 2.199 amostras (1.174 benignas, 1.025 ransomware). A performance final, validada em um conjunto de teste cego, alcançou uma taxa de detecção de ransomware de 93,7%.Matriz de Confusão (Conjunto de Teste)A matriz demonstra a eficácia do modelo em seu objetivo principal: minimizar Falsos Negativos (ransomware classificado como benigno).Falsos Negativos (FN): 13Verdadeiros Positivos (TP): 192Métricas de Performance (Validação Cruzada 5-Folds)As métricas abaixo (do arquivo metricas_cv.txt) provam a estabilidade e robustez do modelo:MétricaResultado (Média ± Desvio Padrão)Acurácia0.8562 ± 0.0152Precisão (Weighted)0.8764 ± 0.0124Recall (Weighted)0.8562 ± 0.0152F1-Score (Weighted)0.8554 ± 0.0155ROC AUC0.8728 ± 0.0165🛠️ Tecnologias UtilizadasBackend (API): FastAPI, UvicornFrontend: React (JavaScript)Machine Learning: Scikit-learn (LogisticRegression, StandardScaler, Pipeline)Análise de PE: pefileGerenciamento de Ambiente: Conda📂 Estrutura do Repositório/tcc-frontend: Aplicação React (Frontend).main.py: Backend FastAPI (API).extractor.py: Script principal de extração de features (PEfile, strings64.exe).create_header.py: Script utilitário para criar o cabeçalho do dataset.TCC_Notebook.ipynb: Notebook Jupyter com todo o processo de ML (Fases 1-8).ransomware_functions.txt: Lista de features de API (ex: CreateFileW).ransomware_strings.txt: Lista de features de strings (ex: .locked).features_selecionadas.txt: Relatório final das 168 features selecionadas pelo modelo L1.metricas_cv.txt: Relatório final das métricas de performance.requirements.txt: Lista de dependências do Conda/Pip.base/: Diretório onde os dados de treinamento devem ser colocados (ignorado pelo Git).⚠️ Aviso de Dataset (IMPORTANTE)Este repositório NÃO contém as amostras de malware ou benignas necessárias para o treinamento, devido ao seu tamanho e natureza maliciosa.Para reproduzir este projeto, você deve obter o dataset referenciado:Fonte: github.com/refade/RansomwareComposição Esperada: 1174 amostras benignas e 1025 amostras de ransomware.Você deve criar a seguinte estrutura de pastas na raiz do projeto:Plaintexttcc-malware-analysis/
├── base/
│   ├── benignos/
│   │   └── (1174 arquivos .exe benignos aqui)
│   └── malwares/
│       └── (1025 arquivos .exe maliciosos aqui)
└── ... (resto dos arquivos do projeto)
⚙️ Guia de Execução (Do Zero à Demo)1. Setup do AmbienteO projeto usa Conda para gerenciamento de ambiente.Bash# 1. Crie um novo ambiente Conda (recomendado)
conda create -n tcc-env python=3.10 -y

# 2. Ative o ambiente
conda activate tcc-env

# 3. Instale todas as dependências do Python
# (Isso instalará pandas, sklearn, fastapi, etc.)
conda install --file requirements.txt -y

# 4. Instale o Node.js para o frontend
conda install -c conda-forge nodejs -y

# 5. Instale as dependências do React
cd tcc-frontend
npm install
cd ..
2. Missão 1: Geração do DatasetGere o arquivo base.csv a partir das amostras que você baixou.Bash# (No terminal, na pasta raiz)
python create_header.py > base/base.csv
python extractor.py --directory "./base/benignos/" --csv base/base.csv --fileclass 0
python extractor.py --directory "./base/malwares/" --csv base/base.csv --fileclass 1
3. Missão 2: Treinamento do ModeloExecute o Jupyter Notebook TCC_Notebook.ipynb para treinar o modelo.Bashjupyter lab
Ação: Rode todas as células do notebook. Isso irá gerar os artefatos (malware_model.joblib, malware_scaler.joblib) necessários para a API. Os relatórios de performance (matriz_confusao.png, etc.) também serão atualizados.4. Missão 3: Executando a Aplicação (Demo)Você precisará de dois terminais rodando simultaneamente.Terminal 1: Backend (API)Bashconda activate tcc-env
uvicorn main:app --reload
Terminal 2: Frontend (React)Bashconda activate tcc-env
cd tcc-frontend
npm start
Acesse http://localhost:3000 no seu navegador para usar a aplicação.
