#!/usr/bin/env python3
"""
Script de Exemplo - Uso Programático do Extrator

Este script demonstra como usar os módulos do extrator
de forma programática em seus próprios projetos.
"""

import sys
import os

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.orchestrator import WorldBankOrchestrator
from src.api_client import WorldBankAPIClient
from src.data_extractor import DataExtractor
from src.data_processor import DataProcessor
from src.logger import logger


def exemplo_completo():
    """Exemplo de uso completo do orquestrador"""
    logger.info("=== EXEMPLO 1: Uso Completo do Orquestrador ===")
    
    # Criar orquestrador
    orchestrator = WorldBankOrchestrator(
        start_year=2015,
        end_year=2020
    )
    
    # Executar extração completa
    data = orchestrator.run()
    
    logger.info(f"Dados extraídos: {len(data)} indicadores")
    return data


def exemplo_modular():
    """Exemplo de uso modular dos componentes"""
    logger.info("=== EXEMPLO 2: Uso Modular dos Componentes ===")
    
    # 1. Obter países
    api_client = WorldBankAPIClient()
    countries = api_client.get_developing_countries()
    logger.info(f"Países obtidos: {len(countries)}")
    
    # 2. Extrair apenas alguns indicadores
    indicadores_selecionados = {
        "SP.POP.TOTL": "Populacao_Total",
        "NY.GDP.MKTP.KD.ZG": "Crescimento_PIB"
    }
    
    extractor = DataExtractor(
        start_year=2018,
        end_year=2022,
        countries=countries[:10]  # Apenas 10 primeiros países
    )
    
    data = extractor.fetch_all_indicators(indicadores_selecionados)
    
    # 3. Processar dados
    processor = DataProcessor()
    cleaned_data = processor.clean_data(data)
    stats = processor.get_data_statistics(cleaned_data)
    
    logger.info(f"Estatísticas: {stats}")
    
    return cleaned_data


def exemplo_api_client():
    """Exemplo de uso do cliente API"""
    logger.info("=== EXEMPLO 3: Uso do Cliente API ===")
    
    api_client = WorldBankAPIClient()
    
    # Obter metadados de um indicador específico
    metadata = api_client.get_indicator_metadata("SP.POP.TOTL")
    
    logger.info(f"Metadados do indicador População Total:")
    logger.info(f"  Nome: {metadata.get('name')}")
    logger.info(f"  Fonte: {metadata.get('source_organization')}")
    
    return metadata


def exemplo_processamento():
    """Exemplo de processamento de dados"""
    logger.info("=== EXEMPLO 4: Processamento de Dados ===")
    
    import pandas as pd
    
    # Criar dados de exemplo
    df1 = pd.DataFrame({
        'country': ['BRA', 'BRA', 'ARG', 'ARG'],
        'ano': [2020, 2021, 2020, 2021],
        'Populacao_Total': [212559417, 214326223, 45195774, 45808747]
    })
    
    df2 = pd.DataFrame({
        'country': ['BRA', 'BRA', 'ARG', 'ARG'],
        'ano': [2020, 2021, 2020, 2021],
        'Crescimento_PIB': [-3.9, 4.6, -9.9, 10.3]
    })
    
    data = {
        'Populacao_Total': df1,
        'Crescimento_PIB': df2
    }
    
    # Processar
    processor = DataProcessor()
    cleaned = processor.clean_data(data)
    consolidated = processor.consolidate_data(cleaned)
    
    logger.info(f"Dataset consolidado:\n{consolidated}")
    
    return consolidated


def main():
    """Função principal com exemplos"""
    try:
        logger.info("=" * 60)
        logger.info("EXEMPLOS DE USO DO EXTRATOR DO BANCO MUNDIAL")
        logger.info("=" * 60)
        
        # Descomente o exemplo que deseja executar:
        
        # exemplo_completo()
        # exemplo_modular()
        exemplo_api_client()
        # exemplo_processamento()
        
        logger.info("=" * 60)
        logger.info("EXEMPLOS CONCLUÍDOS")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Erro ao executar exemplo: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
