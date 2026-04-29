"""Exportação de dados WGI processados."""

import pandas as pd
from wgi_config import CSV_OUTPUT, XLSX_OUTPUT, OUTPUT_DIR


def exportar_csv(df, path=CSV_OUTPUT):
    """Exporta dados para CSV."""
    try:
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  ✅ CSV: {path}")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao exportar CSV: {e}")
        return False


def exportar_xlsx(df, path=XLSX_OUTPUT):
    """Exporta dados para Excel."""
    try:
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            # Aba de dados
            df.to_excel(writer, sheet_name='Dados', index=False)
            
            # Aba de metadados
            metadados = pd.DataFrame({
                'Metadado': [
                    'Total de linhas',
                    'Total de colunas',
                    'Período',
                    'Países',
                    'Data de processamento'
                ],
                'Valor': [
                    len(df),
                    len(df.columns),
                    f"{df['year'].min()}-{df['year'].max()}",
                    df['country_code'].nunique(),
                    pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            })
            metadados.to_excel(writer, sheet_name='Metadados', index=False)
        
        print(f"  ✅ XLSX: {path}")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao exportar XLSX: {e}")
        return False


def exportar_dados(df):
    """Exporta dados em ambos os formatos."""
    print(f"\n" + "="*60)
    print(f"  💾 EXPORTANDO DADOS")
    print(f"="*60 + "\n")
    
    csv_ok = exportar_csv(df)
    xlsx_ok = exportar_xlsx(df)
    
    if csv_ok and xlsx_ok:
        print(f"\n  ✅ Exportação concluída com sucesso!")
        print(f"  📁 Ficheiros salvos em: {OUTPUT_DIR}/")
        return True
    else:
        print(f"\n  ⚠️  Exportação parcial (alguns formatos falharam)")
        return False
