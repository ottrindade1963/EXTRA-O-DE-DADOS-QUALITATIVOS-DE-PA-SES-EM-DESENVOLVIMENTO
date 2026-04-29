"""Download dos ficheiros WGI (Banco Mundial) e ICRG (QoG)."""

import os
import requests
import pandas as pd
from wgi_config import WGI_URL, QOG_URL, TIMEOUT_WGI, TIMEOUT_QOG


def baixar_wgi():
    """Baixa o ficheiro Excel do WGI do Banco Mundial."""
    print("📥 Baixando Worldwide Governance Indicators (WGI)...")
    
    response = requests.get(WGI_URL, timeout=TIMEOUT_WGI)
    response.raise_for_status()
    
    with open("wgi_raw.xlsx", "wb") as f:
        f.write(response.content)
    
    wgi_raw = pd.ExcelFile("wgi_raw.xlsx")
    
    print(f"   ✅ WGI baixado com sucesso")
    print(f"   Abas disponíveis: {wgi_raw.sheet_names}")
    
    return wgi_raw


def baixar_qog():
    """Baixa o dataset QoG Standard Time-Series (contém ICRG)."""
    print("\n📥 Baixando ICRG via QoG Standard Dataset...")
    
    response = requests.get(QOG_URL, timeout=TIMEOUT_QOG)
    response.raise_for_status()
    
    # Salva localmente para evitar re-download
    with open("qog_std_ts.csv", "wb") as f:
        f.write(response.content)
    
    qog_df = pd.read_csv("qog_std_ts.csv", low_memory=False)
    
    print(f"   ✅ QoG baixado com sucesso")
    print(f"   Dimensões: {qog_df.shape}")
    
    return qog_df
