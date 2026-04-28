"""Carregamento e limpeza dos dados."""

import pandas as pd
from eda_config import DATA_PATH, COLUNAS_NUMERICAS


def carregar_dados():
    """Carrega o CSV e retorna o DataFrame."""
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
    return df


def resumo_geral(df):
    """Imprime resumo geral do dataset."""
    print(f"\n📋 RESUMO GERAL")
    print(f"  Período: {df['ano'].min()} – {df['ano'].max()}")
    print(f"  Países: {df['pais'].nunique()}")
    print(f"  Registros: {len(df)}")

    print(f"\n📊 VALORES AUSENTES (%):")
    missing = (df[COLUNAS_NUMERICAS].isnull().mean() * 100).round(1)
    print(missing.to_string())

    print(f"\n📈 ESTATÍSTICAS DESCRITIVAS:")
    display(df[COLUNAS_NUMERICAS].describe().round(2))
    return missing
