"""Download de indicadores WGI - Modo híbrido (local + API)."""

import os
import requests
import pandas as pd
import time
from wgi_config import (
    WGI_API_BASE, WGI_INDICATORS, ANO_MINIMO, ANO_MAXIMO,
    TIMEOUT, MAX_RETRIES, RETRY_DELAY, NOMES_INDICADORES
)


def verificar_arquivo_local():
    """Verifica se o ficheiro wgi_raw.xlsx existe localmente."""
    if os.path.exists("wgi_raw.xlsx"):
        print("✅ Ficheiro wgi_raw.xlsx encontrado localmente")
        return True
    return False


def carregar_de_arquivo_local():
    """Carrega dados WGI do ficheiro Excel local."""
    print("\n📂 Carregando dados do ficheiro local (wgi_raw.xlsx)...")
    
    try:
        wgi_raw = pd.ExcelFile("wgi_raw.xlsx")
        print(f"   Abas disponíveis: {wgi_raw.sheet_names}")
        
        all_data = []
        
        for sheet_name in wgi_raw.sheet_names:
            if sheet_name not in WGI_INDICATORS:
                continue
            
            indicator_name = WGI_INDICATORS[sheet_name]
            print(f"   Processando aba: {sheet_name} ({NOMES_INDICADORES[indicator_name]})")
            
            df = wgi_raw.parse(sheet_name)
            
            # Filtra dados agregados
            if 'indicator' in df.columns:
                mask = df['indicator'].str.lower().str.contains('average', na=False)
                df_subset = df[mask].copy()
                if df_subset.empty:
                    df_subset = df.copy()
            else:
                df_subset = df.copy()
            
            # Seleciona colunas
            if 'econ_code' in df_subset.columns and 'production_year' in df_subset.columns and 'value' in df_subset.columns:
                df_subset = df_subset[['econ_code', 'production_year', 'value']].copy()
                df_subset.columns = ['country_code', 'year', 'value']
                
                # Remove faltantes
                df_subset = df_subset.dropna(subset=['country_code', 'year', 'value'])
                
                # Filtra período
                df_subset = df_subset[
                    (df_subset['year'] >= ANO_MINIMO) & (df_subset['year'] <= ANO_MAXIMO)
                ]
                
                # Adiciona indicador
                df_subset['indicator'] = indicator_name
                
                # Remove duplicatas
                df_subset = df_subset.drop_duplicates(subset=['country_code', 'year'], keep='first')
                
                if not df_subset.empty:
                    all_data.append(df_subset)
                    print(f"     ✅ {len(df_subset)} linhas extraídas")
        
        if all_data:
            wgi_combined = pd.concat(all_data, ignore_index=True)
            print(f"\n   Total: {len(wgi_combined)} registros")
            return wgi_combined
        else:
            raise ValueError("Nenhum dado válido encontrado no ficheiro")
    
    except Exception as e:
        print(f"   ❌ Erro ao carregar ficheiro: {e}")
        raise


def fazer_requisicao_com_retry(url, max_retries=MAX_RETRIES):
    """Faz requisição HTTP com retry automático."""
    for tentativa in range(max_retries):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if tentativa < max_retries - 1:
                print(f"    ⚠️  Tentativa {tentativa + 1} falhou, retentando...")
                time.sleep(RETRY_DELAY)
            else:
                raise Exception(f"Falha após {max_retries} tentativas: {e}")


def baixar_de_api():
    """Tenta baixar dados da API do Banco Mundial."""
    print("\n🌐 Tentando baixar da API do Banco Mundial...")
    print("   ⚠️  NOTA: Os indicadores WGI podem não estar disponíveis na API")
    print("   Recomendação: Use o ficheiro wgi_raw.xlsx local\n")
    
    raise ValueError("API WGI não está disponível. Use o ficheiro wgi_raw.xlsx local.")


def baixar_todos_indicadores():
    """Baixa indicadores WGI - tenta local primeiro, depois API."""
    print("\n" + "="*60)
    print("  📥 CARREGANDO INDICADORES WGI")
    print("="*60)
    
    # Tentar carregar do ficheiro local primeiro
    if verificar_arquivo_local():
        try:
            return carregar_de_arquivo_local()
        except Exception as e:
            print(f"   Erro ao carregar local: {e}")
            print("   Tentando API...")
    
    # Se não conseguir localmente, tentar API
    print("\n📥 Ficheiro local não encontrado")
    try:
        return baixar_de_api()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\n" + "="*60)
        print("  ⚠️  SOLUÇÃO:")
        print("="*60)
        print("  1. Faça download do ficheiro WGI do Banco Mundial")
        print("  2. Salve como 'wgi_raw.xlsx' na raiz do repositório")
        print("  3. Execute novamente este script")
        print("="*60 + "\n")
        raise
