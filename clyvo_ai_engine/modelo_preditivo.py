"""
Clyvo Vet — PetCare 360 AI Engine
Módulo de Machine Learning Preditivo: Classificação do Índice de Risco Preventivo (IRP)
Disciplina: Disruptive Architectures: IoT, IoB & Generative IA (FIAP 2026)
Equipe: João Vitor Lacerda, Kauan Vieira, Murillo Carapia, Pedro Previtali
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

MODEL_FILE = os.path.join(os.path.dirname(__file__), 'modelo_risco_veterinario.joblib')

# Mapeamento de Classes de Risco
CLASSES_RISCO = {
    0: 'BAIXO',
    1: 'MODERADO',
    2: 'ALTO',
    3: 'CRITICO'
}

FEATURES = [
    'temperatura_atual',
    'delta_temperatura_24h',
    'umidade_ambiente',
    'idade_anos',
    'especie_gato',
    'porte_codigo',       # 1: Pequeno, 2: Medio, 3: Grande, 4: Gigante
    'atraso_vacina_dias',
    'variacao_peso_pct',
    'medicamento_continuo',
    'indice_atividade_iob' # 0 a 100 (IoB coleira)
]

def gerar_dataset_veterinario(n_amostras=1500, random_state=42):
    """
    Gera dataset sintético baseado em parâmetros clínicos reais de medicina veterinária
    (canina e felina), correlacionando telemetria IoT térmica, acelerometria e histórico.
    """
    np.random.seed(random_state)
    
    # 1. Espécie (0 = Cão, 1 = Gato)
    especie_gato = np.random.choice([0, 1], size=n_amostras, p=[0.65, 0.35])
    
    # 2. Porte (1: Pequeno a 4: Gigante - gatos são sempre pequeno/médio 1 ou 2)
    porte_codigo = np.where(especie_gato == 1, 
                            np.random.choice([1, 2], size=n_amostras, p=[0.7, 0.3]),
                            np.random.choice([1, 2, 3, 4], size=n_amostras, p=[0.25, 0.35, 0.30, 0.10]))
    
    # 3. Idade em anos (0.5 a 16)
    idade_anos = np.round(np.random.uniform(0.5, 16.0, size=n_amostras), 1)
    
    # 4. Telemetria IoT: Temperatura Corporal Atual (°C)
    # Temperatura normal canina/felina: 38.0°C a 39.2°C
    temperatura_base = np.random.normal(38.5, 0.4, size=n_amostras)
    # Injeta variações fisiológicas e patológicas
    disturbios = np.random.choice(['normal', 'febre_leve', 'hipertermia', 'hipotermia'], 
                                  size=n_amostras, p=[0.65, 0.18, 0.10, 0.07])
    temperatura_atual = np.copy(temperatura_base)
    for i, d in enumerate(disturbios):
        if d == 'febre_leve':
            temperatura_atual[i] = np.random.uniform(39.4, 39.9)
        elif d == 'hipertermia':
            temperatura_atual[i] = np.random.uniform(40.1, 41.2)
        elif d == 'hipotermia':
            temperatura_atual[i] = np.random.uniform(35.5, 37.2)
    temperatura_atual = np.round(temperatura_atual, 2)
    
    # 5. Delta de temperatura em 24h
    delta_temperatura_24h = np.round(np.abs(temperatura_atual - 38.5) + np.random.normal(0, 0.2, size=n_amostras), 2)
    
    # 6. Umidade ambiente capturada pelo DHT22 (%)
    umidade_ambiente = np.round(np.random.uniform(30.0, 85.0, size=n_amostras), 1)
    
    # 7. Atraso vacinal em dias (0 = em dia, até 400 dias)
    atraso_vacina_dias = np.random.choice([0, 15, 45, 90, 180, 365], size=n_amostras, p=[0.55, 0.15, 0.12, 0.08, 0.06, 0.04])
    
    # 8. Variação de peso recente (%) - perda > 8% é sinal de alerta
    variacao_peso_pct = np.round(np.random.normal(-0.5, 4.0, size=n_amostras), 1)
    
    # 9. Uso de medicação contínua
    medicamento_continuo = np.random.choice([0, 1], size=n_amostras, p=[0.75, 0.25])
    
    # 10. Índice de Atividade Diária IoB (0 = imóvel/letárgico a 100 = muito ativo)
    # Animais com febre ou hipotermia tendem a ter baixa atividade motora
    indice_atividade_iob = np.clip(
        np.round(np.random.normal(70, 18, size=n_amostras) - np.where(temperatura_atual > 39.5, 35, 0) - np.where(temperatura_atual < 37.5, 40, 0)),
        5, 100
    )
    
    # Regra de Determinação do Risco Clínico (Target de Treinamento Ground Truth)
    rotulos = []
    for i in range(n_amostras):
        t = temperatura_atual[i]
        atraso = atraso_vacina_dias[i]
        peso_delta = variacao_peso_pct[i]
        ativ = indice_atividade_iob[i]
        idade = idade_anos[i]
        
        pontos_risco = 0
        if t >= 40.5 or t < 36.8:
            pontos_risco += 50  # Emergência crítica
        elif t >= 39.6 or t < 37.4:
            pontos_risco += 30  # Febre ou hipotermia moderada
            
        if ativ < 25:
            pontos_risco += 25  # Letargia severa
        elif ativ < 45:
            pontos_risco += 12
            
        if atraso > 90:
            pontos_risco += 20
        elif atraso > 30:
            pontos_risco += 10
            
        if peso_delta < -8.0:
            pontos_risco += 20  # Perda ponderal abrupta
        elif peso_delta < -4.0:
            pontos_risco += 8
            
        if idade > 11.0:
            pontos_risco += 8   # Geriatria
            
        if pontos_risco >= 55:
            rotulos.append(3) # CRÍTICO
        elif pontos_risco >= 35:
            rotulos.append(2) # ALTO
        elif pontos_risco >= 18:
            rotulos.append(1) # MODERADO
        else:
            rotulos.append(0) # BAIXO
            
    df = pd.DataFrame({
        'temperatura_atual': temperatura_atual,
        'delta_temperatura_24h': delta_temperatura_24h,
        'umidade_ambiente': umidade_ambiente,
        'idade_anos': idade_anos,
        'especie_gato': especie_gato,
        'porte_codigo': porte_codigo,
        'atraso_vacina_dias': atraso_vacina_dias,
        'variacao_peso_pct': variacao_peso_pct,
        'medicamento_continuo': medicamento_continuo,
        'indice_atividade_iob': indice_atividade_iob,
        'nivel_risco': rotulos
    })
    
    return df

def treinar_e_salvar_modelo():
    """Treina o modelo RandomForestClassifier e salva os pesos no disco."""
    print("-> Gerando dataset clínico sintético veterinário...")
    df = gerar_dataset_veterinario(n_amostras=2000)
    
    X = df[FEATURES]
    y = df['nivel_risco']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    print(f"-> Treinando Random Forest com {len(X_train)} amostras de treino...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(n_estimators=120, max_depth=12, min_samples_split=4, random_state=42, class_weight='balanced'))
    ])
    
    pipeline.fit(X_train, y_train)
    
    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"-> Modelo Treinado com Sucesso! Acurácia no Teste: {acc:.4f} ({acc*100:.2f}%)")
    print("\nRelatório de Classificação:\n", classification_report(y_test, preds, target_names=['BAIXO', 'MODERADO', 'ALTO', 'CRITICO']))
    
    joblib.dump(pipeline, MODEL_FILE)
    print(f"-> Modelo salvo em: {MODEL_FILE}")
    return pipeline

class ClassificadorRiscoVeterinario:
    """Carrega o modelo treinado e fornece inferência em tempo real."""
    
    def __init__(self):
        if not os.path.exists(MODEL_FILE):
            treinar_e_salvar_modelo()
        self.model = joblib.load(MODEL_FILE)
        
    def analisar_risco(self, dados_pet: dict) -> dict:
        """
        Recebe os dados do pet (IoT + histórico) e infere o risco preventivo.
        """
        # Extrai features padronizadas
        temp = float(dados_pet.get('temperatura_atual', 38.5))
        delta_temp = float(dados_pet.get('delta_temperatura_24h', 0.2))
        umidade = float(dados_pet.get('umidade_ambiente', 55.0))
        idade = float(dados_pet.get('idade_anos', 3.0))
        especie_gato = 1 if str(dados_pet.get('especie', '')).upper() in ['GATO', 'FELINO'] else 0
        porte_map = {'PEQUENO': 1, 'MEDIO': 2, 'GRANDE': 3, 'GIGANTE': 4}
        porte = porte_map.get(str(dados_pet.get('porte', 'MEDIO')).upper(), 2)
        atraso_vacina = int(dados_pet.get('atraso_vacina_dias', 0))
        delta_peso = float(dados_pet.get('variacao_peso_pct', 0.0))
        med_continuo = 1 if dados_pet.get('medicamento_continuo', False) else 0
        atividade = float(dados_pet.get('indice_atividade_iob', 70.0))
        
        vetor_entrada = pd.DataFrame([[
            temp, delta_temp, umidade, idade, especie_gato, porte,
            atraso_vacina, delta_peso, med_continuo, atividade
        ]], columns=FEATURES)
        
        classe_predita = int(self.model.predict(vetor_entrada)[0])
        probas = self.model.predict_proba(vetor_entrada)[0]
        
        nome_classe = CLASSES_RISCO[classe_predita]
        
        # Cálculo do score ponderado contínuo (0 a 100%)
        # Pesos das classes: Baixo(10%), Moderado(40%), Alto(75%), Crítico(100%)
        score_cont = (probas[0]*10 + probas[1]*40 + probas[2]*75 + (probas[3] if len(probas)>3 else 0)*100)
        
        # Identificação explicável dos fatores de risco
        fatores = []
        if temp >= 40.0:
            fatores.append(f"Hipertermia severa detectada pelo sensor IoT ({temp}°C).")
        elif temp >= 39.4:
            fatores.append(f"Temperatura corporal febril ({temp}°C) acima do limiar biológico.")
        elif temp < 37.3:
            fatores.append(f"Hipotermia corporal detectada ({temp}°C).")
            
        if atividade < 30:
            fatores.append(f"Letargia acentuada identificada pela telemetria IoB (Índice: {atividade}/100).")
            
        if atraso_vacina > 0:
            fatores.append(f"Imunização atrasada em {atraso_vacina} dias (janela imunológica desprotegida).")
            
        if delta_peso < -5.0:
            fatores.append(f"Queda ponderal de peso recente ({delta_peso}%).")
            
        if med_continuo:
            fatores.append("Animal sob regime terapêutico medicamentoso contínuo.")
            
        if not fatores:
            fatores.append("Parâmetros fisiológicos, térmicos e vacinais dentro da normalidade.")
            
        recomendacoes = {
            'BAIXO': 'Manter rotina preventiva de alimentação e atividades. Animal clinicamente estável.',
            'MODERADO': 'Agendar consulta clínica eletiva nos próximos 15 dias e regularizar reforços vacinais.',
            'ALTO': 'Recomenda-se avaliação veterinária em até 24-48 horas para investigação diagnóstica de febre/letargia.',
            'CRITICO': 'Atenção Imediata: risco de choque térmico ou sepse aguda. Conduzir ao pronto-atendimento 24h.'
        }
        
        return {
            'nivel_risco': nome_classe,
            'classe_id': classe_predita,
            'score_risco': round(float(score_cont), 1),
            'probabilidades': {
                'BAIXO': round(float(probas[0]) * 100, 1),
                'MODERADO': round(float(probas[1]) * 100, 1),
                'ALTO': round(float(probas[2]) * 100, 1),
                'CRITICO': round(float(probas[3]) * 100, 1) if len(probas)>3 else 0.0
            },
            'fatores_alerta': fatores,
            'recomendacao_imediata': recomendacoes[nome_classe],
            'telemetria_processada': {
                'temperatura': temp,
                'atividade_iob': atividade,
                'umidade': umidade,
                'status_termico': 'FEBRE' if temp > 39.5 else ('HIPOTERMIA' if temp < 37.5 else 'NORMAL')
            }
        }

if __name__ == '__main__':
    print("=== TREINANDO MODELO PREDITIVO DE IA CLYVO VET ===")
    treinar_e_salvar_modelo()
    
    print("\n=== TESTE DE INFERÊNCIA ===")
    clf = ClassificadorRiscoVeterinario()
    
    caso_rex = {
        'nome': 'Rex',
        'especie': 'CANINO',
        'porte': 'GRANDE',
        'idade_anos': 4.5,
        'temperatura_atual': 39.8,
        'delta_temperatura_24h': 1.1,
        'umidade_ambiente': 52.0,
        'atraso_vacina_dias': 45,
        'variacao_peso_pct': -3.2,
        'medicamento_continuo': False,
        'indice_atividade_iob': 28.0
    }
    
    resultado = clf.analisar_risco(caso_rex)
    print(f"Paciente: Rex")
    print(f"Nível de Risco: {resultado['nivel_risco']} ({resultado['score_risco']}%)")
    print(f"Fatores de Alerta: {resultado['fatores_alerta']}")
    print(f"Recomendação: {resultado['recomendacao_imediata']}")
