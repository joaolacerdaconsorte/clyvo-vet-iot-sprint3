# Clyvo Vet — PetCare 360 IoT Wearable (Sprint 1)

Este repositório contém o código-fonte, diagrama de conexões e configurações da solução de **IoT (Internet of Things)** desenvolvida para o ecossistema de saúde preventiva animal **Clyvo Vet / PetCare 360**.

---

## 1. Descrição do Projeto

Com o objetivo de transformar a jornada de saúde animal em um modelo proativo, preventivo e contínuo, a **Clyvo Vet** projetou um **Wearable IoT (Coleira Inteligente)** para monitoramento contínuo da temperatura e umidade corporal de animais de estimação.

O dispositivo consiste em um microcontrolador **ESP32** equipado com um sensor de temperatura e umidade de alta precisão (**DHT22**), um **LED RGB** para sinalização visual de alertas locais e integração com um **Broker MQTT** na nuvem para envio de telemetria em tempo real.

---

## 2. Arquitetura de Hardware e Conexões

### Componentes Utilizados
*   **ESP32 DevKit v4** (Microcontrolador com conectividade Wi-Fi e Bluetooth)
*   **Sensor DHT22** (Sensor digital de Temperatura e Umidade)
*   **LED RGB** (Cátodo comum, representando alertas de saúde localmente)
*   **3 Resistores de 1kΩ** (Limitadores de corrente para proteção dos pinos do LED RGB)

### Esquema de Conexão Física (Pinagem)
*   **Sensor DHT22:**
    *   `VCC` ➔ `ESP32 3V3`
    *   `SDA` (Sinal de Dados) ➔ `ESP32 GPIO 4`
    *   `GND` ➔ `ESP32 GND`
*   **LED RGB:**
    *   `Pino Vermelho (R)` ➔ Resistor 1kΩ ➔ `ESP32 GPIO 25`
    *   `Pino Verde (G)` ➔ Resistor 1kΩ ➔ `ESP32 GPIO 26`
    *   `Pino Azul (B)` ➔ Resistor 1kΩ ➔ `ESP32 GPIO 27`
    *   `Cátodo Comum (GND)` ➔ `ESP32 GND`

---

## 3. Lógica de Alertas Preventivos

O firmware realiza leituras térmicas a cada 5 segundos e toma decisões locais baseadas nos padrões biológicos de temperatura veterinária:

1.  **Status NORMAL (37.5°C a 39.5°C):**
    *   O pet está em temperatura corporal saudável.
    *   O LED RGB brilha na cor **VERDE**.
    *   Status publicado: `"NORMAL"`.
2.  **Status ALERTA_FEBRE (> 39.5°C):**
    *   Indica febre ou estresse térmico severo, requerendo atenção do veterinário.
    *   O LED RGB brilha na cor **VERMELHA** (LED Vermelho em ALTO).
    *   Status publicado: `"ALERTA_FEBRE"`.
3.  **Status ALERTA_HIPOTERMIA (< 37.5°C):**
    *   Indica risco de hipotermia devido à exposição ao frio extremo ou recuperação anestésica.
    *   O LED RGB brilha na cor **AZUL** (LED Azul em ALTO).
    *   Status publicado: `"ALERTA_HIPOTERMIA"`.

---

## 4. Comunicação MQTT e Nuvem

O dispositivo conecta-se automaticamente à rede Wi-Fi e estabelece conexão com o Broker público **HiveMQ** (`broker.hivemq.com` na porta `1883`).

As informações de telemetria são serializadas em formato **JSON** e publicadas periodicamente no tópico `petcare360/telemetria`:

```json
{
  "pet_id": 1,
  "temperatura": 38.2,
  "umidade": 52.4,
  "timestamp": 125000,
  "status": "NORMAL"
}
```

---

## 5. Simulador Wokwi e Código-Fonte

Este diretório contém os arquivos de simulação e código-fonte originais:
*   **Código Principal:** [sketch.ino](sketch.ino)
*   **Conexões do Hardware:** [diagram.json](diagram.json)
*   **Bibliotecas do Projeto:** [libraries.txt](libraries.txt)
*   **Link para Simulação Online Interativa:** [Wokwi - PetCare 360 IoT](https://wokwi.com/projects/464135788106122241)

---

## 6. Identificação da Equipe (Turma: 2TDSPW)
*   **João Vitor Lacerda** — RM 565565
*   **Kauan Vieira de Lima** — RM 565403
*   **Murillo Fernandes Carapia** — RM 564969
