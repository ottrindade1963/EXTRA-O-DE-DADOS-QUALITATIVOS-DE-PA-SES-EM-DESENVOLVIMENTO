"""Configurações para download e processamento de indicadores qualitativos."""
import os

# URLs de download
WGI_URL = "https://datacatalogfiles.worldbank.org/ddh-published/0038026/DR0095946/Raw_Data_from_Underlying_Data_Sources_(1996-2024).xlsx"
QOG_URL = "https://www.qogdata.pol.gu.se/data/qog_std_ts_jan26.csv"

# Mapeamento de colunas WGI (sufixo .est = estimate)
WGI_COL_KEYWORDS = {
    'cc.est': 'wgi_control_corruption',
    'ge.est': 'wgi_gov_effectiveness',
    'ps.est': 'wgi_political_stability',
    'rl.est': 'wgi_rule_law',
    'rq.est': 'wgi_regulatory_quality',
    'va.est': 'wgi_voice_accountability'
}

# Mapeamento de colunas ICRG no QoG (versão Jan26)
ICRG_COLS = {
    'ccodealp': 'country_code',
    'year': 'year',
    'icrg_qog': 'icrg_qog'
}

# Período de cobertura
ANO_MINIMO = 1996
ANO_MAXIMO = 2024

# Caminhos de saída
OUTPUT_DIR = "dados_qualitativos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_OUTPUT = os.path.join(OUTPUT_DIR, "dados_qualitativos.csv")
XLSX_OUTPUT = os.path.join(OUTPUT_DIR, "dados_qualitativos.xlsx")

# Configurações de requisição
TIMEOUT_WGI = 60
TIMEOUT_QOG = 120
