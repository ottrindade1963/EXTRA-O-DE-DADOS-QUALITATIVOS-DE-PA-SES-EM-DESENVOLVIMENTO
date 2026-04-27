"""
Módulo de Processamento de Dados
Responsável por limpar, validar e consolidar os dados extraídos
"""

import pandas as pd
from typing import Dict
from src.logger import logger


class DataProcessor:
    """Processador de dados do Banco Mundial"""
    
    @staticmethod
    def clean_data(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Limpa e valida os dados extraídos
        
        Args:
            data: Dicionário com DataFrames de cada indicador
            
        Returns:
            Dicionário com DataFrames limpos
        """
        logger.info("Iniciando limpeza de dados")
        cleaned = {}
        
        for name, df in data.items():
            if df.empty:
                continue
            
            try:
                # Criar cópia
                df_clean = df.copy()
                
                # Remover valores nulos na coluna principal
                main_column = [
                    col for col in df_clean.columns 
                    if col not in ['country', 'ano']
                ][0]
                df_clean = df_clean.dropna(subset=[main_column])
                
                if df_clean.empty:
                    logger.warning(f"Sem dados após limpeza: {name}")
                    continue
                
                # Garantir tipos corretos
                df_clean['ano'] = df_clean['ano'].astype(int)
                df_clean['country'] = df_clean['country'].astype(str)
                
                # Ordenar e remover duplicatas
                df_clean = df_clean.sort_values(['country', 'ano'])
                df_clean = df_clean.drop_duplicates(subset=['country', 'ano'])
                
                cleaned[name] = df_clean
                logger.info(f"Limpo: {name} ({len(df_clean)} registros)")
                
            except Exception as e:
                logger.error(f"Erro ao limpar {name}: {str(e)}")
        
        logger.info(f"Limpeza concluída: {len(cleaned)} indicadores")
        return cleaned
    
    @staticmethod
    def consolidate_data(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Consolida todos os indicadores em um único DataFrame
        
        Args:
            data: Dicionário com DataFrames de cada indicador
            
        Returns:
            DataFrame consolidado com todos os indicadores
        """
        logger.info("Consolidando dados")
        
        dfs = [df for df in data.values() if not df.empty]
        
        if not dfs:
            logger.error("Nenhum dado para consolidar")
            return pd.DataFrame()
        
        try:
            # Começar com o primeiro DataFrame
            consolidated = dfs[0].copy()
            
            # Fazer merge com os demais
            for df in dfs[1:]:
                consolidated = pd.merge(
                    consolidated, 
                    df, 
                    on=['country', 'ano'], 
                    how='outer'
                )
            
            logger.info(
                f"Dataset consolidado criado: {len(consolidated)} registros, "
                f"{len(consolidated.columns)} colunas"
            )
            return consolidated
            
        except Exception as e:
            logger.error(f"Erro ao consolidar dados: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def get_data_statistics(data: Dict[str, pd.DataFrame]) -> Dict:
        """
        Calcula estatísticas dos dados
        
        Args:
            data: Dicionário com DataFrames de cada indicador
            
        Returns:
            Dicionário com estatísticas
        """
        stats = {
            "total_indicators": len(data),
            "non_empty_indicators": sum(1 for df in data.values() if not df.empty),
            "total_records": sum(len(df) for df in data.values()),
            "indicators_details": {}
        }
        
        for name, df in data.items():
            if not df.empty:
                stats["indicators_details"][name] = {
                    "records": len(df),
                    "countries": df['country'].nunique(),
                    "years": df['ano'].nunique(),
                    "missing_values": df.isnull().sum().sum()
                }
        
        return stats
