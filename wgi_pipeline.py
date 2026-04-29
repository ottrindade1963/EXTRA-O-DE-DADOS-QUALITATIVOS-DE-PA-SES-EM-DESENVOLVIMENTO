"""Pipeline completo de download e processamento de indicadores WGI."""

from wgi_downloader import baixar_todos_indicadores
from wgi_processor import pivotar_dados, converter_tipos_dados, ordenar_e_reorganizar, gerar_resumo
from wgi_exporter import exportar_dados


def executar_extracao_wgi():
    """Executa o pipeline completo: download → processamento → exportação."""
    
    print("\n" + "="*60)
    print("  EXTRAÇÃO DE INDICADORES QUALITATIVOS (WGI)")
    print("  Worldwide Governance Indicators")
    print("  API do Banco Mundial")
    print("="*60)
    
    try:
        # 1. Baixar dados da API
        wgi_combined = baixar_todos_indicadores()
        
        # 2. Pivotar para formato largo
        df_pivot = pivotar_dados(wgi_combined)
        
        # 3. Converter tipos de dados
        df_clean = converter_tipos_dados(df_pivot)
        
        # 4. Ordenar e reorganizar
        df_final = ordenar_e_reorganizar(df_clean)
        
        # 5. Gerar resumo
        df_final = gerar_resumo(df_final)
        
        # 6. Exportar dados
        exportar_dados(df_final)
        
        print("\n" + "="*60)
        print("  ✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60 + "\n")
        
        return df_final
    
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("="*60 + "\n")
        raise
