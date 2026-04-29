"""Pipeline completo: download → processamento → integração → exportação."""

from wgi_downloader import baixar_wgi, baixar_qog
from wgi_processor import processar_wgi, processar_icrg, integrar_datasets
from wgi_exporter import exportar_dados


def executar_extracao_wgi():
    """Executa o pipeline completo de extração qualitativa."""
    
    print("\n" + "="*60)
    print("  EXTRAÇÃO DE INDICADORES QUALITATIVOS")
    print("  WGI (Banco Mundial) + ICRG (QoG)")
    print("="*60)
    
    try:
        # 1. Download do WGI
        wgi_raw = baixar_wgi()
        
        # 2. Processar WGI (todas as abas)
        wgi_clean = processar_wgi(wgi_raw)
        
        # 3. Download do QoG (ICRG)
        qog_df = baixar_qog()
        
        # 4. Processar ICRG
        icrg_clean = processar_icrg(qog_df)
        
        # 5. Integrar datasets
        df_final = integrar_datasets(wgi_clean, icrg_clean)
        
        # 6. Exportar
        exportar_dados(df_final)
        
        print("\n" + "="*60)
        print("  ✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60 + "\n")
        
        return df_final
    
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("="*60 + "\n")
        raise
