"""Carregamento e análise descritiva de dados limpos."""

import pandas as pd
import numpy as np
from scipy import stats
from eda2_config import DATA_PATH, COLUNAS_NUMERICAS, NOMES_VARIAVEIS


def carregar_dados(path):
    """Carrega o CSV limpo."""
    df = pd.read_csv(path)
    print(f"✅ Dados limpos carregados: {df.shape[0]:,} linhas x {df.shape[1]} colunas")
    print(f"   Período: {df['ano'].min()}-{df['ano'].max()}")
    print(f"   Países: {df['pais'].nunique()}")
    return df


def resumo_geral(df):
    """Gera resumo geral dos dados."""
    print("\n" + "="*60)
    print("  📊 RESUMO GERAL DOS DADOS")
    print("="*60)
    
    print(f"\n  Total de registros: {len(df):,}")
    print(f"  Total de colunas: {len(df.columns)}")
    print(f"  Período: {df['ano'].min()}-{df['ano'].max()}")
    print(f"  Países: {df['pais'].nunique()}")
    print(f"  Anos: {df['ano'].nunique()}")
    
    print(f"\n  Valores ausentes (missing):")
    for col in COLUNAS_NUMERICAS:
        miss = df[col].isnull().sum()
        pct = miss / len(df) * 100
        print(f"    {NOMES_VARIAVEIS[col]}: {miss} ({pct:.1f}%)")


def estatisticas_descritivas(df):
    """Calcula estatísticas descritivas completas."""
    print("\n" + "="*60)
    print("  📈 ESTATÍSTICAS DESCRITIVAS COMPLETAS")
    print("="*60)
    
    stats_list = []
    
    for col in COLUNAS_NUMERICAS:
        data = df[col].dropna()
        
        stats_list.append({
            "Variável": NOMES_VARIAVEIS[col],
            "N": len(data),
            "Média": data.mean(),
            "Mediana": data.median(),
            "Moda": data.mode().values[0] if len(data.mode()) > 0 else np.nan,
            "Desvio-Padrão": data.std(),
            "Variância": data.var(),
            "Mínimo": data.min(),
            "Q1": data.quantile(0.25),
            "Q3": data.quantile(0.75),
            "Máximo": data.max(),
            "IQR": data.quantile(0.75) - data.quantile(0.25),
            "Amplitude": data.max() - data.min(),
            "Assimetria": stats.skew(data),
            "Curtose": stats.kurtosis(data),
            "CV(%)": (data.std() / data.mean() * 100) if data.mean() != 0 else 0,
        })
    
    df_stats = pd.DataFrame(stats_list)
    print("\n", df_stats.to_string(index=False))
    
    return df_stats


def intervalos_confianca(df):
    """Calcula intervalos de confiança 95%."""
    print("\n" + "="*60)
    print("  🎯 INTERVALOS DE CONFIANÇA (95%)")
    print("="*60)
    
    ic_list = []
    
    for col in COLUNAS_NUMERICAS:
        data = df[col].dropna()
        n = len(data)
        media = data.mean()
        erro_padrao = data.std() / np.sqrt(n)
        margem = 1.96 * erro_padrao  # 95% confiança
        
        ic_list.append({
            "Variável": NOMES_VARIAVEIS[col],
            "N": n,
            "Média": media,
            "Erro Padrão": erro_padrao,
            "IC Inferior": media - margem,
            "IC Superior": media + margem,
            "Margem": margem,
        })
    
    df_ic = pd.DataFrame(ic_list)
    print("\n", df_ic.to_string(index=False))
    
    return df_ic


def testes_normalidade(df):
    """Testes de normalidade (Shapiro-Wilk e D'Agostino-Pearson)."""
    print("\n" + "="*60)
    print("  🔬 TESTES DE NORMALIDADE")
    print("="*60)
    
    testes_list = []
    
    for col in COLUNAS_NUMERICAS:
        data = df[col].dropna()
        
        # Shapiro-Wilk
        if len(data) <= 5000:
            stat_sw, p_sw = stats.shapiro(data)
            conclusao_sw = "Normal" if p_sw > 0.05 else "Não-Normal"
        else:
            stat_sw, p_sw = np.nan, np.nan
            conclusao_sw = "N/A (n>5000)"
        
        # D'Agostino-Pearson
        stat_dp, p_dp = stats.normaltest(data)
        conclusao_dp = "Normal" if p_dp > 0.05 else "Não-Normal"
        
        testes_list.append({
            "Variável": NOMES_VARIAVEIS[col],
            "Shapiro-Wilk (p)": f"{p_sw:.4f}" if not np.isnan(p_sw) else "N/A",
            "Conclusão SW": conclusao_sw,
            "D'Agostino (p)": f"{p_dp:.4f}",
            "Conclusão DP": conclusao_dp,
        })
    
    df_testes = pd.DataFrame(testes_list)
    print("\n", df_testes.to_string(index=False))
    
    return df_testes


def estatisticas_por_decada(df):
    """Estatísticas por década para cada variável."""
    print("\n" + "="*60)
    print("  📅 ESTATÍSTICAS POR DÉCADA")
    print("="*60)
    
    df["decada"] = (df["ano"] // 10 * 10).astype(str) + "s"
    
    for col in COLUNAS_NUMERICAS:
        print(f"\n  ▸ {NOMES_VARIAVEIS[col]}:")
        
        stats_decada = df.groupby("decada")[col].agg([
            ("N", "count"),
            ("Média", "mean"),
            ("Mediana", "median"),
            ("Desvio-Padrão", "std"),
            ("Mín", "min"),
            ("Máx", "max"),
        ]).round(2)
        
        print(stats_decada.to_string())
    
    return df


def matriz_correlacao(df):
    """Calcula matriz de correlação."""
    print("\n" + "="*60)
    print("  🔗 MATRIZ DE CORRELAÇÃO")
    print("="*60)
    
    corr_matrix = df[COLUNAS_NUMERICAS].corr()
    print("\n", corr_matrix.round(3).to_string())
    
    return corr_matrix
