"""Treino e avaliação do SARIMAX."""

import pandas as pd
import numpy as np
import warnings
from model_config import SARIMAX_CONFIG, TARGET
from model_metrics import calcular_metricas, imprimir_metricas

warnings.filterwarnings('ignore')


def treinar_sarimax_pais(treino_pais, teste_pais, exogenas):
    """Treina SARIMAX para um único país."""
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    
    y_treino = treino_pais[TARGET].values
    
    # Limitar exógenas (máx 3 para estabilidade)
    exog_disp = [c for c in exogenas if c in treino_pais.columns
                 and treino_pais[c].dtype in ['float64', 'float32', 'int64']]
    exog_disp = exog_disp[:3]  # Limitar para evitar overfitting
    
    X_treino = treino_pais[exog_disp].values if exog_disp else None
    X_teste = teste_pais[exog_disp].values if exog_disp else None
    
    try:
        modelo = SARIMAX(
            y_treino,
            exog=X_treino,
            order=(1, 1, 1),
            seasonal_order=(0, 0, 0, 0),
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        resultado = modelo.fit(disp=False, maxiter=200)
        
        # Prever
        n_teste = len(teste_pais)
        previsoes = resultado.forecast(steps=n_teste, exog=X_teste)
        
        return previsoes, True
    except Exception:
        return np.full(len(teste_pais), np.nan), False


def treinar_sarimax(treino_path, teste_path, exogenas_path):
    """Treina e avalia SARIMAX para múltiplos países."""
    print("\n  ── SARIMAX ──")
    
    # Carregar dados
    treino = pd.read_csv(treino_path)
    teste = pd.read_csv(teste_path)
    exogenas = pd.read_csv(exogenas_path).iloc[:, 0].tolist()
    
    print(f"    Treino: {treino.shape} | Teste: {teste.shape}")
    print(f"    Exógenas: {len(exogenas)} variáveis")
    
    # Treinar por país (limitar para performance)
    paises = sorted(treino['country_code'].unique())
    max_paises = SARIMAX_CONFIG['max_paises']
    paises_treinar = paises[:max_paises]
    
    print(f"    Treinando para {len(paises_treinar)} países (de {len(paises)} total)...")
    
    y_real_total, y_pred_total = [], []
    sucessos, falhas = 0, 0
    
    for pais in paises_treinar:
        treino_p = treino[treino['country_code'] == pais].sort_values('year')
        teste_p = teste[teste['country_code'] == pais].sort_values('year')
        
        if len(treino_p) < 10 or len(teste_p) < 1:
            continue
        
        previsoes, sucesso = treinar_sarimax_pais(treino_p, teste_p, exogenas)
        
        if sucesso:
            y_real_total.extend(teste_p[TARGET].values)
            y_pred_total.extend(previsoes)
            sucessos += 1
        else:
            falhas += 1
    
    print(f"    ✅ Concluído: {sucessos} países OK, {falhas} falhas")
    
    # Métricas agregadas
    y_real_total = np.array(y_real_total)
    y_pred_total = np.array(y_pred_total)
    
    # Remover NaN
    mask = ~(np.isnan(y_real_total) | np.isnan(y_pred_total))
    y_real_total = y_real_total[mask]
    y_pred_total = y_pred_total[mask]
    
    metricas = calcular_metricas(y_real_total, y_pred_total, 'SARIMAX')
    imprimir_metricas(metricas)
    
    return None, metricas, y_pred_total, y_real_total, {'sucessos': sucessos, 'falhas': falhas}
