"""
Módulo de Extração de Dados
Responsável por buscar dados dos indicadores do Banco Mundial
"""

import pandas as pd
import wbdata
import time
from datetime import datetime
from typing import Dict, List, Tuple
from src.config import API_DELAY_BETWEEN_REQUESTS
from src.logger import logger


class DataExtractor:
    """Extrator de dados do Banco Mundial"""
    
    def __init__(self, start_year: int, end_year: int, countries: List[str]):
        """
        Inicializa o extrator de dados
        
        Args:
            start_year: Ano inicial do período
            end_year: Ano final do período
            countries: Lista de códigos de países
        """
        self.start_year = start_year
        self.end_year = end_year
        self.countries = countries
        self.successful_indicators: List[Tuple[str, str, int]] = []
        self.failed_indicators: List[Tuple[str, str, str]] = []
    
    def fetch_single_indicator(
        self, 
        indicator_code: str, 
        indicator_name: str
    ) -> pd.DataFrame:
        """
        Busca dados de um indicador específico
        
        Args:
            indicator_code: Código do indicador
            indicator_name: Nome do indicador
            
        Returns:
            DataFrame com os dados do indicador
        """
        logger.info(f"Buscando {indicator_name} ({indicator_code})")
        
        for attempt in range(2):
            try:
                # Buscar dados usando wbdata
                data = wbdata.get_dataframe(
                    {indicator_code: indicator_name},
                    country=self.countries,
                    date=(
                        datetime(self.start_year, 1, 1), 
                        datetime(self.end_year, 12, 31)
                    )
                )
                
                if data.empty:
                    logger.warning(f"Sem dados para {indicator_code}")
                    self.failed_indicators.append(
                        (indicator_code, indicator_name, "Sem dados")
                    )
                    return pd.DataFrame()
                
                # Resetar índice e processar
                data_reset = data.reset_index()
                
                # Verificar colunas esperadas
                expected_columns = ['country', 'date', indicator_name]
                if not all(col in data_reset.columns for col in expected_columns):
                    logger.error(
                        f"Colunas incorretas para {indicator_code}: "
                        f"{data_reset.columns.tolist()}"
                    )
                    self.failed_indicators.append(
                        (indicator_code, indicator_name, "Estrutura incorreta")
                    )
                    return pd.DataFrame()
                
                # Renomear coluna de data para 'ano'
                data_reset = data_reset.rename(columns={'date': 'ano'})
                
                # Converter data para ano
                if hasattr(data_reset['ano'].iloc[0], 'year'):
                    data_reset['ano'] = data_reset['ano'].dt.year
                elif isinstance(data_reset['ano'].iloc[0], str):
                    data_reset['ano'] = pd.to_datetime(data_reset['ano']).dt.year
                
                # Garantir que ano seja inteiro
                data_reset['ano'] = data_reset['ano'].astype(int)
                
                # Filtrar por período
                data_filtered = data_reset[
                    (data_reset['ano'] >= self.start_year) & 
                    (data_reset['ano'] <= self.end_year)
                ].copy()
                
                logger.info(
                    f"OK - {indicator_name}: {len(data_filtered)} registros"
                )
                self.successful_indicators.append(
                    (indicator_code, indicator_name, len(data_filtered))
                )
                return data_filtered
                
            except Exception as e:
                logger.warning(
                    f"Tentativa {attempt + 1} falhou para {indicator_code}: {str(e)}"
                )
                if attempt < 1:
                    time.sleep(1)
                else:
                    logger.error(f"ERRO FINAL para {indicator_code}: {str(e)}")
                    self.failed_indicators.append(
                        (indicator_code, indicator_name, str(e))
                    )
                    return pd.DataFrame()
        
        return pd.DataFrame()
    
    def fetch_all_indicators(
        self, 
        indicators: Dict[str, str]
    ) -> Dict[str, pd.DataFrame]:
        """
        Busca todos os indicadores sequencialmente
        
        Args:
            indicators: Dicionário com códigos e nomes dos indicadores
            
        Returns:
            Dicionário com DataFrames de cada indicador
        """
        logger.info(
            "Iniciando busca SEQUENCIAL de indicadores "
            "(evita problemas de threading)"
        )
        all_data = {}
        
        total_indicators = len(indicators)
        for i, (code, name) in enumerate(indicators.items(), 1):
            logger.info(f"[{i}/{total_indicators}] Processando {name}")
            all_data[name] = self.fetch_single_indicator(code, name)
            time.sleep(API_DELAY_BETWEEN_REQUESTS)
        
        return all_data
    
    def get_extraction_summary(self) -> Dict:
        """
        Retorna resumo da extração
        
        Returns:
            Dicionário com estatísticas da extração
        """
        return {
            "successful_count": len(self.successful_indicators),
            "failed_count": len(self.failed_indicators),
            "successful_indicators": self.successful_indicators,
            "failed_indicators": self.failed_indicators
        }
