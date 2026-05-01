"""Treino e avaliação do LSTM."""

import numpy as np
import os
from model_config import LSTM_CONFIG
from model_metrics import calcular_metricas, imprimir_metricas


def construir_lstm(input_shape):
    """Constrói a arquitetura LSTM."""
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    
    modelo = Sequential([
        LSTM(LSTM_CONFIG['units_1'], return_sequences=True, input_shape=input_shape),
        Dropout(LSTM_CONFIG['dropout']),
        LSTM(LSTM_CONFIG['units_2'], return_sequences=False),
        Dropout(LSTM_CONFIG['dropout']),
        Dense(16, activation='relu'),
        Dense(1)
    ])
    
    modelo.compile(
        optimizer=Adam(learning_rate=LSTM_CONFIG['learning_rate']),
        loss='mse',
        metrics=['mae']
    )
    
    return modelo


def treinar_lstm(prefixo):
    """Treina e avalia LSTM.
    
    Args:
        prefixo: prefixo do dataset (ex: 'inner', 'left', 'outer')
    """
    from tensorflow.keras.callbacks import EarlyStopping
    
    print("\n  ── LSTM ──")
    
    # Carregar dados dos ficheiros .npz na raiz
    treino_path = f"{prefixo}_lstm_treino.npz"
    teste_path = f"{prefixo}_lstm_teste.npz"
    
    if not os.path.exists(treino_path) or not os.path.exists(teste_path):
        raise FileNotFoundError(f"Ficheiros LSTM não encontrados: {treino_path} ou {teste_path}")
        
    treino_npz = np.load(treino_path)
    teste_npz = np.load(teste_path)
    
    X_treino = treino_npz['X']
    y_treino = treino_npz['y']
    X_teste = teste_npz['X']
    y_teste = teste_npz['y']
    
    print(f"    Treino: {X_treino.shape} | Teste: {X_teste.shape}")
    
    # Construir modelo
    input_shape = (X_treino.shape[1], X_treino.shape[2])
    modelo = construir_lstm(input_shape)
    print(f"    Arquitetura: LSTM({LSTM_CONFIG['units_1']}) → LSTM({LSTM_CONFIG['units_2']}) → Dense(16) → Dense(1)")
    
    # Treinar
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=LSTM_CONFIG['patience'],
        restore_best_weights=True,
        verbose=0
    )
    
    historico = modelo.fit(
        X_treino, y_treino,
        validation_data=(X_teste, y_teste),
        epochs=LSTM_CONFIG['epochs'],
        batch_size=LSTM_CONFIG['batch_size'],
        callbacks=[early_stop],
        verbose=0
    )
    
    epocas_treinadas = len(historico.history['loss'])
    print(f"    ✅ Treinado em {epocas_treinadas} épocas (early stopping)")
    
    # Prever
    y_pred = modelo.predict(X_teste, verbose=0).flatten()
    
    # Métricas
    metricas = calcular_metricas(y_teste, y_pred, 'LSTM')
    imprimir_metricas(metricas)
    
    return modelo, metricas, y_pred, y_teste, historico
