"""Processamento de dados WGI baixados."""

import pandas as pd
from wgi_config import NOMES_INDICADORES


def pivotar_dados(wgi_combined):
    """Pivota dados para formato largo."""
    print(f"\n🔄 Pivotando para formato largo...")
    
    wgi_pivot = wgi_combined.pivot_table(
        index=['country_code', 'year'],
        columns='indicator',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    print(f"   {len(wgi_pivot)} linhas (país-ano)")
    
    return wgi_pivot


def converter_tipos_dados(df):
    """Converte tipos de dados."""
    print(f"\n🔧 Convertendo tipos de dados...")
    
    df['year'] = df['year'].astype(int)
    
    for col in df.columns:
        if col not in ['country_code', 'year']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"   ✅ Conversão concluída")
    
    return df


def ordenar_e_reorganizar(df):
    """Ordena e reorganiza as colunas."""
    print(f"\n📋 Reorganizando dataframe...")
    
    # Ordena por país e ano
    df = df.sort_values(['country_code', 'year']).reset_index(drop=True)
    
    # Reorganiza colunas
    wgi_cols = sorted([c for c in df.columns if c.startswith('wgi_')])
    col_order = ['country_code', 'year'] + wgi_cols
    df = df[col_order]
    
    print(f"   ✅ Dataframe reorganizado")
    
    return df


def gerar_resumo(df):
    """Gera resumo dos dados processados."""
    print(f"\n" + "="*60)
    print(f"  📊 RESUMO DOS DADOS PROCESSADOS")
    print(f"="*60)
    
    print(f"\n  Dimensões: {df.shape[0]} linhas (país-ano) × {df.shape[1]} colunas")
    print(f"  Países únicos: {df['country_code'].nunique()}")
    print(f"  Período: {df['year'].min()} a {df['year'].max()}")
    
    print(f"\n  Cobertura de dados:")
    for col in df.columns:
        if col not in ['country_code', 'year']:
            non_null = df[col].notna().sum()
            pct = (non_null / len(df)) * 100
            print(f"    {col:35s}: {non_null:6d} ({pct:5.1f}%)")
    
    return df
