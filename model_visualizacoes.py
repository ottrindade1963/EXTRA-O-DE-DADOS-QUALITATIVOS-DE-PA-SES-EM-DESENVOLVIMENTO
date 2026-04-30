"""Visualizações de avaliação dos modelos."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def grafico_real_vs_previsto(resultados, pasta_saida):
    """Gráfico scatter real vs previsto para cada modelo."""
    n_modelos = len(resultados)
    fig, axes = plt.subplots(1, n_modelos, figsize=(5 * n_modelos, 5))
    if n_modelos == 1:
        axes = [axes]
    
    for ax, (nome, res) in zip(axes, resultados.items()):
        y_real, y_pred = res['y_real'], res['y_pred']
        ax.scatter(y_real, y_pred, alpha=0.3, s=10, color='steelblue')
        
        # Linha de referência
        lim_min = min(y_real.min(), y_pred.min())
        lim_max = max(y_real.max(), y_pred.max())
        ax.plot([lim_min, lim_max], [lim_min, lim_max], 'r--', lw=1.5)
        
        ax.set_xlabel('Real')
        ax.set_ylabel('Previsto')
        ax.set_title(f'{nome}\nR²={res["metricas"]["R2"]:.3f}')
    
    plt.tight_layout()
    path = os.path.join(pasta_saida, '01_real_vs_previsto.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


def grafico_barras_metricas(tabela_comp, pasta_saida):
    """Gráfico de barras comparando métricas entre modelos."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    metricas_plot = ['MAE', 'RMSE', 'R2', 'MAPE (%)']
    cores = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']
    
    for ax, metrica in zip(axes.flatten(), metricas_plot):
        valores = tabela_comp[metrica].values
        nomes = tabela_comp['modelo'].values
        barras = ax.bar(nomes, valores, color=cores[:len(nomes)], alpha=0.8)
        ax.set_title(metrica, fontweight='bold')
        ax.set_xticklabels(nomes, rotation=30, ha='right', fontsize=9)
        
        # Valores nas barras
        for bar, val in zip(barras, valores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    
    plt.suptitle('Comparação de Métricas entre Modelos', fontweight='bold', fontsize=13)
    plt.tight_layout()
    path = os.path.join(pasta_saida, '02_comparacao_metricas.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


def grafico_residuos(resultados, pasta_saida):
    """Gráfico de distribuição dos resíduos por modelo."""
    n_modelos = len(resultados)
    fig, axes = plt.subplots(1, n_modelos, figsize=(5 * n_modelos, 4))
    if n_modelos == 1:
        axes = [axes]
    
    for ax, (nome, res) in zip(axes, resultados.items()):
        residuos = res['y_real'] - res['y_pred']
        ax.hist(residuos, bins=30, alpha=0.7, color='steelblue', edgecolor='white')
        ax.axvline(0, color='red', linestyle='--', lw=1.5)
        ax.set_xlabel('Resíduo (Real - Previsto)')
        ax.set_ylabel('Frequência')
        ax.set_title(f'{nome}\nμ={residuos.mean():.3f}, σ={residuos.std():.3f}')
    
    plt.tight_layout()
    path = os.path.join(pasta_saida, '03_distribuicao_residuos.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


def grafico_ranking(tabela_comp, pasta_saida):
    """Gráfico radar com ranking dos modelos."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Normalizar métricas para [0, 1] (R2 já está, inverter MAE/RMSE/MAPE)
    df = tabela_comp.copy()
    df['MAE_norm'] = 1 - (df['MAE'] - df['MAE'].min()) / (df['MAE'].max() - df['MAE'].min() + 1e-10)
    df['RMSE_norm'] = 1 - (df['RMSE'] - df['RMSE'].min()) / (df['RMSE'].max() - df['RMSE'].min() + 1e-10)
    df['R2_norm'] = (df['R2'] - df['R2'].min()) / (df['R2'].max() - df['R2'].min() + 1e-10)
    df['MAPE_norm'] = 1 - (df['MAPE (%)'] - df['MAPE (%)'].min()) / (df['MAPE (%)'].max() - df['MAPE (%)'].min() + 1e-10)
    
    df['Score'] = (df['MAE_norm'] + df['RMSE_norm'] + df['R2_norm'] + df['MAPE_norm']) / 4
    df = df.sort_values('Score', ascending=False)
    
    cores = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
    barras = ax.barh(df['modelo'], df['Score'], color=cores[:len(df)], alpha=0.8)
    
    for bar, score in zip(barras, df['Score']):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{score:.3f}', va='center', fontsize=10)
    
    ax.set_xlabel('Score Normalizado (maior = melhor)')
    ax.set_title('Ranking Geral dos Modelos', fontweight='bold')
    ax.set_xlim(0, 1.15)
    
    plt.tight_layout()
    path = os.path.join(pasta_saida, '04_ranking_modelos.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


def gerar_visualizacoes(resultados, tabela_comp, pasta_saida):
    """Gera todas as visualizações de avaliação."""
    os.makedirs(pasta_saida, exist_ok=True)
    
    graficos = []
    graficos.append(grafico_real_vs_previsto(resultados, pasta_saida))
    graficos.append(grafico_barras_metricas(tabela_comp, pasta_saida))
    graficos.append(grafico_residuos(resultados, pasta_saida))
    graficos.append(grafico_ranking(tabela_comp, pasta_saida))
    
    print(f"    ✅ {len(graficos)} gráficos gerados em {pasta_saida}/")
    return graficos
