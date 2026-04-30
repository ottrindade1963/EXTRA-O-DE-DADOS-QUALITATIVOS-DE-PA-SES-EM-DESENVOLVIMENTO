"""Preparação de dados para Temporal Fusion Transformer (TFT)."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from prep_config import QUANT_VARS, QUAL_VARS, TARGET, SEQ_LENGTH, FORECAST_HORIZON


def padronizar_zscore(df, features=None):
    """Padroniza features com Z-score (média=0, std=1)."""
    if features is None:
        features = QUANT_VARS + QUAL_VARS
    
    df = df.copy()
    features_existentes = [f for f in features if f in df.columns]
    
    scaler = StandardScaler()
    df[features_existentes] = scaler.fit_transform(df[features_existentes])
    
    return df, scaler


def criar_time_index(df):
    """Cria índice temporal contínuo por país (necessário para TFT)."""
    df = df.copy()
    df['time_idx'] = df.groupby('country_code').cumcount()
    return df


def codificar_categoricas(df):
    """Codifica variáveis categóricas para embeddings do TFT."""
    df = df.copy()
    
    # País como código numérico
    paises = sorted(df['country_code'].unique())
    mapa_pais = {p: i for i, p in enumerate(paises)}
    df['country_id'] = df['country_code'].map(mapa_pais)
    
    # Fonte de dados (se existir)
    if 'fonte_dados' in df.columns:
        fontes = sorted(df['fonte_dados'].dropna().unique())
        mapa_fonte = {f: i for i, f in enumerate(fontes)}
        df['fonte_id'] = df['fonte_dados'].map(mapa_fonte).fillna(-1).astype(int)
    
    return df


def classificar_variaveis(df):
    """Classifica variáveis em estáticas, dinâmicas conhecidas e desconhecidas."""
    
    # Estáticas: não mudam ao longo do tempo para cada país
    estaticas_categoricas = ['country_id']
    if 'fonte_id' in df.columns:
        estaticas_categoricas.append('fonte_id')
    
    # Dinâmicas conhecidas no futuro (sabemos o ano futuro)
    dinamicas_conhecidas = ['year', 'time_idx']
    
    # Dinâmicas desconhecidas no futuro (variáveis a prever/observar)
    dinamicas_desconhecidas = [c for c in QUANT_VARS + QUAL_VARS if c in df.columns]
    
    classificacao = {
        'estaticas_categoricas': estaticas_categoricas,
        'dinamicas_conhecidas': dinamicas_conhecidas,
        'dinamicas_desconhecidas': dinamicas_desconhecidas,
        'target': TARGET,
        'group_ids': ['country_id'],
        'time_idx': 'time_idx',
        'max_encoder_length': SEQ_LENGTH,
        'max_prediction_length': FORECAST_HORIZON,
    }
    
    return classificacao


def preparar_para_tft(df, nome_dataset):
    """Pipeline completo de preparação para TFT."""
    print(f"\n  ── Preparação para TFT ({nome_dataset}) ──")
    
    # Codificar categóricas
    df = codificar_categoricas(df)
    print(f"    ✅ Variáveis categóricas codificadas")
    
    # Criar time_idx
    df = criar_time_index(df)
    print(f"    ✅ Índice temporal criado (time_idx)")
    
    # Padronizar com Z-score
    df, scaler = padronizar_zscore(df)
    print(f"    ✅ Padronização Z-score aplicada")
    
    # Classificar variáveis
    classificacao = classificar_variaveis(df)
    print(f"    ✅ Variáveis classificadas:")
    print(f"       Estáticas categóricas: {classificacao['estaticas_categoricas']}")
    print(f"       Dinâmicas conhecidas: {classificacao['dinamicas_conhecidas']}")
    print(f"       Dinâmicas desconhecidas: {len(classificacao['dinamicas_desconhecidas'])} variáveis")
    print(f"       Target: {classificacao['target']}")
    
    return df, scaler, classificacao
