"""Processamento dos dados WGI e ICRG."""

import pandas as pd
from wgi_config import ANO_MINIMO, ANO_MAXIMO, ICRG_COLS

# Mapeamento de abas para nomes de indicadores
SHEET_TO_INDICATOR = {
    'VA': 'wgi_voice_accountability',
    'PV': 'wgi_political_stability',
    'GE': 'wgi_gov_effectiveness',
    'RQ': 'wgi_regulatory_quality',
    'RL': 'wgi_rule_law',
    'CC': 'wgi_control_corruption'
}


def processar_wgi(wgi_raw):
    """Processa todas as abas do ficheiro WGI."""
    print("\n🔧 Processando WGI...")
    
    all_data = []
    
    for sheet_name in wgi_raw.sheet_names:
        if sheet_name not in SHEET_TO_INDICATOR:
            continue
        
        indicator_name = SHEET_TO_INDICATOR[sheet_name]
        print(f"   Aba: {sheet_name} ({indicator_name})")
        
        df = wgi_raw.parse(sheet_name)
        
        # Filtra dados agregados (contêm "average")
        if 'indicator' in df.columns:
            mask = df['indicator'].str.lower().str.contains('average', na=False)
            df_subset = df[mask].copy()
            if df_subset.empty:
                df_subset = df.copy()
        else:
            df_subset = df.copy()
        
        # Seleciona colunas relevantes
        if 'econ_code' in df_subset.columns and 'production_year' in df_subset.columns and 'value' in df_subset.columns:
            df_subset = df_subset[['econ_code', 'production_year', 'value']].copy()
            df_subset.columns = ['country_code', 'year', 'value']
            
            df_subset = df_subset.dropna(subset=['country_code', 'year', 'value'])
            df_subset['country_code'] = df_subset['country_code'].astype(str).str.strip()
            df_subset['year'] = df_subset['year'].astype(int)
            df_subset = df_subset[
                (df_subset['year'] >= ANO_MINIMO) & (df_subset['year'] <= ANO_MAXIMO)
            ]
            df_subset['indicator'] = indicator_name
            df_subset = df_subset.drop_duplicates(subset=['country_code', 'year'], keep='first')
            
            if not df_subset.empty:
                all_data.append(df_subset)
                print(f"     ✅ {len(df_subset)} linhas")
    
    if not all_data:
        raise ValueError("Nenhum dado WGI extraído")
    
    # Combina e pivota para formato largo
    wgi_combined = pd.concat(all_data, ignore_index=True)
    
    wgi_clean = wgi_combined.pivot_table(
        index=['country_code', 'year'],
        columns='indicator',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    wgi_clean.columns.name = None
    wgi_clean['year'] = wgi_clean['year'].astype(int)
    wgi_clean['country_code'] = wgi_clean['country_code'].astype(str)
    
    for col in wgi_clean.columns:
        if col not in ['country_code', 'year']:
            wgi_clean[col] = pd.to_numeric(wgi_clean[col], errors='coerce')
    
    print(f"\n   ✅ WGI processado: {len(wgi_clean)} linhas (país-ano)")
    return wgi_clean


def processar_icrg(qog_df):
    """Processa os dados ICRG do dataset QoG."""
    print("\n🔧 Processando ICRG...")
    
    # Verifica colunas disponíveis
    missing_qog = [c for c in ICRG_COLS.keys() if c not in qog_df.columns]
    
    if missing_qog:
        print(f"   ⚠️  Colunas ausentes: {missing_qog}")
        existentes = {k: v for k, v in ICRG_COLS.items() if k in qog_df.columns}
        if not existentes:
            raise KeyError("Nenhuma coluna ICRG encontrada no QoG")
        icrg_subset = qog_df[list(existentes.keys())].rename(columns=existentes)
    else:
        icrg_subset = qog_df[list(ICRG_COLS.keys())].rename(columns=ICRG_COLS)
    
    # Garantir tipos corretos
    icrg_subset['country_code'] = icrg_subset['country_code'].astype(str).str.strip()
    icrg_subset['year'] = icrg_subset['year'].astype(int)
    
    # Filtra período e remove linhas sem país
    icrg_subset = icrg_subset[
        (icrg_subset['year'] >= ANO_MINIMO) & (icrg_subset['year'] <= ANO_MAXIMO)
    ]
    icrg_subset = icrg_subset.dropna(subset=['country_code'])
    icrg_subset = icrg_subset[icrg_subset['country_code'] != 'nan']
    
    print(f"   ✅ ICRG processado: {len(icrg_subset)} linhas (país-ano)")
    return icrg_subset


def integrar_datasets(wgi_clean, icrg_subset):
    """Integra WGI e ICRG num único dataset."""
    print("\n🔗 Integrando WGI e ICRG...")
    
    # Garantir tipos iguais para merge
    wgi_clean['country_code'] = wgi_clean['country_code'].astype(str)
    icrg_subset['country_code'] = icrg_subset['country_code'].astype(str)
    wgi_clean['year'] = wgi_clean['year'].astype(int)
    icrg_subset['year'] = icrg_subset['year'].astype(int)
    
    final_df = wgi_clean.merge(icrg_subset, on=['country_code', 'year'], how='outer')
    final_df = final_df.sort_values(['country_code', 'year']).reset_index(drop=True)
    
    print(f"   ✅ Dataset integrado: {len(final_df)} linhas, {len(final_df.columns)} colunas")
    return final_df
