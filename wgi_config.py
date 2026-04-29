"""Configurações para download e processamento de indicadores WGI."""
import os

# URLs da API do Banco Mundial para WGI
WGI_API_BASE = "https://api.worldbank.org/v2"

# Mapeamento de indicadores WGI
WGI_INDICATORS = {
    'VA.EST': 'wgi_voice_accountability',
    'PV.EST': 'wgi_political_stability',
    'GE.EST': 'wgi_gov_effectiveness',
    'RQ.EST': 'wgi_regulatory_quality',
    'RL.EST': 'wgi_rule_law',
    'CC.EST': 'wgi_control_corruption'
}

# Nomes descritivos dos indicadores
NOMES_INDICADORES = {
    'wgi_voice_accountability': 'Voz e Responsabilidade',
    'wgi_political_stability': 'Estabilidade Política',
    'wgi_gov_effectiveness': 'Efetividade Governamental',
    'wgi_regulatory_quality': 'Qualidade Regulatória',
    'wgi_rule_law': 'Estado de Direito',
    'wgi_control_corruption': 'Controle de Corrupção'
}

# Período de cobertura
ANO_MINIMO = 1996
ANO_MAXIMO = 2024

# Caminhos de saída
OUTPUT_DIR = "dados_qualitativos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_OUTPUT = f"{OUTPUT_DIR}/dados_qualitativos.csv"
XLSX_OUTPUT = f"{OUTPUT_DIR}/dados_qualitativos.xlsx"

# Configurações de requisição
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos
