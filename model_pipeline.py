"""Orquestração do treino e avaliação dos 5 modelos × 3 datasets."""

import os
import numpy as np
import pandas as pd
from model_config import DATASETS, OUTPUT_DIR
from model_metrics import tabela_comparativa
from model_rf import treinar_random_forest
from model_xgboost import treinar_xgboost
from model_lstm import treinar_lstm
from model_sarimax import treinar_sarimax
from model_tft import treinar_tft
from model_visualizacoes import gerar_visualizacoes


def treinar_dataset(chave, pasta_dados):
    """Treina os 5 modelos para um dataset e retorna resultados."""
    
    print(f"\n{'╔' + '═' * 68 + '╗'}")
    print(f"║  TREINO E AVALIAÇÃO: {chave.upper():^46} ║")
    print(f"{'╚' + '═' * 68 + '╝'}")
    
    resultados = {}
    metricas_lista = []
    
    # 1. Random Forest
    try:
        _, met_rf, y_pred_rf, y_real_rf, _ = treinar_random_forest(
            os.path.join(pasta_dados, 'trees_treino.csv'),
            os.path.join(pasta_dados, 'trees_teste.csv')
        )
        resultados['Random Forest'] = {'metricas': met_rf, 'y_pred': y_pred_rf, 'y_real': y_real_rf}
        metricas_lista.append(met_rf)
    except Exception as e:
        print(f"    ❌ Random Forest falhou: {e}")
    
    # 2. XGBoost
    try:
        _, met_xgb, y_pred_xgb, y_real_xgb, _ = treinar_xgboost(
            os.path.join(pasta_dados, 'trees_treino.csv'),
            os.path.join(pasta_dados, 'trees_teste.csv')
        )
        resultados['XGBoost'] = {'metricas': met_xgb, 'y_pred': y_pred_xgb, 'y_real': y_real_xgb}
        metricas_lista.append(met_xgb)
    except Exception as e:
        print(f"    ❌ XGBoost falhou: {e}")
    
    # 3. LSTM
    try:
        _, met_lstm, y_pred_lstm, y_real_lstm, _ = treinar_lstm(pasta_dados)
        resultados['LSTM'] = {'metricas': met_lstm, 'y_pred': y_pred_lstm, 'y_real': y_real_lstm}
        metricas_lista.append(met_lstm)
    except Exception as e:
        print(f"    ❌ LSTM falhou: {e}")
    
    # 4. SARIMAX
    try:
        _, met_sar, y_pred_sar, y_real_sar, _ = treinar_sarimax(
            os.path.join(pasta_dados, 'sarimax_treino.csv'),
            os.path.join(pasta_dados, 'sarimax_teste.csv'),
            os.path.join(pasta_dados, 'sarimax_exogenas.csv')
        )
        resultados['SARIMAX'] = {'metricas': met_sar, 'y_pred': y_pred_sar, 'y_real': y_real_sar}
        metricas_lista.append(met_sar)
    except Exception as e:
        print(f"    ❌ SARIMAX falhou: {e}")
    
    # 5. TFT
    try:
        _, met_tft, y_pred_tft, y_real_tft, _ = treinar_tft(
            os.path.join(pasta_dados, 'tft_treino.csv'),
            os.path.join(pasta_dados, 'tft_teste.csv')
        )
        resultados['TFT (GRU+Attn)'] = {'metricas': met_tft, 'y_pred': y_pred_tft, 'y_real': y_real_tft}
        metricas_lista.append(met_tft)
    except Exception as e:
        print(f"    ❌ TFT falhou: {e}")
    
    # Tabela comparativa
    tabela = tabela_comparativa(metricas_lista)
    print(f"\n  ── TABELA COMPARATIVA ({chave}) ──")
    print(tabela.to_string())
    
    # Visualizações
    pasta_saida = os.path.join(OUTPUT_DIR, chave)
    gerar_visualizacoes(resultados, tabela, pasta_saida)
    
    # Salvar tabela
    tabela.to_csv(os.path.join(pasta_saida, 'comparacao_modelos.csv'), index=True)
    
    return resultados, tabela


def executar_treino_avaliacao():
    """Executa treino e avaliação completa para os 3 datasets."""
    
    print("╔" + "═" * 68 + "╗")
    print("║  TREINO E AVALIAÇÃO — 5 MODELOS × 3 DATASETS                     ║")
    print("╚" + "═" * 68 + "╝")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    todos_resultados = {}
    todas_tabelas = {}
    
    for chave, pasta in DATASETS.items():
        if not os.path.exists(pasta):
            print(f"\n  ⚠️ Pasta não encontrada: {pasta}")
            print(f"      Verifique se o notebook Preparacao_Dados.ipynb foi executado.")
            continue
        resultados, tabela = treinar_dataset(chave, pasta)
        todos_resultados[chave] = resultados
        todas_tabelas[chave] = tabela
    
    # Resumo final
    print(f"\n{'═' * 70}")
    print(f"  ✅ TREINO E AVALIAÇÃO COMPLETOS")
    print(f"{'═' * 70}")
    
    for chave, tabela in todas_tabelas.items():
        melhor = tabela.iloc[0]
        print(f"\n  {chave.upper()}:")
        print(f"    🏆 Melhor modelo: {melhor['modelo']}")
        print(f"       RMSE={melhor['RMSE']:.4f} | R²={melhor['R2']:.4f} | MAPE={melhor['MAPE (%)']:.2f}%")
    
    print(f"\n{'═' * 70}")
    
    return todos_resultados, todas_tabelas
