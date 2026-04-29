"""Visualizações para segunda análise exploratória."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from eda2_config import (
    COLUNAS_NUMERICAS, NOMES_VARIAVEIS, CORES, FIGSIZE_PADRAO, DPI, STYLE, OUTPUT_DIR
)

plt.style.use(STYLE)


def grafico_1_heatmap_missing(df):
    """Heatmap de valores ausentes por década."""
    print("  Gerando: 1. Heatmap de valores ausentes...")
    
    df["decada"] = (df["ano"] // 10 * 10).astype(str) + "s"
    missing_por_decada = df.groupby("decada")[COLUNAS_NUMERICAS].apply(
        lambda x: x.isnull().sum() / len(x) * 100
    )
    
    fig, ax = plt.subplots(figsize=FIGSIZE_PADRAO, dpi=DPI)
    sns.heatmap(missing_por_decada.T, annot=True, fmt=".1f", cmap="RdYlGn_r", 
                cbar_kws={"label": "% Missing"}, ax=ax, vmin=0, vmax=50)
    ax.set_title("Valores Ausentes por Década (%)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Variáveis", fontsize=11)
    ax.set_xlabel("Década", fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/01_heatmap_missing.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_2_histogramas(df):
    """Histogramas de distribuição."""
    print("  Gerando: 2. Histogramas...")
    
    fig, axes = plt.subplots(2, 4, figsize=(18, 10), dpi=DPI)
    axes = axes.flatten()
    
    for idx, col in enumerate(COLUNAS_NUMERICAS):
        data = df[col].dropna()
        axes[idx].hist(data, bins=30, color=CORES["principal"], alpha=0.7, edgecolor="black")
        axes[idx].set_title(NOMES_VARIAVEIS[col], fontsize=10, fontweight="bold")
        axes[idx].set_xlabel("Valor")
        axes[idx].set_ylabel("Frequência")
        axes[idx].grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/02_histogramas.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_3_boxplots(df):
    """Boxplots para detectar outliers."""
    print("  Gerando: 3. Boxplots...")
    
    fig, axes = plt.subplots(2, 4, figsize=(18, 10), dpi=DPI)
    axes = axes.flatten()
    
    for idx, col in enumerate(COLUNAS_NUMERICAS):
        data = df[col].dropna()
        axes[idx].boxplot(data, vert=True, patch_artist=True,
                         boxprops=dict(facecolor=CORES["principal"], alpha=0.7),
                         medianprops=dict(color="red", linewidth=2))
        axes[idx].set_title(NOMES_VARIAVEIS[col], fontsize=10, fontweight="bold")
        axes[idx].set_ylabel("Valor")
        axes[idx].grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/03_boxplots.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_4_matriz_correlacao(df):
    """Matriz de correlação com heatmap."""
    print("  Gerando: 4. Matriz de correlação...")
    
    corr = df[COLUNAS_NUMERICAS].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10), dpi=DPI)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, linewidths=0.5, cbar_kws={"label": "Correlação"}, ax=ax)
    ax.set_title("Matriz de Correlação de Pearson", fontsize=14, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/04_matriz_correlacao.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_5_evolucao_temporal(df):
    """Evolução temporal (linhas)."""
    print("  Gerando: 5. Evolução temporal...")
    
    fig, ax = plt.subplots(figsize=FIGSIZE_PADRAO, dpi=DPI)
    
    for col in COLUNAS_NUMERICAS:
        media_anual = df.groupby("ano")[col].mean()
        ax.plot(media_anual.index, media_anual.values, marker="o", label=NOMES_VARIAVEIS[col], linewidth=2)
    
    ax.set_title("Evolução Temporal das Variáveis (Média Global)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("Valor Médio", fontsize=11)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/05_evolucao_temporal.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_6_top10_paises(df):
    """Top 10 países por PIB per capita."""
    print("  Gerando: 6. Top 10 países...")
    
    top10 = df.groupby("pais")["pib_per_capita_ppc"].mean().nlargest(10)
    
    fig, ax = plt.subplots(figsize=FIGSIZE_PADRAO, dpi=DPI)
    top10.plot(kind="barh", color=CORES["principal"], ax=ax, edgecolor="black")
    ax.set_title("Top 10 Países por PIB per Capita Médio (PPC)", fontsize=14, fontweight="bold")
    ax.set_xlabel("PIB per Capita (USD)", fontsize=11)
    ax.set_ylabel("País", fontsize=11)
    ax.grid(axis="x", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/06_top10_paises.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_7_scatter_pib_industrializacao(df):
    """Scatter: PIB vs Industrialização (bolhas por população)."""
    print("  Gerando: 7. Scatter PIB vs Industrialização...")
    
    df_scatter = df.groupby("pais").agg({
        "pib_per_capita_ppc": "mean",
        "valor_agregado_industrial_percent_pib": "mean",
        "populacao_total": "mean",
    }).dropna()
    
    fig, ax = plt.subplots(figsize=FIGSIZE_PADRAO, dpi=DPI)
    scatter = ax.scatter(df_scatter["pib_per_capita_ppc"], 
                        df_scatter["valor_agregado_industrial_percent_pib"],
                        s=df_scatter["populacao_total"]/1e6,  # Tamanho proporcional à população
                        alpha=0.6, color=CORES["principal"], edgecolors="black", linewidth=0.5)
    
    ax.set_title("PIB per Capita vs Valor Agregado Industrial\n(Tamanho = População)", 
                fontsize=14, fontweight="bold")
    ax.set_xlabel("PIB per Capita (USD)", fontsize=11)
    ax.set_ylabel("Valor Agregado Industrial (% PIB)", fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/07_scatter_pib_industrializacao.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_8_violin_emprego(df):
    """Violin plot: Emprego industrial por década."""
    print("  Gerando: 8. Violin plot...")
    
    df["decada"] = (df["ano"] // 10 * 10).astype(str) + "s"
    
    fig, ax = plt.subplots(figsize=FIGSIZE_PADRAO, dpi=DPI)
    sns.violinplot(data=df, x="decada", y="emprego_industria_percent_emprego_total",
                   color=CORES["principal"], ax=ax)
    ax.set_title("Distribuição do Emprego Industrial por Década", fontsize=14, fontweight="bold")
    ax.set_xlabel("Década", fontsize=11)
    ax.set_ylabel("Emprego Indústria (%)", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/08_violin_emprego.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_9_pairplot(df):
    """Pairplot de 4 variáveis principais."""
    print("  Gerando: 9. Pairplot...")
    
    cols_principais = [
        "pib_per_capita_ppc",
        "valor_agregado_industrial_percent_pib",
        "matricula_ensino_secundario_percent",
        "comercio_percent_pib",
    ]
    
    df_pair = df[cols_principais].dropna()
    
    fig = plt.figure(figsize=(14, 12), dpi=DPI)
    sns.pairplot(df_pair, diag_kind="hist", plot_kws={"alpha": 0.6, "s": 20},
                diag_kws={"bins": 20, "edgecolor": "black"})
    
    plt.suptitle("Pairplot de Variáveis Principais", fontsize=14, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/09_pairplot.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def grafico_10_heatmap_paises(df):
    """Heatmap: Perfil normalizado dos top 20 países."""
    print("  Gerando: 10. Heatmap de países...")
    
    top20 = df.groupby("pais")[COLUNAS_NUMERICAS].mean().nlargest(20, "pib_per_capita_ppc")
    
    # Normalizar (0-1)
    top20_norm = (top20 - top20.min()) / (top20.max() - top20.min())
    
    fig, ax = plt.subplots(figsize=(14, 10), dpi=DPI)
    sns.heatmap(top20_norm, annot=False, cmap="YlOrRd", cbar_kws={"label": "Valor Normalizado"},
                ax=ax, linewidths=0.5)
    ax.set_title("Perfil Normalizado dos Top 20 Países (por PIB per Capita)", 
                fontsize=14, fontweight="bold")
    ax.set_xlabel("Variáveis", fontsize=11)
    ax.set_ylabel("País", fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/10_heatmap_paises.png", dpi=DPI, bbox_inches="tight")
    plt.close()


def gerar_todos_graficos(df):
    """Gera todos os 10 gráficos."""
    print("\n" + "="*60)
    print("  📊 GERANDO VISUALIZAÇÕES")
    print("="*60 + "\n")
    
    grafico_1_heatmap_missing(df)
    grafico_2_histogramas(df)
    grafico_3_boxplots(df)
    grafico_4_matriz_correlacao(df)
    grafico_5_evolucao_temporal(df)
    grafico_6_top10_paises(df)
    grafico_7_scatter_pib_industrializacao(df)
    grafico_8_violin_emprego(df)
    grafico_9_pairplot(df)
    grafico_10_heatmap_paises(df)
    
    print(f"\n  ✅ Todos os gráficos salvos em: {OUTPUT_DIR}/")
