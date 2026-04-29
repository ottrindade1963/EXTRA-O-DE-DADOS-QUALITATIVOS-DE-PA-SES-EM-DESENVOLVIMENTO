"""Configurações para segunda análise exploratória (dados limpos)."""
import os

# Caminhos
DATA_PATH = os.path.join(os.path.dirname(__file__), "wdi_emergentes_limpo.csv")
OUTPUT_DIR = "resultados_eda2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colunas numéricas
COLUNAS_NUMERICAS = [
    "pib_per_capita_ppc",
    "formacao_bruta_capital_fixo_percent_pib",
    "matricula_ensino_secundario_percent",
    "comercio_percent_pib",
    "investimento_estrangeiro_direto_percent_pib",
    "populacao_total",
    "emprego_industria_percent_emprego_total",
    "valor_agregado_industrial_percent_pib",
]

# Nomes descritivos
NOMES_VARIAVEIS = {
    "pib_per_capita_ppc": "PIB per capita (PPC)",
    "formacao_bruta_capital_fixo_percent_pib": "Form. Bruta Capital (%PIB)",
    "matricula_ensino_secundario_percent": "Matrícula Secundário (%)",
    "comercio_percent_pib": "Comércio (%PIB)",
    "investimento_estrangeiro_direto_percent_pib": "IDE (%PIB)",
    "populacao_total": "População Total",
    "emprego_industria_percent_emprego_total": "Emprego Indústria (%)",
    "valor_agregado_industrial_percent_pib": "Valor Agregado Ind. (%PIB)",
}

# Cores para visualizações
CORES = {
    "principal": "#2E86AB",
    "secundaria": "#A23B72",
    "sucesso": "#06A77D",
    "alerta": "#F18F01",
}

# Configurações de gráficos
FIGSIZE_PADRAO = (14, 8)
DPI = 100
STYLE = "seaborn-v0_8-darkgrid"
