import pandas as pd
import requests
import time
from config import BASE_URL, INDICADORES, DATA_INICIO, DATA_FIM

def get_countries():
    """Obtém a lista completa de países e regiões do Banco Mundial."""
    print("-> Obtendo lista de países do Banco Mundial...")
    url = f"{BASE_URL}/country"
    params = {"format": "json", "per_page": 300}
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data[1]
    except Exception as e:
        print(f"Erro ao obter países: {e}")
        return []

def process_countries(countries_info):
    """Filtra a lista para obter apenas países em desenvolvimento (não HIC)."""
    df = pd.DataFrame(countries_info)

    # Extrair informações de dicionários aninhados
    df["region_name"] = df["region"].apply(lambda x: x.get("value") if isinstance(x, dict) else None)
    df["income_code"] = df["incomeLevel"].apply(lambda x: x.get("id") if isinstance(x, dict) else None)
    df.rename(columns={"id": "codigo_pais", "name": "nome_pais"}, inplace=True)

    # Filtro: apenas países reais (não agregados) e que não sejam de alta renda (HIC)
    paises_validos = df[
        (df["region_name"].notna()) &
        (df["region_name"] != "Aggregates") &
        (df["income_code"].notna()) &
        (df["income_code"] != "HIC") &
        (df["codigo_pais"].str.match(r"^[A-Z]{3}$"))
    ].copy()

    return paises_validos

def get_indicator_data(indicator_id, indicator_name, country_codes):
    """Baixa dados de um indicador específico para uma lista de países."""
    print(f"-> Baixando: {indicator_name} ({indicator_id})...")
    all_data = []

    # Dividir países em blocos para evitar URLs excessivamente longas
    chunk_size = 40
    for i in range(0, len(country_codes), chunk_size):
        chunk = country_codes[i:i + chunk_size]
        countries_str = ";".join(chunk)

        url = f"{BASE_URL}/country/{countries_str}/indicator/{indicator_id}"
        params = {
            "format": "json",
            "per_page": 2000,
            "date": f"{DATA_INICIO}:{DATA_FIM}"
        }

        try:
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()

            # A API retorna [metadata, data_list]
            if len(data) > 1 and data[1]:
                for entry in data[1]:
                    if entry["value"] is not None: # Apenas manter se houver valor
                        all_data.append({
                            "pais": entry["country"]["value"],
                            "codigo_iso3": entry["countryiso3code"],
                            "ano": int(entry["date"]),
                            indicator_name: entry["value"]
                        })
            # Pequeno delay para não sobrecarregar a API
            time.sleep(0.2)
        except Exception as e:
            print(f"   ! Erro no bloco {i//chunk_size + 1}: {e}")

    return pd.DataFrame(all_data)
