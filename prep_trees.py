"""Preparação de dados para Random Forest e XGBoost."""

import pandas as pd
import numpy as np
from prep_config import ALL_FEATURES, TARGET, LAGS, ROLLING_WINDOWS


def criar_lags(df, features=None, lags=None):
    """Cria variáveis defasadas (lags) por país."""
    if features is None:
        features = ALL_FEATURES
    if lags is None:
        lags = LAGS
    
    df = df.copy()
    features_existentes = [f for f in features if f in df.columns]
    
    for col in features_existentes:
        for lag in lags:
            df[f'{col}_lag{lag}'] = df.groupby('country_code')[col].shift(lag)
    return df


def criar_medias_moveis(df, features=None, windows=None):
    """Cria médias móveis por país."""
    if features is None:
        features = ALL_FEATURES
    if windows is None:
        windows = ROLLING_WINDOWS
    
    df = df.copy()
    features_existentes = [f for f in features if f in df.columns]
    
    for col in features_existentes:
        for w in windows:
            df[f'{col}_ma{w}'] = df.groupby('country_code')[col].transform(
                lambda s: s.rolling(window=w, min_periods=1).mean()
            )
    return df


def criar_diferencas(df, features=None):
    """Cria diferenças de primeira ordem (variação anual) por país."""
    if features is None:
        features = ALL_FEATURES
    
    df = df.copy()
    features_existentes = [f for f in features if f in df.columns]
    
    for col in features_existentes:
        df[f'{col}_diff1'] = df.groupby('country_code')[col].diff(1)
    return df


def codificar_pais(df, metodo='label'):
    """Codifica country_code como variável numérica."""
    df = df.copy()
    if metodo == 'label':
        codigos = {pais: i for i, pais in enumerate(sorted(df['country_code'].unique()))}
        df['country_id'] = df['country_code'].map(codigos)
    return df


def preparar_para_trees(df, nome_dataset):
    """Pipeline completo de preparação para Random Forest / XGBoost."""
    print(f"\n  ── Preparação para RF/XGBoost ({nome_dataset}) ──")
    
    # Engenharia de features
    df = criar_lags(df)
    print(f"    ✅ Lags criados: {LAGS}")
    
    df = criar_medias_moveis(df)
    print(f"    ✅ Médias móveis: janelas {ROLLING_WINDOWS}")
    
    df = criar_diferencas(df)
    print(f"    ✅ Diferenças de 1ª ordem criadas")
    
    df = codificar_pais(df)
    print(f"    ✅ País codificado (label encoding)")
    
    # Remover linhas com NaN gerados pelos lags
    antes = len(df)
    df = df.dropna(subset=[f'{TARGET}_lag1']).reset_index(drop=True)
    print(f"    ✅ Removidas {antes - len(df)} linhas (lags iniciais)")
    
    return df
