"""
Módulo de Configuração
Contém todas as configurações e constantes do projeto
"""

import os
from typing import Dict

# Configurações de período
DEFAULT_START_YEAR = 2003
DEFAULT_END_YEAR = 2023

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Configurações de API
API_BASE_URL = "http://api.worldbank.org/v2"
API_TIMEOUT = 30
API_RETRY_ATTEMPTS = 2
API_DELAY_BETWEEN_REQUESTS = 0.5  # segundos

# Configurações de logging
LOG_FILE = os.path.join(LOGS_DIR, "worldbank_extraction.log")
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Indicadores do Banco Mundial
INDICATORS: Dict[str, str] = {
    # Indicadores básicos e confiáveis
    "SP.POP.TOTL": "Populacao_Total",
    "NY.GDP.MKTP.KD.ZG": "Crescimento_PIB",
    "FP.CPI.TOTL.ZG": "Inflacao",
    "SL.UEM.TOTL.ZS": "Desemprego",
    "SP.DYN.LE00.IN": "Expectativa_de_Vida",
    
    # Educação
    "SE.SCH.LIFE": "Anos_Esperados_Escolaridade",
    "SE.XPD.TOTL.GD.ZS": "Gastos_Educacao_PIB",
    
    # Infraestrutura
    "EG.ELC.ACCS.ZS": "Acesso_Eletricidade",
    "IT.NET.BBND.P2": "Assinaturas_Banda_Larga",
    
    # Desenvolvimento Industrial
    "NV.IND.TOTL.ZS": "Valor_Agregado_Industrial_PIB",
    "NV.IND.MANF.ZS": "Valor_Agregado_Manufatura_PIB",
    "NE.GDI.FTOT.ZS": "Formacao_Bruta_Capital_Fixo",
    
    # Comércio
    "NE.EXP.GNFS.ZS": "Exportacoes_Bens_Servicos_PIB",
    "NE.IMP.GNFS.ZS": "Importacoes_Bens_Servicos_PIB",
    
    # Governança
    "CC.EST": "Controle_Corrupcao",
    "GE.EST": "Eficacia_Governamental",
    "RL.EST": "Estado_de_Direito",
    
    # Finanças
    "GC.TAX.TOTL.GD.ZS": "Receita_Impostos_PIB",
    
    # Inovação
    "IP.PAT.RESD": "Patentes_Residentes",
    "GB.XPD.RSDV.GD.ZS": "Gastos_PD_PIB",
    
    # Variáveis adicionais
    "NY.GDP.MKTP.CD": "PIB_USD_correntes",
    "NY.GDP.MKTP.PP.CD": "PIB_USD_PPP",
    "NV.IND.MANF.CD": "Valor_Agregado_Manufatura_USD",
    "NE.CON.PETC.CD": "Consumo_Final_Familias_USD",
    "NE.CON.GOVT.CD": "Gastos_Governo_USD",
    "NE.EXP.GNFS.CD": "Exportacoes_Bens_Servicos_USD",
    "NE.IMP.GNFS.CD": "Importacoes_Bens_Servicos_USD",
    "HD.HCI.OVRL": "Indice_Capital_Humano",
    "SP.POP.GROW": "Crescimento_Populacional",
    "SP.URB.TOTL.IN.ZS": "Urbanizacao_Porcentagem",
    "IQ.STL.REGQ": "Qualidade_Regulatoria",
    "IC.BUS.DFRN.XQ": "Facilidade_Negocios",
    "BX.KLT.DINV.CD.WD": "Fluxos_IDE_Entrada_Liquida"
}

# Países a excluir (agregados e regiões)
EXCLUDED_INCOME_LEVELS = ['HIC']  # High Income Countries
EXCLUDED_REGIONS = ['NA']  # Not Applicable
EXCLUDED_COUNTRY_CODES = [
    'INX', 'WLD', 'EUU', 'OED', 'HPC', 'LDC', 
    'LMY', 'UMC', 'LIC', 'MIC'
]

# Lista de fallback de países em desenvolvimento
FALLBACK_COUNTRIES = [
    'ARG', 'BRA', 'CHL', 'COL', 'MEX', 'PER', 'URY',  # América Latina
    'CHN', 'IND', 'IDN', 'THA', 'MYS', 'PHL', 'VNM',  # Ásia
    'ZAF', 'NGA', 'KEN', 'GHA', 'ETH', 'EGY', 'MAR',  # África
    'TUR', 'RUS', 'POL', 'HUN', 'CZE', 'BGR', 'ROU'   # Europa Oriental
]
