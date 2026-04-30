"""Transformações base comuns a todos os modelos."""

import pandas as pd
import numpy as np
from prep_config import ALL_FEATURES, LOG_TRANSFORM_VARS, TARGET


def carregar_dataset(path):
    """Carrega CSV e faz limpeza básica."""
    df = pd.read_csv(path)
    df = df.sort_values(['country_code', 'year']).reset_index(drop=True)
    return df


def remover_missing_critico(df, limiar=0.5):
    """Remove linhas com mais de 'limiar' % de missing nas features."""
    cols = [c for c in ALL_FEATURES if c in df.columns]
    pct_missing = df[cols].isnull().mean(axis=1)
    df_limpo = df[pct_missing <= limiar].copy()
    removidas = len(df) - len(df_limpo)
    if removidas > 0:
        print(f"    Removidas {removidas} linhas com >{limiar*100:.0f}% missing")
    return df_limpo


def imputar_missing(df):
    """Imputa valores ausentes por interpolação temporal dentro de cada país."""
    cols = [c for c in ALL_FEATURES if c in df.columns]
    df = df.copy()
    for col in cols:
        df[col] = df.groupby('country_code')[col].transform(
            lambda s: s.interpolate(method='linear', limit_direction='both')
        )
    # Preencher restantes com mediana global
    for col in cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    return df


def transformar_log(df):
    """Aplica log1p a variáveis com assimetria forte."""
    df = df.copy()
    for col in LOG_TRANSFORM_VARS:
        if col in df.columns:
            # Para IDE que pode ser negativo: shift para positivo
            if df[col].min() < 0:
                shift = abs(df[col].min()) + 1
                df[f'{col}_log'] = np.log1p(df[col] + shift)
            else:
                df[f'{col}_log'] = np.log1p(df[col])
    return df


def split_temporal(df, train_ratio=0.8):
    """Split treino/teste respeitando a ordem temporal por país."""
    treino_list, teste_list = [], []
    for pais, grupo in df.groupby('country_code'):
        grupo = grupo.sort_values('year')
        n = len(grupo)
        corte = int(n * train_ratio)
        treino_list.append(grupo.iloc[:corte])
        teste_list.append(grupo.iloc[corte:])
    treino = pd.concat(treino_list).reset_index(drop=True)
    teste = pd.concat(teste_list).reset_index(drop=True)
    return treino, teste


def resumo_preparacao(df, nome):
    """Imprime resumo do dataset preparado."""
    cols = [c for c in ALL_FEATURES if c in df.columns]
    missing = df[cols].isnull().sum().sum()
    print(f"    {nome}: {df.shape[0]:,} linhas × {df.shape[1]} colunas | Missing: {missing}")
