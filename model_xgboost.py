"""Treino e avaliação do XGBoost."""

import pandas as pd
import numpy as np
from model_config import XGB_CONFIG, TARGET
from model_metrics import calcular_metricas, imprimir_metricas


def treinar_xgboost(treino_path, teste_path):
    """Treina e avalia XGBoost."""
    from xgboost import XGBRegressor
    
    print("\n  ── XGBoost ──")
    
    # Carregar dados
    treino = pd.read_csv(treino_path)
    teste = pd.read_csv(teste_path)
    
    # Separar features e target (excluir texto e target)
    cols_excluir = [TARGET, 'country_code', 'year']
    features = [c for c in treino.columns if c not in cols_excluir
                and treino[c].dtype in ['float64', 'float32', 'int64', 'int32']]
    
    X_treino = treino[features].values
    y_treino = treino[TARGET].values
    X_teste = teste[features].values
    y_teste = teste[TARGET].values
    
    print(f"    Treino: {X_treino.shape} | Teste: {X_teste.shape}")
    
    # Treinar modelo
    modelo = XGBRegressor(**XGB_CONFIG, verbosity=0)
    modelo.fit(
        X_treino, y_treino,
        eval_set=[(X_teste, y_teste)],
        verbose=False
    )
    print(f"    ✅ Modelo treinado ({XGB_CONFIG['n_estimators']} boosters)")
    
    # Prever
    y_pred = modelo.predict(X_teste)
    
    # Métricas
    metricas = calcular_metricas(y_teste, y_pred, 'XGBoost')
    imprimir_metricas(metricas)
    
    # Feature importance (top 10)
    importancias = pd.Series(modelo.feature_importances_, index=features)
    top10 = importancias.nlargest(10)
    print(f"\n    Top 10 Features:")
    for feat, imp in top10.items():
        print(f"      {feat[:40]:<40s} {imp:.4f}")
    
    return modelo, metricas, y_pred, y_teste, top10
