import pandas as pd
import os
from data_extractor import get_countries, process_countries, get_indicator_data
from config import DATA_DIR, INDICADORES

def run_extraction():
    print("=== INICIANDO DOWNLOAD DE DADOS WDI ===")

    # 1. Identificar países alvo
    countries_raw = get_countries()
    if not countries_raw:
        print("ERRO: Não foi possível obter a lista de países.")
        return

    paises_validos = process_countries(countries_raw)
    paises_dev_id = paises_validos["codigo_pais"].tolist()
    print(f"✅ {len(paises_dev_id)} países em desenvolvimento identificados.")

    # Salvar lista de países para referência
    os.makedirs(DATA_DIR, exist_ok=True)
    paises_validos.to_csv(f'{DATA_DIR}/paises_em_desenvolvimento_limpos.csv', index=False)

    # 2. Baixar dados de cada indicador e consolidar
    df_final = pd.DataFrame()

    for id_ind, nome_ind in INDICADORES.items():
        df_ind = get_indicator_data(id_ind, nome_ind, paises_dev_id)

        if df_ind.empty:
            print(f"   ⚠️ Nenhum dado encontrado para {nome_ind}")
            continue

        if df_final.empty:
            df_final = df_ind
        else:
            # Merge usando outer join para preservar todos os anos/países disponíveis
            df_final = pd.merge(df_final, df_ind, on=["pais", "codigo_iso3", "ano"], how="outer")

    # 3. Finalização e Exportação
    if not df_final.empty:
        # Ordenar por país e ano
        df_final = df_final.sort_values(["pais", "ano"])

        # Salvar em CSV e Excel
        csv_path = f'{DATA_DIR}/wdi_emergentes_final.csv'
        xlsx_path = f'{DATA_DIR}/wdi_emergentes_final.xlsx'

        df_final.to_csv(csv_path, index=False)
        df_final.to_excel(xlsx_path, index=False)

        print("\n=== PROCESSO CONCLUÍDO COM SUCESSO ===")
        print(f"📊 Total de registros (país-ano): {len(df_final)}")
        print(f"📂 Arquivos gerados em '{DATA_DIR}':")
        print(f"   - wdi_emergentes_final.csv")
        print(f"   - wdi_emergentes_final.xlsx")
        print(f"   - paises_em_desenvolvimento_limpos.csv")

        print("\nResumo dos dados (primeiras 5 linhas):")
        print(df_final.head())
    else:
        print("\n❌ Falha crítica: Nenhum dado foi coletado.")

if __name__ == "__main__":
    run_extraction()
