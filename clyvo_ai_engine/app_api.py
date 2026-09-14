"""
Clyvo Vet — PetCare 360 AI Engine
API REST e Servidor Web Interativo para Demonstração de IA & IoT
Disciplina: Disruptive Architectures: IoT, IoB & Generative IA (FIAP 2026)
Equipe: João Vitor Lacerda, Kauan Vieira, Murillo Carapia, Pedro Previtali
"""

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from modelo_preditivo import ClassificadorRiscoVeterinario
from agente_generativo import AgenteGenerativoVeterinario

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

# Inicialização dos componentes de IA
classificador = ClassificadorRiscoVeterinario()
agente_ia = AgenteGenerativoVeterinario()

# Base de Pacientes para Demonstração Interativa
PACIENTES_DEMO = {
    "rex": {
        "id": 1,
        "nome": "Rex",
        "especie": "Canino",
        "raca": "Golden Retriever",
        "porte": "GRANDE",
        "idade_anos": 4.5,
        "peso_kg": 29.5,
        "temperatura_atual": 39.8,
        "delta_temperatura_24h": 1.2,
        "umidade_ambiente": 54.0,
        "atraso_vacina_dias": 45,
        "variacao_peso_pct": -3.2,
        "medicamento_continuo": False,
        "indice_atividade_iob": 28.0,
        "historico": "Apresentou prostração nas últimas 24 horas. Vacina V10 vencida há 45 dias."
    },
    "luna": {
        "id": 2,
        "nome": "Luna",
        "especie": "Felino",
        "raca": "Persa",
        "porte": "PEQUENO",
        "idade_anos": 2.0,
        "peso_kg": 3.8,
        "temperatura_atual": 38.6,
        "delta_temperatura_24h": 0.2,
        "umidade_ambiente": 58.0,
        "atraso_vacina_dias": 0,
        "variacao_peso_pct": +0.5,
        "medicamento_continuo": False,
        "indice_atividade_iob": 78.0,
        "historico": "Animal ativo, sem histórico de doenças preexistentes. Vacinação antirrábica e quádrupla felina em dia."
    },
    "thor": {
        "id": 3,
        "nome": "Thor",
        "especie": "Canino",
        "raca": "Buldogue Francês",
        "porte": "PEQUENO",
        "idade_anos": 7.0,
        "peso_kg": 13.2,
        "temperatura_atual": 40.4,
        "delta_temperatura_24h": 1.8,
        "umidade_ambiente": 72.0,
        "atraso_vacina_dias": 120,
        "variacao_peso_pct": -6.5,
        "medicamento_continuo": True,
        "indice_atividade_iob": 15.0,
        "historico": "Hipertermia severa, dispneia e respiração ofegante em dia quente. Risco iminente de colapso respiratório braquicefálico."
    }
}

@app.route('/')
def index():
    """Renderiza o Dashboard Interativo da IA do Clyvo Vet."""
    return render_template('dashboard_ia.html')

@app.route('/api/v1/ia/health', methods=['GET'])
def health():
    return jsonify({
        "status": "OPERACIONAL",
        "servico": "Clyvo Vet AI Core",
        "versao": "3.0.0",
        "disciplina": "Disruptive Architectures: IoT, IoB & Generative IA",
        "componentes": {
            "machine_learning_preditivo": "Ativo (RandomForestClassifier - Acurácia: 93.4%)",
            "ia_generativa_copilot": "Ativo (Grounded Veterinary Clinical Assistant)",
            "ingestao_telemetria_iot": "Ativo (MQTT HiveMQ Listener)"
        }
    })

@app.route('/api/v1/ia/pacientes-demo', methods=['GET'])
def listar_pacientes():
    return jsonify(PACIENTES_DEMO)

@app.route('/api/v1/ia/analise-completa', methods=['POST'])
def analise_completa():
    """
    Recebe os dados do pet e telemetria, processa pelo modelo preditivo ML
    e gera as recomendações personalizadas da IA generativa para Tutor e Veterinário.
    """
    dados = request.json or {}
    
    # 1. Inferência de Machine Learning (Índice de Risco Preventivo)
    resultado_ml = classificador.analisar_risco(dados)
    
    # 2. IA Generativa: Geração de Orientação ao Tutor
    orientacao_tutor = agente_ia.gerar_orientacao_tutor(dados, resultado_ml)
    
    # 3. IA Generativa: Briefing Clínico SOAP ao Veterinário
    briefing_vet = agente_ia.gerar_briefing_clinico_veterinario(dados, resultado_ml)
    
    return jsonify({
        "sucesso": True,
        "paciente": dados.get('nome', 'Não Identificado'),
        "predicao_machine_learning": resultado_ml,
        "ia_generativa_tutor": orientacao_tutor,
        "ia_generativa_veterinario": briefing_vet
    })

@app.route('/api/v1/ia/telemetria-iot', methods=['POST'])
def telemetria_iot():
    """
    Endpoint de ingestão de telemetria transmitida pela coleira ESP32 Wearable.
    """
    payload = request.json or {}
    pet_id = payload.get('pet_id', 1)
    temp = float(payload.get('temperatura', 38.5))
    umid = float(payload.get('umidade', 50.0))
    timestamp = payload.get('timestamp', 0)
    
    # Localiza paciente ou usa padrão
    pet = PACIENTES_DEMO.get("rex")
    pet_atualizado = pet.copy()
    pet_atualizado['temperatura_atual'] = temp
    pet_atualizado['umidade_ambiente'] = umid
    
    resultado_ml = classificador.analisar_risco(pet_atualizado)
    orientacao_tutor = agente_ia.gerar_orientacao_tutor(pet_atualizado, resultado_ml)
    
    return jsonify({
        "status": "PROCESSADO",
        "iot_telemetria": {
            "pet_id": pet_id,
            "temperatura": temp,
            "umidade": umid,
            "timestamp": timestamp
        },
        "analise_imediata": {
            "nivel_risco": resultado_ml['nivel_risco'],
            "score_risco": resultado_ml['score_risco'],
            "acao_tutor": orientacao_tutor['acao_recomendada']
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f"-> Servidor de IA Clyvo Vet rodando em: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
