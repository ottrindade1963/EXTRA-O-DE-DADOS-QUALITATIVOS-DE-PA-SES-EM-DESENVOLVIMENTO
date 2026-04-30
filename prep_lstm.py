"""Preparação de dados para LSTM (Long Short-Term Memory)."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from prep_config import ALL_FEATURES, TARGET, SEQ_LENGTH, FORECAST_HORIZON


def normalizar_minmax(df, features=None):
    """Normaliza features para [0, 1] usando Min-Max Scaling."""
    if features is None:
        features = ALL_FEATURES
    
    df = df.copy()
    features_existentes = [f for f in features if f in df.columns]
    
    scaler = MinMaxScaler()
    df[features_existentes] = scaler.fit_transform(df[features_existentes])
    
    return df, scaler


def criar_sequencias(df, seq_length=None, target=None):
    """Cria sequências 3D (amostras, passos_tempo, features) por país."""
    if seq_length is None:
        seq_length = SEQ_LENGTH
    if target is None:
        target = TARGET
    
    features = [c for c in ALL_FEATURES if c in df.columns]
    
    X_list, y_list, info_list = [], [], []
    
    for pais, grupo in df.groupby('country_code'):
        grupo = grupo.sort_values('year')
        valores = grupo[features].values
        alvos = grupo[target].values
        anos = grupo['year'].values
        
        for i in range(len(grupo) - seq_length - FORECAST_HORIZON + 1):
            X_list.append(valores[i:i + seq_length])
            y_list.append(alvos[i + seq_length + FORECAST_HORIZON - 1])
            info_list.append({
                'country_code': pais,
                'year_pred': anos[i + seq_length + FORECAST_HORIZON - 1]
            })
    
    X = np.array(X_list)
    y = np.array(y_list)
    info = pd.DataFrame(info_list)
    
    return X, y, info


def preparar_para_lstm(df, nome_dataset):
    """Pipeline completo de preparação para LSTM."""
    print(f"\n  ── Preparação para LSTM ({nome_dataset}) ──")
    
    # Normalizar
    df_norm, scaler = normalizar_minmax(df)
    print(f"    ✅ Normalização Min-Max [0, 1]")
    
    # Criar sequências
    X, y, info = criar_sequencias(df_norm)
    print(f"    ✅ Sequências criadas: {X.shape}")
    print(f"       Shape: ({X.shape[0]} amostras, {X.shape[1]} passos, {X.shape[2]} features)")
    
    return X, y, info, scaler
