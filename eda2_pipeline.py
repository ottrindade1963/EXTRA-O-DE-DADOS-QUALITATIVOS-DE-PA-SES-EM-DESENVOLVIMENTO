"""Pipeline de segunda análise exploratória (dados limpos)."""

from eda2_config import DATA_PATH, OUTPUT_DIR
from eda2_loader import (
    carregar_dados, resumo_geral, estatisticas_descritivas, intervalos_confianca,
    testes_normalidade, estatisticas_por_decada, matriz_correlacao
)
from eda2_visualizacoes import gerar_todos_graficos


def executar_eda2():
    """Executa o pipeline completo da segunda análise exploratória."""
    
    print("\n" + "="*60)
    print("  SEGUNDA ANÁLISE EXPLORATÓRIA")
    print("  Dados Limpos — Países Emergentes")
    print("="*60)
    
    # 1. Carregar dados
    df = carregar_dados(DATA_PATH)
    
    # 2. Resumo geral
    resumo_geral(df)
    
    # 3. Estatísticas descritivas
    df_stats = estatisticas_descritivas(df)
    
    # 4. Intervalos de confiança
    df_ic = intervalos_confianca(df)
    
    # 5. Testes de normalidade
    df_testes = testes_normalidade(df)
    
    # 6. Estatísticas por década
    df = estatisticas_por_decada(df)
    
    # 7. Matriz de correlação
    corr_matrix = matriz_correlacao(df)
    
    # 8. Gerar visualizações
    gerar_todos_graficos(df)
    
    print("\n" + "="*60)
    print("  ✅ ANÁLISE EXPLORATÓRIA CONCLUÍDA!")
    print(f"  📁 Resultados salvos em: {OUTPUT_DIR}/")
    print("="*60 + "\n")
    
    return df, df_stats, df_ic, df_testes, corr_matrix
