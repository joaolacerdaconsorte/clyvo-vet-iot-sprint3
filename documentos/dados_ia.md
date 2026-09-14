# Engenharia de Dados & Governança da IA — CLYVO VET

**Disciplina:** Disruptive Architectures: IoT, IoB & Generative IA (Sprint 3 — FIAP 2026)  
**Projeto:** CLYVO VET (PetCare 360)  
**Equipe (Turma 2TDSPW):**
- João Vitor Lacerda — RM 565565
- Kauan Vieira de Lima — RM 565403
- Murillo Fernandes Carapia — RM 564969
- Pedro de Matos Previtali — RM 564184

---

## 1. Inventário das Fontes de Dados

Para viabilizar a predição clínica precisa e a geração contextualizada de orientações, o ecossistema CLYVO VET consome quatro fontes de dados primárias:

| Fonte de Dados | Origem | Protocolo / Meio | Frequência de Coleta | Tipo de Dado |
| :--- | :--- | :--- | :--- | :--- |
| **Telemetria Biométrica & Microclima** | Coleira Wearable ESP32 (DHT22) | MQTT (Tópico `petcare360/telemetria`) | A cada 5 seg. (modo demo) / a cada 15 min. (produção) | Streaming Contínuo |
| **Comportamento Animal (IoB)** | Acelerômetro / Análise de Padrão Motor | Agregação no Gateway / Ingestion API | Consolidado a cada 1 hora / 24 horas | Time-Series & Agregações |
| **Prontuário e Cadastro Clínico** | Prontuário Eletrônico da Clínica (Oracle DB) | API REST Interna (JSON) | Sob demanda (consultas, pesagens, receitas) | Estruturado Relacional |
| **Calendário Sanitário Preventivo** | Módulo de Vacinação e Controle Parasitário | Job Batch Noturno / Triggers de Evento | Verificação Diária / Atualização por dose | Estruturado Tabular |

---

## 2. Estrutura e Dicionário de Features (Dataset da IA)

O modelo preditivo de Machine Learning (`RandomForestClassifier`) processa um vetor de 10 variáveis críticas normalizadas:

### Tabela de Features de Entrada

| Feature | Tipo | Unidade / Domínio | Faixa Típica | Relevância Clínica / Fisiológica |
| :--- | :--- | :--- | :--- | :--- |
| `especie_id` | Inteiro (Categórica) | 0: Canino, 1: Felino | {0, 1} | Limiares térmicos e susceptibilidades patológicas distintas entre espécies. |
| `porte_id` | Inteiro (Categórica) | 0: Pequeno, 1: Médio, 2: Grande | {0, 1, 2} | Taxa metabólica basal e curvas de envelhecimento variam drasticamente pelo porte. |
| `idade_anos` | Float | Anos de vida | 0.2 a 20.0 | Filhotes e geriatras possuem maior vulnerabilidade a desidratação e imunossupressão. |
| `temperatura_atual` | Float | Graus Celsius (°C) | 36.0 a 42.5 | Normotermia: 37.5°C a 39.2°C. Valores >39.5°C indicam febre; >40.5°C emergência. |
| `delta_temperatura_24h`| Float | Variação em °C nas últimas 24h | -3.0 a +3.5 | Elevações súbitas (>1.0°C) sugerem processos infecciosos agudos ou insolação. |
| `umidade_ambiente` | Float | Percentual (%) | 20.0 a 95.0 | Umidades extremas com alta temperatura potencializam choque térmico por perda de termorregulação. |
| `atraso_vacina_dias` | Inteiro | Dias decorridos do vencimento | 0 a 365+ | Janela imunológica desprotegida eleva risco de parvovirose, cinomose ou panleucopenia. |
| `variacao_peso_pct` | Float | Percentual de oscilação em 30 dias | -15.0% a +10.0% | Perda involuntária de peso >3% em 30 dias é sinal cardinal de afecções crônicas ou metabólicas. |
| `medicamento_continuo`| Inteiro (Binário) | 0: Não, 1: Sim | {0, 1} | Pacientes cardiopatas, nefropatas ou epilépticos exigem vigilância prioritária. |
| `indice_atividade_iob`| Float | Score normalizado (0 a 100) | 0.0 a 100.0 | *Internet of Behaviors*: Mede letargia/prostração (<30) vs. normocinesia (40-75) vs. hiperatividade (>85). |

### Variável-Alvo (Target)

O alvo de predição é a variável ordinal e multiclasse `nivel_risco_id`:
- **0: BAIXO (Score IRP 0 a 25%)** — Pet normotérmico, ativo, vacinação em dia, peso estável.
- **1: MODERADO (Score IRP 26 a 50%)** — Leves oscilações térmicas, vacina ligeiramente atrasada ou discreta queda na atividade motora.
- **2: ALTO (Score IRP 51 a 75%)** — Temperatura febril (39.5°C a 40.2°C), prostração detectada pelo IoB, imunização vencida.
- **3: CRÍTICO (Score IRP 76 a 100%)** — Hipertermia severa (>40.3°C), apatia aguda, risco iminente de colapso circulatório ou choque.

---

## 3. Estratégia de Personalização da IA

A IA da CLYVO VET não entrega uma resposta genérica estática. A estratégia de personalização baseia-se em segmentação comportamental e clínica:

### 1. Personalização para o Tutor (Persona: Tutor Copilot)
- **Tom de Voz:** Empático, tranquilizador, preventivo e desprovido de termos herméticos da medicina veterinária.
- **Adaptação por Gravidade:**
  - *Baixo Risco:* Reforço positivo dos bons hábitos do tutor, parabéns pelos cuidados e sugestão de atividades de enriquecimento ambiental.
  - *Moderado Risco:* Alerta orientativo ("Notei que Rex está um pouco mais quieto hoje..."), instruindo observação da ingestão de água e apetite nas próximas 12 horas.
  - *Alto / Crítico:* Chamada clara para ação ("Atenção: Luna está com temperatura febril. Recomendamos agendar uma consulta nas próximas horas"), disponibilizando botão de agendamento em 1 clique.
- **Contextualização com Nome e Raça:** Citações diretas ao nome do animal e particularidades (e.g., alerta específico de respiração para raças braquicefálicas como Buldogue e Pug).

### 2. Personalização para o Veterinário (Persona: Grounded Clinical Assistant)
- **Padronização Internacional SOAP:**
  - **S (Subjetivo):** Queixa principal consolidada a partir da telemetria comportamental e relato registrado do tutor.
  - **O (Objetivo):** Dados vitais exatos aferidos pela coleira, datas de vencimento de vacinas, peso e variações percentuais.
  - **A (Avaliação):** Índice de Risco Preventivo (IRP) calculado pelo modelo Random Forest, com lista de diagnósticos diferenciais prováveis ordenados por relevância.
  - **P (Plano de Conduta):** Sugestões de exames complementares (hemograma, PCR, bioquímica sérica, ultrassom) e condutas emergenciais recomendadas.
- **Apoio à Decisão Sem Alucinação:** As hipóteses diagnósticas são estritamente ancoradas nos fatores patológicos detectados pelas regras clínicas e probabilidades estatísticas da predição.

---

## 4. Considerações Éticas, Segurança e Privacidade (LGPD)

A implementação do sistema atende às melhores práticas de governança de dados em saúde e inteligência artificial responsável:

### 1. Princípio Human-in-the-Loop (Supervisão Humana Obrigatória)
- **A IA da CLYVO VET é uma ferramenta de triagem, suporte à decisão e facilitação de comunicação, NUNCA substituindo o julgamento do Médico Veterinário habilitado.**
- O sistema **não emite receitas de antimicrobianos, sedativos ou diagnósticos finais definitivos de forma autônoma**, em estrito cumprimento às normas do Conselho Federal de Medicina Veterinária (CFMV).

### 2. Conformidade com a Lei Geral de Proteção de Dados (LGPD)
- **Minimização de Dados:** O microcontrolador ESP32 transmite apenas `pet_id`, `temperatura`, `umidade` e `timestamp`. Nenhum dado pessoal do tutor (nome, CPF, endereço, telefone) transita na camada de rádio ou no broker MQTT.
- **Pseudonimização:** A associação entre a coleira e os dados cadastrais do tutor ocorre exclusivamente na camada interna segura do backend, mediante tokens de autenticação criptografados.
- **Consentimento Explícito:** O tutor autoriza formalmente a coleta de telemetria contínua durante a contratação do plano de cuidado preventivo da CLYVO VET.

### 3. Explicabilidade da Inteligência Artificial (XAI)
- Em conformidade com os princípios de transparência algorítmica, o modelo de predição nunca opera como "caixa preta". Toda predição é acompanhada dos **Fatores de Alerta** pontuais que justificaram o score (e.g., *"Temperatura corporal febril (39.8°C) acima do limiar biológico"*, *"Letargia acentuada identificada pela telemetria IoB"*).
