"""Orquestração da preparação de dados para os 5 modelos."""

import pandas as pd
import numpy as np
import os
from prep_config import DATASETS, OUTPUT_DIR, TRAIN_RATIO
from prep_base import (
    carregar_dataset, remover_missing_critico, imputar_missing,
    transformar_log, split_temporal, resumo_preparacao
)
from prep_trees import preparar_para_trees
from prep_lstm import preparar_para_lstm
from prep_sarimax import preparar_para_sarimax
from prep_tft import preparar_para_tft


def preparar_dataset(chave):
    """Prepara um dataset para os 5 modelos e exporta resultados."""
    path = DATASETS[chave]
    nome = f"Dataset {chave}"
    
    print(f"\n{'╔' + '═' * 68 + '╗'}")
    print(f"║  PREPARAÇÃO: {nome.upper():^54} ║")
    print(f"{'╚' + '═' * 68 + '╝'}")
    
    # 1. Carregar e limpeza base
    print(f"\n  ── Etapa Base ──")
    df = carregar_dataset(path)
    print(f"    ✅ Carregado: {df.shape}")
    
    df = remover_missing_critico(df)
    df = imputar_missing(df)
    df = transformar_log(df)
    print(f"    ✅ Transformação log aplicada")
    
    # Pasta de saída por dataset
    pasta = os.path.join(OUTPUT_DIR, chave)
    os.makedirs(pasta, exist_ok=True)
    
    # 2. Random Forest / XGBoost
    df_trees = preparar_para_trees(df.copy(), nome)
    treino_t, teste_t = split_temporal(df_trees, TRAIN_RATIO)
    treino_t.to_csv(os.path.join(pasta, 'trees_treino.csv'), index=False)
    teste_t.to_csv(os.path.join(pasta, 'trees_teste.csv'), index=False)
    resumo_preparacao(treino_t, 'RF/XGBoost treino')
    resumo_preparacao(teste_t, 'RF/XGBoost teste')
    
    # 3. LSTM
    X, y, info, scaler_lstm = preparar_para_lstm(df.copy(), nome)
    n_treino = int(len(X) * TRAIN_RATIO)
    np.savez(os.path.join(pasta, 'lstm_treino.npz'),
             X=X[:n_treino], y=y[:n_treino])
    np.savez(os.path.join(pasta, 'lstm_teste.npz'),
             X=X[n_treino:], y=y[n_treino:])
    info[:n_treino].to_csv(os.path.join(pasta, 'lstm_treino_info.csv'), index=False)
    info[n_treino:].to_csv(os.path.join(pasta, 'lstm_teste_info.csv'), index=False)
    print(f"    LSTM treino: {X[:n_treino].shape} | teste: {X[n_treino:].shape}")
    
    # 4. SARIMAX
    df_sarimax, exogenas = preparar_para_sarimax(df.copy(), nome)
    treino_s, teste_s = split_temporal(df_sarimax, TRAIN_RATIO)
    treino_s.to_csv(os.path.join(pasta, 'sarimax_treino.csv'), index=False)
    teste_s.to_csv(os.path.join(pasta, 'sarimax_teste.csv'), index=False)
    # Salvar lista de exógenas
    pd.Series(exogenas).to_csv(os.path.join(pasta, 'sarimax_exogenas.csv'), index=False)
    resumo_preparacao(treino_s, 'SARIMAX treino')
    resumo_preparacao(teste_s, 'SARIMAX teste')
    
    # 5. TFT
    df_tft, scaler_tft, classificacao = preparar_para_tft(df.copy(), nome)
    treino_tft, teste_tft = split_temporal(df_tft, TRAIN_RATIO)
    treino_tft.to_csv(os.path.join(pasta, 'tft_treino.csv'), index=False)
    teste_tft.to_csv(os.path.join(pasta, 'tft_teste.csv'), index=False)
    # Salvar classificação de variáveis
    pd.DataFrame({k: [str(v)] for k, v in classificacao.items()}).to_csv(
        os.path.join(pasta, 'tft_classificacao.csv'), index=False)
    resumo_preparacao(treino_tft, 'TFT treino')
    resumo_preparacao(teste_tft, 'TFT teste')
    
    print(f"\n  ✅ Ficheiros salvos em: {pasta}/")
    return pasta


def executar_preparacao():
    """Executa a preparação completa dos 3 datasets para os 5 modelos."""
    
    print("╔" + "═" * 68 + "╗")
    print("║  PREPARAÇÃO DE DADOS PARA MODELAGEM — 5 MODELOS × 3 DATASETS     ║")
    print("╚" + "═" * 68 + "╝")
    
    pastas = {}
    for chave in DATASETS:
        pastas[chave] = preparar_dataset(chave)
    
    # Resumo final
    print(f"\n{'═' * 70}")
    print(f"  ✅ PREPARAÇÃO COMPLETA")
    print(f"{'═' * 70}")
    for chave, pasta in pastas.items():
        ficheiros = os.listdir(pasta)
        print(f"  • {chave}: {len(ficheiros)} ficheiros em {pasta}/")
    
    total = sum(len(os.listdir(p)) for p in pastas.values())
    print(f"\n  Total: {total} ficheiros gerados")
    print(f"  Modelos: LSTM, Random Forest, XGBoost, SARIMAX, TFT")
    print(f"  Split: {TRAIN_RATIO*100:.0f}% treino / {(1-TRAIN_RATIO)*100:.0f}% teste")
    print(f"{'═' * 70}")
    
    return pastas
