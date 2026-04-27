"""
Módulo Orquestrador
Coordena todo o processo de extração, processamento e exportação de dados
"""

from typing import Dict
import pandas as pd
from src.config import INDICATORS
from src.api_client import WorldBankAPIClient
from src.data_extractor import DataExtractor
from src.data_processor import DataProcessor
from src.data_exporter import DataExporter
from src.logger import logger


class WorldBankOrchestrator:
    """Orquestrador do processo de extração de dados do Banco Mundial"""
    
    def __init__(self, start_year: int, end_year: int):
        """
        Inicializa o orquestrador
        
        Args:
            start_year: Ano inicial do período
            end_year: Ano final do período
        """
        self.start_year = start_year
        self.end_year = end_year
        self.api_client = WorldBankAPIClient()
        self.countries = []
        self.indicators = INDICATORS
    
    def run(self) -> Dict[str, pd.DataFrame]:
        """
        Executa todo o processo de extração
        
        Returns:
            Dicionário com os dados extraídos e processados
        """
        logger.info("=" * 60)
        logger.info("INICIANDO EXTRAÇÃO DE DADOS DO BANCO MUNDIAL")
        logger.info("=" * 60)
        logger.info(f"Período: {self.start_year}-{self.end_year}")
        logger.info(f"Indicadores: {len(self.indicators)}")
        
        # 1. Obter lista de países
        self.countries = self.api_client.get_developing_countries()
        logger.info(f"Países a processar: {len(self.countries)}")
        
        # 2. Obter metadados dos indicadores
        metadata = self.api_client.get_all_indicators_metadata(self.indicators)
        
        # 3. Extrair dados
        extractor = DataExtractor(
            self.start_year, 
            self.end_year, 
            self.countries
        )
        raw_data = extractor.fetch_all_indicators(self.indicators)
        extraction_summary = extractor.get_extraction_summary()
        
        # 4. Processar dados
        processor = DataProcessor()
        cleaned_data = processor.clean_data(raw_data)
        consolidated_data = processor.consolidate_data(cleaned_data)
        data_stats = processor.get_data_statistics(cleaned_data)
        
        # 5. Exportar dados
        exporter = DataExporter(self.start_year, self.end_year)
        exporter.save_individual_indicators(cleaned_data)
        exporter.save_consolidated_dataset(consolidated_data)
        exporter.save_metadata(metadata)
        exporter.save_execution_report(
            extraction_summary,
            data_stats,
            len(self.countries)
        )
        
        # 6. Exibir resumo
        self._print_summary(extraction_summary, data_stats)
        
        logger.info("=" * 60)
        logger.info("EXTRAÇÃO CONCLUÍDA")
        logger.info("=" * 60)
        
        return cleaned_data
    
    def _print_summary(
        self, 
        extraction_summary: Dict, 
        data_stats: Dict
    ) -> None:
        """
        Exibe resumo da execução
        
        Args:
            extraction_summary: Resumo da extração
            data_stats: Estatísticas dos dados
        """
        logger.info("=" * 60)
        logger.info("RESUMO DA EXTRAÇÃO")
        logger.info("=" * 60)
        
        logger.info(f"Países processados: {len(self.countries)}")
        logger.info(
            f"Indicadores bem-sucedidos: "
            f"{extraction_summary['successful_count']}"
        )
        logger.info(
            f"Indicadores falhados: "
            f"{extraction_summary['failed_count']}"
        )
        logger.info(f"Total de registros: {data_stats['total_records']}")
        
        if extraction_summary['successful_indicators']:
            logger.info("\nIndicadores extraídos com sucesso:")
            for code, name, count in extraction_summary['successful_indicators']:
                logger.info(f"  {code} ({name}): {count} registros")
        
        if extraction_summary['failed_indicators']:
            logger.info("\nIndicadores que falharam:")
            for code, name, error in extraction_summary['failed_indicators']:
                logger.info(f"  {code} ({name}): {error}")
