"""Exportação de dados qualitativos processados."""

import pandas as pd
from wgi_config import CSV_OUTPUT, XLSX_OUTPUT, OUTPUT_DIR


def exportar_dados(df):
    """Exporta dados em CSV e XLSX."""
    print("\n" + "="*60)
    print("  💾 EXPORTANDO DADOS")
    print("="*60 + "\n")
    
    # CSV
    df.to_csv(CSV_OUTPUT, index=False, encoding="utf-8-sig")
    print(f"  ✅ {CSV_OUTPUT}")
    
    # XLSX
    df.to_excel(XLSX_OUTPUT, index=False)
    print(f"  ✅ {XLSX_OUTPUT}")
    
    # Resumo
    print(f"\n  Painel final: {df.shape[0]} linhas, {df.shape[1]} colunas")
    print(f"  Países: {df['country_code'].nunique()}")
    print(f"  Período: {df['year'].min()} - {df['year'].max()}")
    print(f"  📁 Ficheiros salvos em: {OUTPUT_DIR}/")
    
    return True
