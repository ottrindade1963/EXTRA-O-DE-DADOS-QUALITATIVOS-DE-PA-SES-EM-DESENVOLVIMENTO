"""Preparação de dados para SARIMAX."""

import pandas as pd
import numpy as np
from scipy import stats as sp_stats
from prep_config import ALL_FEATURES, TARGET, QUAL_VARS


def teste_estacionariedade(serie, nome=''):
    """Aplica teste ADF (Augmented Dickey-Fuller) a uma série."""
    from statsmodels.tsa.stattools import adfuller
    
    serie_limpa = serie.dropna()
    if len(serie_limpa) < 10:
        return {'variavel': nome, 'adf_stat': np.nan, 'p_valor': np.nan,
                'estacionaria': False, 'diferenciacoes': 0}
    
    resultado = adfuller(serie_limpa, autolag='AIC')
    estacionaria = resultado[1] < 0.05
    
    return {
        'variavel': nome,
        'adf_stat': resultado[0],
        'p_valor': resultado[1],
        'estacionaria': estacionaria,
        'diferenciacoes': 0 if estacionaria else 1
    }


def diferenciar_serie(df, col, ordem=1):
    """Aplica diferenciação de ordem n a uma coluna por país."""
    df = df.copy()
    nome_diff = f'{col}_d{ordem}'
    df[nome_diff] = df.groupby('country_code')[col].diff(ordem)
    return df, nome_diff


def garantir_continuidade(df):
    """Garante que cada país tem série temporal contínua (sem gaps de anos)."""
    resultado = []
    for pais, grupo in df.groupby('country_code'):
        grupo = grupo.sort_values('year')
        ano_min, ano_max = grupo['year'].min(), grupo['year'].max()
        anos_completos = set(range(ano_min, ano_max + 1))
        anos_existentes = set(grupo['year'])
        gaps = anos_completos - anos_existentes
        
        if gaps:
            # Criar linhas para anos faltantes e interpolar
            idx_completo = pd.DataFrame({'year': sorted(anos_completos)})
            idx_completo['country_code'] = pais
            grupo = idx_completo.merge(grupo, on=['country_code', 'year'], how='left')
            cols_num = grupo.select_dtypes(include=[np.number]).columns
            cols_num = [c for c in cols_num if c != 'year']
            grupo[cols_num] = grupo[cols_num].interpolate(method='linear')
        
        resultado.append(grupo)
    
    return pd.concat(resultado).sort_values(['country_code', 'year']).reset_index(drop=True)


def selecionar_exogenas(df):
    """Seleciona variáveis exógenas para o SARIMAX."""
    exogenas = [c for c in ALL_FEATURES if c in df.columns and c != TARGET]
    return exogenas


def preparar_para_sarimax(df, nome_dataset):
    """Pipeline completo de preparação para SARIMAX."""
    print(f"\n  ── Preparação para SARIMAX ({nome_dataset}) ──")
    
    # Garantir continuidade temporal
    df = garantir_continuidade(df)
    print(f"    ✅ Continuidade temporal garantida")
    
    # Testes de estacionariedade (amostra de 5 países)
    paises_amostra = df['country_code'].unique()[:5]
    print(f"    ── Testes ADF (amostra: {list(paises_amostra)}):")
    
    resultados_adf = []
    for pais in paises_amostra:
        serie = df[df['country_code'] == pais][TARGET]
        r = teste_estacionariedade(serie, f'{TARGET}_{pais}')
        resultados_adf.append(r)
        status = '✅ Estacionária' if r['estacionaria'] else '⚠️ Não-estacionária → d=1'
        print(f"       {pais}: ADF={r['adf_stat']:.3f}, p={r['p_valor']:.4f} → {status}")
    
    # Diferenciar se necessário
    nao_estac = [r for r in resultados_adf if not r['estacionaria']]
    if len(nao_estac) > len(resultados_adf) / 2:
        df, col_diff = diferenciar_serie(df, TARGET, ordem=1)
        print(f"    ✅ Diferenciação aplicada: {col_diff}")
    
    # Selecionar exógenas
    exogenas = selecionar_exogenas(df)
    print(f"    ✅ Variáveis exógenas: {len(exogenas)}")
    
    return df, exogenas
