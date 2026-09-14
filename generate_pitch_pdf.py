# -*- coding: utf-8 -*-
"""
generate_pitch_pdf.py
Gera o documento técnico oficial da Sprint 3 em PDF no estilo suíço minimalista (Helvetica Bold).
Inclui o Diagrama Arquitetural de Alta Resolução integrado na documentação.
Atende 100% aos critérios e objetivos de avaliação da FIAP.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_PATH = r"C:\Users\joaov\Desktop\clyvo-vet-iot-sprint3\video_pitch\fonts\Helvetica-Bold-02.ttf"
pdfmetrics.registerFont(TTFont("HelvBold", FONT_PATH))

PAGE_W, PAGE_H = A4 # 595.27 x 841.89 pt
MARGIN_X = 50.0
MARGIN_TOP = 50.0
RIGHT_MARGIN = PAGE_W - MARGIN_X
PRINTABLE_W = PAGE_W - (2 * MARGIN_X)

DIAGRAM_PNG = r"C:\Users\joaov\Desktop\clyvo-vet-iot-sprint3\documentos\diagrama-arquitetural-render.png"

def draw_header_footer(c, page_num, total_pages=6):
    # Header
    c.setFont("HelvBold", 8)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, PAGE_H - 35, "fiap 2026 • disruptive architectures: iot, iob & ia generativa")
    c.drawRightString(RIGHT_MARGIN, PAGE_H - 35, "sprint 3 • clyvo vet (petcare 360)")
    c.setStrokeColorRGB(0.1, 0.1, 0.1)
    c.setLineWidth(0.75)
    c.line(MARGIN_X, PAGE_H - 42, RIGHT_MARGIN, PAGE_H - 42)

    # Footer
    c.line(MARGIN_X, 42, RIGHT_MARGIN, 42)
    c.setFont("HelvBold", 8)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(MARGIN_X, 30, "turma 2tdspw • joão vitor lacerda, kauan vieira, murillo carapia, pedro previtali")
    c.drawRightString(RIGHT_MARGIN, 30, f"{page_num:02d} / {total_pages:02d}")

def wrap_text(c, text, font_name, font_size, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for w in words:
        test_line = ' '.join(current_line + [w])
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line.append(w)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [w]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_wrapped(c, text, x, y, font_name, font_size, leading, max_width, color=(0.1, 0.1, 0.1)):
    c.setFont(font_name, font_size)
    c.setFillColorRGB(*color)
    lines = wrap_text(c, text, font_name, font_size, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    total_pages = 6

    # ==================== PÁGINA 1: CAPA & LINKS OBRIGATÓRIOS ====================
    draw_header_footer(c, 1, total_pages)
    y = PAGE_H - 85

    c.setFont("HelvBold", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(MARGIN_X, y, "documentação técnica oficial de inteligência artificial.")
    y -= 26

    c.setFont("HelvBold", 34)
    c.setFillColorRGB(0.05, 0.05, 0.05)
    c.drawString(MARGIN_X, y, "clyvo vet • petcare 360.")
    y -= 18

    c.setFont("HelvBold", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(MARGIN_X, y, "arquitetura de ia híbrida e telemetria contínua para saúde animal.")
    y -= 25

    # Links Box
    c.setStrokeColorRGB(0.1, 0.1, 0.1)
    c.setLineWidth(1)
    c.rect(MARGIN_X, y - 118, PRINTABLE_W, 118, stroke=1, fill=0)

    c.setFont("HelvBold", 9)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X + 16, y - 18, "ENTREGÁVEIS OBRIGATÓRIOS CONFORME EDITAL FIAP:")
    
    c.drawString(MARGIN_X + 16, y - 36, "• Link do Vídeo Pitch no YouTube (Modo Não Listado — 5m 41s):")
    c.setFont("HelvBold", 8.5)
    c.setFillColorRGB(0.2, 0.4, 0.8)
    c.drawString(MARGIN_X + 26, y - 48, "https://youtu.be/6eNdyt8E9Jk")

    c.setFont("HelvBold", 9)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X + 16, y - 64, "• Repositório GitHub Oficial (Código, IA, Firmware & README):")
    c.setFont("HelvBold", 8.5)
    c.setFillColorRGB(0.2, 0.4, 0.8)
    c.drawString(MARGIN_X + 26, y - 76, "https://github.com/joaolacerdaconsorte/clyvo-vet-iot-sprint3")

    c.setFont("HelvBold", 9)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X + 16, y - 92, "• Simulação IoT no Wokwi (ESP32 + DHT22 + HiveMQ MQTT):")
    c.setFont("HelvBold", 8.5)
    c.setFillColorRGB(0.2, 0.4, 0.8)
    c.drawString(MARGIN_X + 26, y - 104, "https://wokwi.com/projects/464135788106122241")

    y -= 138

    # Equipe Table
    c.setFont("HelvBold", 10)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "integrantes do grupo (turma 2tdspw):")
    y -= 12
    c.line(MARGIN_X, y, RIGHT_MARGIN, y)
    y -= 16

    team = [
        ("01. João Vitor Lacerda", "RM 565565"),
        ("02. Kauan Vieira de Lima", "RM 565403"),
        ("03. Murillo Fernandes Carapia", "RM 564969"),
        ("04. Pedro de Matos Previtali", "RM 564184")
    ]
    for name, rm in team:
        c.setFont("HelvBold", 9)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.drawString(MARGIN_X + 8, y, name)
        c.drawRightString(RIGHT_MARGIN - 8, y, rm)
        y -= 14
        c.setStrokeColorRGB(0.9, 0.9, 0.9)
        c.line(MARGIN_X + 8, y + 4, RIGHT_MARGIN - 8, y + 4)
        c.setStrokeColorRGB(0.1, 0.1, 0.1)

    y -= 16

    # Seção 1: Problema de Negócio
    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "1. definição do problema de negócio e jornada contínua.")
    y -= 14

    p1 = (
        "No modelo veterinário convencional, o cuidado à saúde animal é predominantemente reativo e tardio. "
        "Cães e gatos possuem o instinto biológico de ocultar dor e vulnerabilidade em fases iniciais de patologias, "
        "fazendo com que tutores só procurem atendimento médico quando o quadro clínico já atingiu severidade aguda. "
        "Adicionalmente, entre as consultas anuais há um completo apagão de dados sobre temperatura, oscilação de peso "
        "e padrão motor diário do pet (Internet of Behaviors - IoB). Esse atraso diagnóstico eleva os riscos de complicações, "
        "encarece tratamentos em internações de UTI evitáveis e sobrecarrega os veterinários com anamneses manuais e imprecisas. "
        "A Clyvo Vet soluciona esse gargalo ao estabelecer uma jornada preventiva contínua 360 graus."
    )
    y = draw_wrapped(c, p1, MARGIN_X, y, "HelvBold", 8.5, 11.5, PRINTABLE_W)

    c.showPage()

    # ==================== PÁGINA 2: ESCOLHA & JUSTIFICATIVA DA IA ====================
    draw_header_footer(c, 2, total_pages)
    y = PAGE_H - 65

    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "2. escolha e justificativa técnica da abordagem de ia.")
    y -= 16

    p_ia_intro = (
        "Optou-se por uma Abordagem Híbrida e Complementar, unindo Machine Learning Supervisionado Tradicional "
        "(Random Forest Classifier) a uma camada de Inteligência Artificial Generativa Ancorada (Grounded Clinical Agent). "
        "Essa decisão fundamenta-se nas restrições críticas do ecossistema de saúde veterinária:"
    )
    y = draw_wrapped(c, p_ia_intro, MARGIN_X, y, "HelvBold", 8.5, 11.5, PRINTABLE_W)
    y -= 10

    # Comparativo em 3 Caixas
    box_w = (PRINTABLE_W - 20) / 3
    box_h = 240

    # Box 1: Por que não LLM puro?
    bx1 = MARGIN_X
    c.rect(bx1, y - box_h, box_w, box_h, stroke=1, fill=0)
    c.setFont("HelvBold", 8.5)
    c.drawString(bx1 + 10, y - 18, "POR QUE NÃO LLM PURO?")
    t1 = (
        "• Risco Crítico de Alucinação:\n"
        "LLMs podem oscilar em limiares vitais estritos (ex: 39.8°C vs 40.5°C).\n\n"
        "• Custo e Latência Inviáveis:\n"
        "Inviável acionar chamadas pesadas de linguagem para streaming massivo de telemetria IoT contínua.\n\n"
        "• Ausência de Calibração:\n"
        "LLMs não oferecem probabilidades estatísticas formais e auditáveis de risco clínico."
    )
    y_inner = y - 35
    for par in t1.split('\n'):
        if par:
            y_inner = draw_wrapped(c, par, bx1 + 10, y_inner, "HelvBold", 7.5, 9.5, box_w - 20)
        else:
            y_inner -= 4

    # Box 2: Por que não ML tradicional isolado?
    bx2 = MARGIN_X + box_w + 10
    c.rect(bx2, y - box_h, box_w, box_h, stroke=1, fill=0)
    c.setFont("HelvBold", 8.5)
    c.drawString(bx2 + 10, y - 18, "POR QUE NÃO ML ISOLADO?")
    t2 = (
        "• Vetores Numéricos Frios:\n"
        "Algoritmos tabulares geram apenas números brutos (ex: Score 78.5%), ininteligíveis ao tutor leigo.\n\n"
        "• Falta de Acolhimento Empático:\n"
        "Não acolhem a família nem fornecem primeiros socorros em linguagem natural.\n\n"
        "• Sem Raciocínio Clínico:\n"
        "Incapacidade de sintetizar prontuários médicos e diagnósticos diferenciais no padrão SOAP."
    )
    y_inner = y - 35
    for par in t2.split('\n'):
        if par:
            y_inner = draw_wrapped(c, par, bx2 + 10, y_inner, "HelvBold", 7.5, 9.5, box_w - 20)
        else:
            y_inner -= 4

    # Box 3: Solução Híbrida
    bx3 = MARGIN_X + (box_w + 10) * 2
    c.rect(bx3, y - box_h, box_w, box_h, stroke=1, fill=0)
    c.setFont("HelvBold", 8.5)
    c.drawString(bx3 + 10, y - 18, "A SOLUÇÃO HÍBRIDA CLYVO")
    t3 = (
        "• 1. Random Forest (93.4% Acc):\n"
        "Classifica 10 features, calcula o Índice IRP e extrai fatores patológicos de alerta.\n\n"
        "• 2. Grounded Clinical GenAI:\n"
        "Ancorada nos dados do modelo:\n"
        "→ Tutor Copilot: orientações claras, acolhedoras e agendamento 1-clique.\n"
        "→ Vet SOAP Assistant: estruturação de prontuário e diagnósticos diferenciais."
    )
    y_inner = y - 35
    for par in t3.split('\n'):
        if par:
            y_inner = draw_wrapped(c, par, bx3 + 10, y_inner, "HelvBold", 7.5, 9.5, box_w - 20)
        else:
            y_inner -= 4

    y -= (box_h + 20)

    # Seção 3: Estratégia de Personalização
    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "3. estratégia de personalização e apoio à tomada de decisão.")
    y -= 14

    p_pers = (
        "A personalização é estruturada em dois eixos operacionais:\n"
        "1. Personalização para o Tutor (Tutor Copilot): adapta o vocabulário à espécie e porte do animal, "
        "removendo jargões cirúrgicos. Classifica a urgência e fornece botão de agendamento em 1 clique em casos de risco.\n"
        "2. Personalização para o Médico Veterinário (Vet Clinical Assistant): sintetiza automaticamente o histórico, "
        "as séries de telemetria e o perfil imunológico no formato SOAP (Subjetivo, Objetivo, Avaliação, Plano), "
        "sugerindo hipóteses diagnósticas diferenciais fundamentadas estatisticamente pela predição do modelo."
    )
    for line in p_pers.split('\n'):
        y = draw_wrapped(c, line, MARGIN_X, y, "HelvBold", 8.5, 11.5, PRINTABLE_W)
        y -= 3

    c.showPage()

    # ==================== PÁGINA 3: DIAGRAMA ARQUITETURAL DA SOLUÇÃO ====================
    draw_header_footer(c, 3, total_pages)
    y = PAGE_H - 65

    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "4. diagrama arquitetural da solução (visão ponta a ponta).")
    y -= 14

    p_diag_desc = (
        "A arquitetura integra a camada de sensoriamento de borda (IoT/IoB), ingestão e mensageria em nuvem, "
        "o motor analítico híbrido de Inteligência Artificial e a entrega de valor em interfaces dedicadas:"
    )
    y = draw_wrapped(c, p_diag_desc, MARGIN_X, y, "HelvBold", 8.5, 11.5, PRINTABLE_W)
    y -= 10

    # Render do Diagrama Arquitetural de Alta Resolução
    diag_w = PRINTABLE_W
    diag_h = diag_w * (680.0 / 1200.0) # Aspect ratio original 1200x680 -> ~280.6 pt
    
    if os.path.exists(DIAGRAM_PNG):
        c.drawImage(DIAGRAM_PNG, MARGIN_X, y - diag_h, width=diag_w, height=diag_h, preserveAspectRatio=True)
    else:
        c.rect(MARGIN_X, y - diag_h, diag_w, diag_h, stroke=1, fill=0)
        c.drawCentredString(MARGIN_X + (diag_w / 2.0), y - (diag_h / 2.0), "[DIAGRAMA ARQUITETURAL]")

    y -= (diag_h + 16)

    # Detalhamento das 4 Macro-Camadas Estruturais
    c.setFont("HelvBold", 9)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "DETALHAMENTO TÉCNICO DAS 4 MACRO-CAMADAS DO ECOSSISTEMA:")
    y -= 12

    layers = [
        ("CAMADA 01: BORDA IOT & IOB", "Coleira inteligente ESP32 com sensor térmico DHT22 e acelerômetro IoB. Publica leituras vitais compactadas via MQTT no tópico petcare360/telemetria."),
        ("CAMADA 02: INGESTÃO & NUVEM", "Broker MQTT HiveMQ Cloud roteia payloads para a API REST. Validação de esquemas, enriquecimento com histórico do banco relacional Oracle e normalização."),
        ("CAMADA 03: NÚCLEO DE IA HÍBRIDA", "Pipeline bifásico: Feature Store estruturada -> Random Forest Classifier (IRP e fatores críticos) -> Grounded GenAI Agent (geração controlada sem alucinações)."),
        ("CAMADA 04: APLICAÇÕES & CLÍNICA", "Tutor Copilot (app mobile para tutor com linguagem humanizada e alertas) + Vet Clinical Portal (prontuários SOAP com diagnósticos diferenciais pré-formatados).")
    ]

    box_layer_h = 32
    for lay_title, lay_body in layers:
        c.rect(MARGIN_X, y - box_layer_h, PRINTABLE_W, box_layer_h, stroke=1, fill=0)
        c.setFont("HelvBold", 7.5)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.drawString(MARGIN_X + 8, y - 10, lay_title)
        draw_wrapped(c, lay_body, MARGIN_X + 8, y - 20, "HelvBold", 6.8, 8.5, PRINTABLE_W - 16, color=(0.3, 0.3, 0.3))
        y -= (box_layer_h + 5)

    c.showPage()

    # ==================== PÁGINA 4: FLUXO DE DADOS & GOVERNANÇA ÉTICA ====================
    draw_header_footer(c, 4, total_pages)
    y = PAGE_H - 65

    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "5. fluxo de dados detalhado entre componentes (7 etapas).")
    y -= 14

    p_flow = (
        "A comunicação entre a camada de borda, nuvem, banco de dados e inteligência artificial opera em 7 etapas orquestradas:"
    )
    y = draw_wrapped(c, p_flow, MARGIN_X, y, "HelvBold", 8.5, 11.5, PRINTABLE_W)
    y -= 10

    steps = [
        ("Etapa 01: Sensoriamento de Borda", "Coleira inteligente vestível (ESP32) afere temperatura pelo sensor DHT22 e monitora índice de atividade pelo acelerômetro (IoB)."),
        ("Etapa 02: Mensageria Leve (MQTT)", "Transmissão contínua em formato JSON compacto para o Broker HiveMQ Cloud no tópico 'petcare360/telemetria' com QoS 1."),
        ("Etapa 03: Ingestão & Enriquecimento", "API REST em nuvem intercepta o payload, valida integridade e recupera histórico do pet (idade, porte, vacinas, medicamentos)."),
        ("Etapa 04: Feature Store Integrada", "Normalização do vetor de 10 variáveis fisiológicas prontas para inferência imediata sem gargalo computacional."),
        ("Etapa 05: Predição Supervisionada", "Random Forest Classifier processa o vetor, calcula o Índice IRP (0 a 100%) e estratifica a classe (Baixo, Moderado, Alto, Crítico)."),
        ("Etapa 06: Síntese Generativa Grounded", "Agente Clínico consome o output preditivo e elabora as orientações empáticas do tutor e o prontuário SOAP do veterinário."),
        ("Etapa 07: Camada de Aplicação", "Dados sincronizados em tempo real com o aplicativo do tutor e o portal clínico da Clyvo Vet.")
    ]

    for st, desc in steps:
        c.rect(MARGIN_X, y - 28, PRINTABLE_W, 28, stroke=1, fill=0)
        c.setFont("HelvBold", 8)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.drawString(MARGIN_X + 10, y - 12, st.upper())
        c.setFont("HelvBold", 7.5)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawString(MARGIN_X + 10, y - 22, desc)
        y -= 33

    y -= 10

    # Seção 6: Governança Ética & LGPD
    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "6. governança ética, segurança e privacidade (lgpd).")
    y -= 14

    gov_text = (
        "• Human-in-the-Loop Obrigatório: A IA atua estritamente como suporte à triagem e apoio à decisão clínica. "
        "A conduta médica definitiva, diagnósticos formais e prescrições terapêuticas são prerrogativas exclusivas do Médico Veterinário com CRMV habilitado.\n\n"
        "• Minimização de Dados (LGPD): O microcontrolador ESP32 trafega via MQTT unicamente identificadores opacos (pet_id) e dados telemétricos vitais. "
        "Nenhum dado pessoal do tutor (nome, CPF, endereço) circula na camada de rádio.\n\n"
        "• Explicabilidade da IA (XAI): Toda inferência preditiva do Random Forest isola os fatores patológicos determinantes que motivaram o alerta, eliminando o efeito de 'caixa-preta'."
    )
    for par in gov_text.split('\n\n'):
        y = draw_wrapped(c, par, MARGIN_X, y, "HelvBold", 8, 11, PRINTABLE_W)
        y -= 6

    c.showPage()

    # ==================== PÁGINA 5: DICIONÁRIO DE DADOS ====================
    draw_header_footer(c, 5, total_pages)
    y = PAGE_H - 65

    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "7. inventário e dicionário de dados da ia.")
    y -= 16

    c.setFont("HelvBold", 8.5)
    c.drawString(MARGIN_X, y, "TABELA DE FEATURES FISIOLÓGICAS (DATASET DE ENTRADA DO MODELO):")
    y -= 12

    headers = [("FEATURE", 110), ("TIPO / DOMÍNIO", 90), ("FAIXA TÍPICA", 80), ("RELEVÂNCIA CLÍNICA", 215)]
    x_curr = MARGIN_X
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(MARGIN_X, y - 14, PRINTABLE_W, 14, stroke=1, fill=1)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont("HelvBold", 7.5)
    for h, w in headers:
        c.drawString(x_curr + 4, y - 10, h)
        x_curr += w
    y -= 14

    features = [
        ("especie_id", "Int {0:Cão, 1:Gato}", "{0, 1}", "Diferenciação biológica de limiares térmicos."),
        ("porte_id", "Int {0:P, 1:M, 2:G}", "{0, 1, 2}", "Curvas de taxa metabólica basal e porte corporal."),
        ("idade_anos", "Float (Anos)", "0.2 a 20.0", "Vulnerabilidade imune de filhotes e geriatras."),
        ("temperatura_atual", "Float (°C)", "36.0 a 42.5", "Normotermia: 37.5°C-39.2°C. >39.5°C indica febre."),
        ("delta_temp_24h", "Float (°C/dia)", "-3.0 a +3.5", "Variações súbitas indicam infecção bacteriana aguda."),
        ("umidade_ambiente", "Float (%)", "20.0 a 95.0", "Microclima crítico para perdas térmicas por ofego."),
        ("atraso_vacina_dias", "Int (Dias)", "0 a 365+", "Janela de vulnerabilidade a patógenos severos."),
        ("variacao_peso_pct", "Float (%)", "-15% a +10%", "Perda >3% em 30 dias é sinal cardinal crônico."),
        ("medicamento_continuo","Int {0:Não, 1:Sim}","{0, 1}", "Pacientes cardiopatas ou epilépticos prioritários."),
        ("indice_atividade_iob","Float (0 a 100)", "0.0 a 100.0", "Internet of Behaviors: detecta letargia (<30) e apatia.")
    ]

    for f, t, r, rel in features:
        c.setFillColorRGB(1, 1, 1)
        c.rect(MARGIN_X, y - 14, PRINTABLE_W, 14, stroke=1, fill=0)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.setFont("HelvBold", 7)
        x_curr = MARGIN_X
        c.drawString(x_curr + 4, y - 10, f)
        x_curr += 110
        c.drawString(x_curr + 4, y - 10, t)
        x_curr += 90
        c.drawString(x_curr + 4, y - 10, r)
        x_curr += 80
        c.drawString(x_curr + 4, y - 10, rel)
        y -= 14

    y -= 18

    # Classes de Risco
    c.setFont("HelvBold", 8.5)
    c.drawString(MARGIN_X, y, "CLASSES DE RISCO (VARIÁVEL-ALVO DO CLASSIFICADOR RANDOM FOREST):")
    y -= 12

    risk_classes = [
        ("0: BAIXO RISCO (IRP 0 a 25%)", "Parâmetros basais normais, vacinação atualizada, atividade regular. Reforço de conduta preventiva."),
        ("1: RISCO MODERADO (IRP 26 a 50%)", "Pequenas oscilações térmicas, discreta hipocinesia ou vacina recentemente expirada. Monitoramento em 12-24h."),
        ("2: ALTO RISCO (IRP 51 a 75%)", "Febre confirmada (>39.5°C), letargia acentuada, perda de peso ou imunização vencida. Triagem ambulatorial."),
        ("3: RISCO CRÍTICO (IRP 76 a 100%)", "Hipertermia extrema (>40.3°C) ou prostração aguda com risco iminente de choque. Encaminhamento emergencial.")
    ]

    for rc, rdesc in risk_classes:
        c.rect(MARGIN_X, y - 20, PRINTABLE_W, 20, stroke=1, fill=0)
        c.setFont("HelvBold", 7.5)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.drawString(MARGIN_X + 8, y - 9, rc)
        c.setFont("HelvBold", 7)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawString(MARGIN_X + 8, y - 17, rdesc)
        y -= 23

    c.showPage()

    # ==================== PÁGINA 6: BENEFÍCIOS, HARDWARE & RESULTADOS ====================
    draw_header_footer(c, 6, total_pages)
    y = PAGE_H - 65

    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "8. benefícios do ecossistema para o tutor e para a clínica.")
    y -= 16

    col_w = (PRINTABLE_W - 16) / 2
    col_h = 160

    # Tutor Box
    c.rect(MARGIN_X, y - col_h, col_w, col_h, stroke=1, fill=0)
    c.setFont("HelvBold", 9)
    c.drawString(MARGIN_X + 12, y - 18, "BENEFÍCIOS PARA O TUTOR")
    tutor_b = (
        "• Tranquilidade Contínua 24/7:\n"
        "Vigilância biométrica e comportamental não invasiva na rotina familiar.\n\n"
        "• Prevenção Ativa de Doenças:\n"
        "Detecção de febre e apatia antes do agravamento sintomático visível.\n\n"
        "• Economia Real com Internações:\n"
        "Tratamentos ambulatoriais precoces evitam contas de UTI de alto custo.\n\n"
        "• Agendamento em 1 Clique:\n"
        "Orientação sem jargões e agendamento rápido com a clínica Clyvo Vet."
    )
    y_in = y - 34
    for p in tutor_b.split('\n'):
        if p:
            y_in = draw_wrapped(c, p, MARGIN_X + 12, y_in, "HelvBold", 7.5, 9.5, col_w - 24)
        else:
            y_in -= 3

    # Clinica Box
    c.rect(MARGIN_X + col_w + 16, y - col_h, col_w, col_h, stroke=1, fill=0)
    c.setFont("HelvBold", 9)
    c.drawString(MARGIN_X + col_w + 28, y - 18, "BENEFÍCIOS PARA A CLÍNICA VET")
    vet_b = (
        "• Anamnese Pré-Preenchida no SOAP:\n"
        "Redução substancial do tempo de atendimento em consulta presencial.\n\n"
        "• Triagem Inteligente de Pacientes:\n"
        "Priorização automática e cirúrgica de casos críticos e emergências.\n\n"
        "• Fidelização Perene de Clientes:\n"
        "Acompanhamento contínuo fortalece o vínculo de confiança com a clínica.\n\n"
        "• Medicina Baseada em Evidências:\n"
        "Diagnósticos embasados em dados biométricos reais e históricos do pet."
    )
    y_in = y - 34
    for p in vet_b.split('\n'):
        if p:
            y_in = draw_wrapped(c, p, MARGIN_X + col_w + 28, y_in, "HelvBold", 7.5, 9.5, col_w - 24)
        else:
            y_in -= 3

    y -= (col_h + 25)

    # Hardware & Simulação Wokwi
    c.setFont("HelvBold", 12)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(MARGIN_X, y, "9. prototipagem funcional iot e simulação wokwi.")
    y -= 16

    p_wok = (
        "Na camada de hardware, o circuito foi validado e testado no simulador online Wokwi:\n"
        "• Microcontrolador: ESP32 DevKit v1 com firmware em C++ estruturado.\n"
        "• Sensoriamento & Atuação: DHT22 para temperatura e umidade + LED RGB indicador de febre local.\n"
        "• Conectividade: Wi-Fi virtual Wokwi-GUEST conectado ao Broker HiveMQ Cloud via protocolo MQTT (porta 1883).\n"
        "• Tópico Publicado: petcare360/telemetria com payloads JSON contendo pet_id e leituras vitais.\n"
        "• Link Público da Simulação Wokwi: https://wokwi.com/projects/464135788106122241"
    )
    for line in p_wok.split('\n'):
        y = draw_wrapped(c, line, MARGIN_X, y, "HelvBold", 8, 11, PRINTABLE_W)
        y -= 3

    y -= 15

    # Resultados Parciais do Modelo
    c.rect(MARGIN_X, y - 50, PRINTABLE_W, 50, stroke=1, fill=0)
    c.setFont("HelvBold", 8.5)
    c.drawString(MARGIN_X + 12, y - 16, "RESULTADOS PARCIAIS DE ENGENHARIA DE IA:")
    c.setFont("HelvBold", 8)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(MARGIN_X + 12, y - 30, "• RandomForestClassifier treinado e serializado: modelo_risco_veterinario.joblib")
    c.drawString(MARGIN_X + 12, y - 42, "• Métrica de Performance: Acurácia Global de 93.40% em validação estratificada cruzada.")

    c.showPage()
    c.save()
    print(f"PDF gerado com sucesso: {filename}")

if __name__ == "__main__":
    out_dir = r"C:\Users\joaov\Desktop\clyvo-vet-iot-sprint3"
    out_pdf = os.path.join(out_dir, "DOCUMENTACAO_TECNICA_IA_CLYVO_VET.pdf")
    create_pdf(out_pdf)
    
    # Copia para Desktop
    desktop_pdf = r"C:\Users\joaov\Desktop\DOCUMENTACAO_TECNICA_IA_CLYVO_VET.pdf"
    import shutil
    shutil.copy2(out_pdf, desktop_pdf)
    print(f"PDF copiado para o Desktop: {desktop_pdf}")
