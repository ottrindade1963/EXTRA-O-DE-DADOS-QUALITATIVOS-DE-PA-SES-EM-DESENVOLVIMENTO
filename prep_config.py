"""Configurações para preparação de dados para modelagem."""
import os

BASE_DIR = os.path.dirname(__file__)

# Datasets de entrada (na raiz do repositório)
DATASETS = {
    "inner":  os.path.join(BASE_DIR, "agregado_inner.csv"),
    "left":   os.path.join(BASE_DIR, "agregado_left_imputado.csv"),
    "outer":  os.path.join(BASE_DIR, "agregado_outer_completo.csv"),
}

# Variáveis quantitativas (features económicas)
QUANT_VARS = [
    'pib_per_capita_ppc',
    'formacao_bruta_capital_fixo_percent_pib',
    'matricula_ensino_secundario_percent',
    'comercio_percent_pib',
    'investimento_estrangeiro_direto_percent_pib',
    'populacao_total',
    'emprego_industria_percent_emprego_total',
    'valor_agregado_industrial_percent_pib'
]

# Variáveis qualitativas (governança)
QUAL_VARS = [
    'wgi_control_corruption',
    'wgi_gov_effectiveness',
    'wgi_political_stability',
    'wgi_regulatory_quality',
    'wgi_rule_law',
    'wgi_voice_accountability',
    'icrg_qog'
]

# Todas as features numéricas
ALL_FEATURES = QUANT_VARS + QUAL_VARS

# Variável alvo (target) padrão
TARGET = 'pib_per_capita_ppc'

# Variáveis com assimetria forte → transformação log
LOG_TRANSFORM_VARS = ['populacao_total', 'investimento_estrangeiro_direto_percent_pib']

# Lags para engenharia de features temporais
LAGS = [1, 2, 3]

# Janela deslizante para médias móveis
ROLLING_WINDOWS = [3, 5]

# Janela de entrada para LSTM e TFT (passos de tempo)
SEQ_LENGTH = 5

# Horizonte de previsão
FORECAST_HORIZON = 1

# Proporção treino/teste (split temporal)
TRAIN_RATIO = 0.8

# Pasta de saída
OUTPUT_DIR = os.path.join(BASE_DIR, "dados_preparados")
os.makedirs(OUTPUT_DIR, exist_ok=True)
