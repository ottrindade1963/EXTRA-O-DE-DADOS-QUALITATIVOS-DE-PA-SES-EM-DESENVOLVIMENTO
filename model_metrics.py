"""Métricas de avaliação comuns a todos os modelos."""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    mean_absolute_percentage_error
)


def calcular_metricas(y_real, y_pred, nome_modelo=''):
    """Calcula todas as métricas de avaliação."""
    y_real = np.array(y_real).flatten()
    y_pred = np.array(y_pred).flatten()
    
    # Remover NaN
    mask = ~(np.isnan(y_real) | np.isnan(y_pred))
    y_real, y_pred = y_real[mask], y_pred[mask]
    
    mae = mean_absolute_error(y_real, y_pred)
    rmse = np.sqrt(mean_squared_error(y_real, y_pred))
    r2 = r2_score(y_real, y_pred)
    
    # MAPE (evitar divisão por zero)
    mask_nz = y_real != 0
    if mask_nz.sum() > 0:
        mape = np.mean(np.abs((y_real[mask_nz] - y_pred[mask_nz]) / y_real[mask_nz])) * 100
    else:
        mape = np.nan
    
    # SMAPE (simétrico)
    denom = (np.abs(y_real) + np.abs(y_pred)) / 2
    mask_d = denom != 0
    if mask_d.sum() > 0:
        smape = np.mean(np.abs(y_real[mask_d] - y_pred[mask_d]) / denom[mask_d]) * 100
    else:
        smape = np.nan
    
    metricas = {
        'modelo': nome_modelo,
        'MAE': round(mae, 4),
        'RMSE': round(rmse, 4),
        'R2': round(r2, 4),
        'MAPE (%)': round(mape, 2),
        'SMAPE (%)': round(smape, 2),
        'N_amostras': len(y_real),
    }
    
    return metricas


def tabela_comparativa(lista_metricas):
    """Cria tabela comparativa de todos os modelos."""
    df = pd.DataFrame(lista_metricas)
    df = df.sort_values('RMSE').reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = 'Rank'
    return df


def imprimir_metricas(metricas):
    """Imprime métricas formatadas."""
    print(f"    {'─' * 45}")
    print(f"    │ {'Métrica':<12} │ {'Valor':>12} │")
    print(f"    {'─' * 45}")
    for k, v in metricas.items():
        if k != 'modelo' and k != 'N_amostras':
            print(f"    │ {k:<12} │ {v:>12} │")
    print(f"    {'─' * 45}")
