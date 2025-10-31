import React, { useState } from 'react';
import axios from 'axios';
import { UploadCloud, File, ShieldOff, ShieldCheck, Cpu, Database, BarChart3, Binary, Scale, Brain } from 'lucide-react';
import './App.css';

function App() {
  // Estado para controlar a aba ativa
  const [activeTab, setActiveTab] = useState('demo');
  
  // Estado para o upload e análise
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // --- DADOS DA PESQUISA (PLACEHOLDERS) ---
  // TODO: Substitua estes valores pelos resultados reais do seu Jupyter Notebook (Missão 2)
  const placeholderResults = {
    metrics: {
        accuracy: "0.8562 ± 0.0152",
        precision: "0.8764 ± 0.0124",
        recall: "0.8562 ± 0.0152",
        f1: "0.8554 ± 0.0155",
        roc_auc: "0.8728 ± 0.0165"
      },
      features: {
        total: 1327,
        selected: 168 
      },
    confusionMatrix: {
      path: "/matriz_confusao.png", // TODO: Coloque seu .png na pasta /public
      alt: "Matriz de Confusão (Validação Cruzada)"
    }
  };
  // ------------------------------------------

  // Lida com a seleção do arquivo
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setResult(null);
    setError(null);
  };

  // Lida com o envio do arquivo para a API
  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Por favor, selecione um arquivo primeiro.");
      return;
    }

    setIsLoading(true);
    setResult(null);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // Chama o endpoint da sua API FastAPI
      const response = await axios.post('http://127.0.0.1:8000/predict_upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      let errorMsg = "Erro ao conectar na API. O backend FastAPI (uvicorn) está rodando?";
      if (err.response && err.response.data && err.response.data.detail) {
        // Exibe o erro específico do FastAPI (ex: "Arquivo não é PE")
        errorMsg = `Erro da API: ${err.response.data.detail}`;
      }
      setError(errorMsg);
    }
    setIsLoading(false);
  };

  // --- COMPONENTES DAS ABAS ---

  // Aba 1: A Demonstração Interativa
  const DemoTab = () => (
    <div className="tab-content">
      <h2><UploadCloud size={28} /> Demonstração do Pipeline</h2>
      <p>Faça o upload de um arquivo executável (PE) do Windows para análise estática. O arquivo será enviado para a API, que executará o `extractor.py` e o modelo L1 otimizado.</p>
      
      <div className="upload-section">
        <label htmlFor="file-upload" className="file-upload-label">
          <File size={18} />
          {selectedFile ? selectedFile.name : "Escolher arquivo..."}
        </label>
        <input id="file-upload" type="file" onChange={handleFileChange} />
        <button 
          onClick={handleUpload} 
          disabled={isLoading || !selectedFile}
          className="scan-button"
        >
          {isLoading ? "Analisando..." : "Analisar"}
        </button>
      </div>

      {/* --- Exibição dos Resultados da Demo --- */}
      {isLoading && <div className="loading-spinner"></div>}
      
      {error && (
        <div className="result-card error-card">
          <ShieldOff size={48} />
          <div className="result-text">
            <h4>Erro na Análise</h4>
            <p>{error}</p>
          </div>
        </div>
      )}

      {result && (
        <div className={`result-card ${result.prediction_class === 1 ? 'malware-card' : 'benign-card'}`}>
          {result.prediction_class === 1 ? <ShieldOff size={48} /> : <ShieldCheck size={48} />}
          <div className="result-text">
            <h4>Análise Concluída</h4>
            <p>Arquivo: <strong>{result.filename}</strong></p>
            <p>Predição: <strong>{result.prediction_label}</strong></p>
          </div>
        </div>
      )}
    </div>
  );

  // Aba 2: Os Resultados Acadêmicos (A Prova)
  const ResultsTab = () => (
    <div className="tab-content">
      <h2><BarChart3 size={28} /> Resultados da Pesquisa</h2>
      <p>O modelo não é uma "caixa-preta". Ele foi treinado e validado cientificamente usando Validação Cruzada Estratificada para garantir robustez e confiabilidade.</p>

      {/* Bloco 1: Métricas de Performance */}
      <div className="result-block">
        <h3><Scale size={20} /> 1. Métricas de Performance (Validação Cruzada 5-Folds)</h3>
        <p>A tabela abaixo mostra a performance média e o desvio padrão do modelo, provando que seu desempenho é estável e não foi "sorte".</p>
        <table className="metrics-table">
          <thead>
            <tr>
              <th>Métrica</th>
              <th>Resultado (Média ± Desvio Padrão)</th>
            </tr>
          </thead>
          <tbody>
            {/* TODO: Substitua estes valores pelos seus resultados reais da Missão 2 */}
            <tr><td>Acurácia</td><td>{placeholderResults.metrics.accuracy}</td></tr>
            <tr><td>Precisão (Weighted)</td><td>{placeholderResults.metrics.precision}</td></tr>
            <tr><td>Recall (Weighted)</td><td>{placeholderResults.metrics.recall}</td></tr>
            <tr><td>F1-Score (Weighted)</td><td>{placeholderResults.metrics.f1}</td></tr>
            <tr><td>ROC AUC</td><td>{placeholderResults.metrics.roc_auc}</td></tr>
          </tbody>
        </table>
      </div>

      {/* Bloco 2: Otimização de Features */}
      <div className="result-block">
        <h3><Brain size={20} /> 2. Otimização (Seleção de Features L1)</h3>
        <p>O dataset bruto foi construído com <strong>{placeholderResults.features.total}</strong> features (strings + funções). Aplicando a regularização L1 (Lasso), o modelo aprendeu a **ignorar o ruído** e focar apenas nas features que importam.</p>
        <div className="feature-comparison">
          <div className="feature-box">
            <Database size={32} />
            <span>{placeholderResults.features.total}</span>
            <label>Features Totais (Ruído)</label>
          </div>
          <div className="feature-arrow">→</div>
          <div className="feature-box optimized">
            <Cpu size={32} />
            <span>{placeholderResults.features.selected}</span>
            <label>Features Relevantes (Sinal)</label>
          </div>
        </div>
        <p>Esta otimização cria um modelo mais leve, rápido e robusto, provando que a maioria das features era desnecessária.</p>
      </div>
      
      {/* Bloco 3: Matriz de Confusão */}
      <div className="result-block">
        <h3><Binary size={20} /> 3. Matriz de Confusão (Agregada)</h3>
        <p>A matriz abaixo (gerada pela Validação Cruzada) mostra visualmente os erros e acertos do modelo. O objetivo é maximizar a "Diagonal Principal" (Verdadeiros Positivos e Verdadeiros Negativos).</p>
        {/* TODO: Coloque seu 'matriz_confusao.png' na pasta /public */}
        <img 
          src={placeholderResults.confusionMatrix.path} 
          alt={placeholderResults.confusionMatrix.alt} 
          className="confusion-matrix"
          onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'block'; }}
        />
        <p style={{display: 'none', color: '#ffcccc'}}>
          Erro: 'matriz_confusao.png' não encontrada na pasta /public. Gere-a na Missão 2 e mova-a para /public.
        </p>
      </div>
    </div>
  );

  // --- Renderização Principal ---
  return (
    <div className="App">
      <header className="app-header-bar">
        <h1>TCC: Análise Estática de Ransomware com ML</h1>
      </header>

      <div className="tab-container">
        <button 
          className={`tab ${activeTab === 'demo' ? 'active' : ''}`}
          onClick={() => setActiveTab('demo')}>
          <UploadCloud size={18} />
          Demonstração
        </button>
        <button 
          className={`tab ${activeTab === 'results' ? 'active' : ''}`}
          onClick={() => setActiveTab('results')}>
          <BarChart3 size={18} />
          Resultados da Pesquisa
        </button>
      </div>

      <main className="main-content">
        {activeTab === 'demo' ? <DemoTab /> : <ResultsTab />}
      </main>
      
      <footer className="app-footer">
        <p>Desenvolvido por João Pedro Rodrigues Pessoa, Rafael Rolim e Sanmir Gabriel</p>
        <p>Orientador: Prof. Edkallen Lima | CENTRO UNIVERSITÁRIO DE JOÃO PESSOA UNIPÊ - JOÃO PESSOA - PB</p>
      </footer>
    </div>
  );
}

export default App;

