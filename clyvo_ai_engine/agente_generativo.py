"""
Clyvo Vet — PetCare 360 AI Engine
Módulo de IA Generativa: Assistente Clínico Veterinário e Copiloto do Tutor
Disciplina: Disruptive Architectures: IoT, IoB & Generative IA (FIAP 2026)
Equipe: João Vitor Lacerda, Kauan Vieira, Murillo Carapia, Pedro Previtali
"""

import os
import json
from datetime import datetime

class AgenteGenerativoVeterinario:
    """
    Componente de Inteligência Artificial Generativa especializado em tradução
    de telemetria IoT e predições clínicas em orientações personalizadas e humanizadas.
    """
    
    def __init__(self):
        self.versao_prompt = "v3.1-clinical-veterinary"
        
    def gerar_orientacao_tutor(self, pet: dict, analise_ml: dict) -> dict:
        """
        Gera explicação empática, personalizada e sem jargões para o tutor do animal.
        """
        nome = pet.get('nome', 'Seu pet')
        especie = pet.get('especie', 'animal')
        porte = pet.get('porte', 'médio')
        idade = pet.get('idade_anos', 3)
        nivel = analise_ml.get('nivel_risco', 'MODERADO')
        score = analise_ml.get('score_risco', 50.0)
        temp = analise_ml.get('telemetria_processada', {}).get('temperatura', 38.5)
        atividade = analise_ml.get('telemetria_processada', {}).get('atividade_iob', 70)
        fatores = analise_ml.get('fatores_alerta', [])
        
        # Persona: Especialista em Saúde Preventiva Animal da Clyvo Vet
        saudacao = f"Olá! Aqui é o assistente preventivo da Clyvo Vet com o resumo de saúde do **{nome}**."
        
        if nivel == 'BAIXO':
            tom = "tranquilo_preventivo"
            titulo = f"Tudo ótimo com o {nome}! Saúde preventiva em dia."
            mensagem_principal = (
                f"As leituras da coleira inteligente mostram que a temperatura corporal do {nome} está em **{temp:.1f}°C**, "
                f"dentro da faixa biológica saudável para a espécie. O nível de atividade física ({atividade:.0f}/100) "
                f"indica boa disposição e bem-estar geral."
            )
            orientacoes = [
                "Mantenha a rotina habitual de passeios, alimentação equilibrada e hidratação fresca.",
                "Não identificamos nenhuma vacina vencida no histórico cadastral.",
                "Sua próxima consulta de rotina preventiva pode ser agendada sem urgência."
            ]
            alerta_urgencia = False
            acao_recomendada = "Continuar monitoramento preventivo diário via coleira IoT."
            
        elif nivel == 'MODERADO':
            tom = "alerta_preventivo"
            titulo = f"Atenção preventiva recomendada para o {nome}."
            mensagem_principal = (
                f"Identificamos pequenos pontos de atenção na rotina do {nome}. A temperatura corporal está em **{temp:.1f}°C** "
                f"e os dados de telemetria apontam para uma leve alteração. "
                f"Além disso, consta uma pendência no calendário de reforços vacinais que merece atenção para manter o animal protegido."
            )
            orientacoes = [
                "Monitore a ingestão de água e o apetite nas próximas refeições.",
                "Verifique se o pet apresenta algum desânimo leve ou sensibilidade ao toque.",
                "Recomendamos agendar uma consulta preventiva na Clyvo Vet nos próximos 10 a 15 dias para atualizar a imunização."
            ]
            alerta_urgencia = False
            acao_recomendada = "Agendar consulta preventiva eletiva para atualização vacinal e checkup."
            
        elif nivel == 'ALTO':
            tom = "atencao_prioritaria"
            titulo = f"Alerta de Saúde: {nome} apresenta sinais de febre e indisposição."
            mensagem_principal = (
                f"A coleira inteligente do {nome} detectou uma temperatura de **{temp:.1f}°C**, caracterizando um quadro febril "
                f"para um animal de porte {porte.lower()}. O sensor de movimento também registrou uma queda significativa "
                f"na atividade motora ({atividade:.0f}/100), sugerindo dor, prostração ou infecção em estágio inicial."
            )
            orientacoes = [
                "Não ofereça medicamentos humanos (como paracetamol ou ibuprofeno), pois são altamente tóxicos e fatais para pets.",
                "Ofereça água fresca e mantenha o animal em local fresco e arejado.",
                "Observe se há vômito, diarreia, tosse ou mucosas pálidas.",
                "**Recomendamos agendar uma avaliação veterinária presencial nas próximas 24 horas.**"
            ]
            alerta_urgencia = True
            acao_recomendada = "Agendar atendimento clínico prioritário na Clyvo Vet em até 24h."
            
        else: # CRÍTICO
            tom = "emergencia_imediata"
            titulo = f"URGENTE: Risco crítico detectado para {nome}!"
            mensagem_principal = (
                f"Atenção tutor: Os sensores da coleira registraram parâmetros vitais fora dos limites de segurança biológica "
                f"(Temperatura: **{temp:.1f}°C**, Atividade: **{atividade:.0f}/100**). Há risco iminente de choque térmico, "
                f"desidratação severa ou complicação sistêmica aguda."
            )
            orientacoes = [
                "Dirija-se imediatamente ao hospital veterinário 24 horas mais próximo.",
                "Mantenha o pet confortável durante o transporte, sem cobri-lo com mantas pesadas se houver febre.",
                "Comunique a equipe de recepção sobre os dados térmicos da coleira inteligente."
            ]
            alerta_urgencia = True
            acao_recomendada = "Encaminhar imediatamente ao Pronto-Socorro Veterinário 24h."
            
        return {
            'destinatario': 'Tutor',
            'pet_nome': nome,
            'nivel_risco': nivel,
            'score_risco': score,
            'titulo': titulo,
            'tom': tom,
            'saudacao': saudacao,
            'mensagem_principal': mensagem_principal,
            'pontos_observacao': orientacoes,
            'acao_recomendada': acao_recomendada,
            'requer_urgencia': alerta_urgencia,
            'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }

    def gerar_briefing_clinico_veterinario(self, pet: dict, analise_ml: dict) -> dict:
        """
        Gera prontuário/sumário estruturado SOAP (Subjetivo, Objetivo, Avaliação, Plano)
        para apoiar a tomada de decisão do médico-veterinário assistente.
        """
        nome = pet.get('nome', 'Paciente')
        especie = pet.get('especie', 'Canino')
        raca = pet.get('raca', 'Indefinida')
        porte = pet.get('porte', 'Médio')
        idade = pet.get('idade_anos', 3)
        peso = pet.get('peso_kg', 25.0)
        nivel = analise_ml.get('nivel_risco', 'MODERADO')
        score = analise_ml.get('score_risco', 50.0)
        temp = analise_ml.get('telemetria_processada', {}).get('temperatura', 38.5)
        umid = analise_ml.get('telemetria_processada', {}).get('umidade', 55.0)
        ativ = analise_ml.get('telemetria_processada', {}).get('atividade_iob', 70)
        fatores = analise_ml.get('fatores_alerta', [])
        atraso_vac = pet.get('atraso_vacina_dias', 0)
        
        # Estrutura padrão SOAP (Padrão ouro em Medicina Veterinária)
        soap = {
            'S_Subjetivo': (
                f"Paciente {nome}, {especie} ({raca}, porte {porte.lower()}), {idade} anos. "
                f"Telemetria IoB acusa índice de atividade motora em {ativ:.0f}/100 "
                f"({'letargia/hipocinesia acentuada' if ativ < 40 else 'nível de atividade adequado'}). "
                f"Tutor notificado automaticamente via aplicativo Clyvo Vet."
            ),
            'O_Objetivo': {
                'temperatura_iot': f"{temp:.2f} °C (Sensor DHT22 Wearable)",
                'umidade_ambiente': f"{umid:.1f} %",
                'peso_atual': f"{peso:.2f} kg",
                'variacao_peso_recente': f"{pet.get('variacao_peso_pct', 0.0):+.1f} %",
                'status_vacinal': f"{atraso_vac} dias de atraso" if atraso_vac > 0 else "Calendário atualizado",
                'medicamento_em_curso': "Sim (uso contínuo)" if pet.get('medicamento_continuo') else "Nenhum"
            },
            'A_Avaliacao': {
                'indice_risco_preventivo_irp': f"{nivel} (Score: {score:.1f}%)",
                'fatores_patologicos_detectados': fatores,
                'diagnosticos_diferenciais_sugeridos': [
                    "Síndrome Febril Infecciosa (viral / bacteriana)",
                    "Hemoparasitose (Erliquiose / Babesiose)",
                    "Estresse Térmico / Insolação",
                    "Gastroenterite Aguda com desidratação"
                ] if temp >= 39.5 else (
                    ["Hipotermia Reativa / Choque", "Intoxicação Exógena"] if temp < 37.5 else
                    ["Exame Clínico de Rotina", "Atualização Profilática Vacinal"]
                )
            },
            'P_Plano_Conduta': [
                "Aferição manual confirmatória da temperatura retal com termômetro clínico veterinário.",
                "Exame físico completo: palpação abdominal, ausculta cardiopulmonar e avaliação de TPC (tempo de preenchimento capilar).",
                "Solicitação de Hemograma Completo + Bioquímica Sérica (ALT, Creatinina, Ureia) se persistência térmica.",
                f"{'Regularização imediata da vacina polivalente (V10) e antirrábica' if atraso_vac > 0 else 'Manutenção do protocolo profilático anual.'}",
                "Prescrição de terapia de suporte sintomática e hidratação guiada conforme diagnóstico presencial."
            ]
        }
        
        return {
            'destinatario': 'Medico_Veterinario',
            'paciente': f"{nome} ({especie} - {raca})",
            'prontuario_soap': soap,
            'alerta_prioridade': nivel,
            'suporte_decisao': "Sugestão gerada por Clyvo Vet AI Core. A decisão diagnóstica e terapêutica final é de responsabilidade exclusiva do médico-veterinário CRMV.",
            'data_emissao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }

if __name__ == '__main__':
    agente = AgenteGenerativoVeterinario()
    
    pet_exemplo = {
        'nome': 'Rex',
        'especie': 'Canino',
        'raca': 'Golden Retriever',
        'porte': 'Grande',
        'idade_anos': 4.5,
        'peso_kg': 29.5,
        'atraso_vacina_dias': 45,
        'variacao_peso_pct': -3.2,
        'medicamento_continuo': False
    }
    
    analise_exemplo = {
        'nivel_risco': 'ALTO',
        'score_risco': 78.9,
        'fatores_alerta': [
            'Temperatura corporal febril (39.8°C) acima do limiar biológico.',
            'Letargia acentuada identificada pela telemetria IoB (Índice: 28.0/100).',
            'Imunização atrasada em 45 dias (janela imunológica desprotegida).'
        ],
        'telemetria_processada': {
            'temperatura': 39.8,
            'atividade_iob': 28.0,
            'umidade': 52.0
        }
    }
    
    print("=== TESTE AGENTE GENERATIVO: TUTOR ===")
    tutor_res = agente.gerar_orientacao_tutor(pet_exemplo, analise_exemplo)
    print("Título:", tutor_res['titulo'])
    print("Mensagem:", tutor_res['mensagem_principal'])
    
    print("\n=== TESTE AGENTE GENERATIVO: VETERINÁRIO (SOAP) ===")
    vet_res = agente.gerar_briefing_clinico_veterinario(pet_exemplo, analise_exemplo)
    print("Avaliação A:", vet_res['prontuario_soap']['A_Avaliacao'])
    print("Plano P:", vet_res['prontuario_soap']['P_Plano_Conduta'])
