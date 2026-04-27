"""
Módulo de Exportação de Dados
Responsável por salvar os dados em diversos formatos
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List
from src.config import DATA_DIR
from src.logger import logger


class DataExporter:
    """Exportador de dados para múltiplos formatos"""
    
    def __init__(self, start_year: int, end_year: int):
        """
        Inicializa o exportador
        
        Args:
            start_year: Ano inicial do período
            end_year: Ano final do período
        """
        self.start_year = start_year
        self.end_year = end_year
        self.data_directory = DATA_DIR
        self.saved_files: List[str] = []
    
    def save_individual_indicators(self, data: Dict[str, pd.DataFrame]) -> None:
        """
        Salva cada indicador em arquivos separados (CSV e Excel)
        
        Args:
            data: Dicionário com DataFrames de cada indicador
        """
        logger.info("Salvando indicadores individuais")
        
        for name, df in data.items():
            if df.empty:
                continue
            
            try:
                base = os.path.join(
                    self.data_directory, 
                    f"{name}_{self.start_year}_{self.end_year}"
                )
                
                # Salvar CSV
                csv_file = f"{base}.csv"
                df.to_csv(csv_file, index=False, encoding='utf-8')
                self.saved_files.append(csv_file)
                
                # Salvar Excel
                xlsx_file = f"{base}.xlsx"
                df.to_excel(xlsx_file, index=False, engine='openpyxl')
                self.saved_files.append(xlsx_file)
                
                logger.info(f"Salvo: {name}")
                
            except Exception as e:
                logger.error(f"Erro ao salvar {name}: {str(e)}")
    
    def save_consolidated_dataset(self, consolidated: pd.DataFrame) -> None:
        """
        Salva o dataset consolidado
        
        Args:
            consolidated: DataFrame consolidado
        """
        if consolidated.empty:
            logger.warning("Dataset consolidado vazio, não será salvo")
            return
        
        logger.info("Salvando dataset consolidado")
        
        try:
            base = os.path.join(
                self.data_directory,
                f"consolidated_dataset_{self.start_year}_{self.end_year}"
            )
            
            # CSV
            csv_file = f"{base}.csv"
            consolidated.to_csv(csv_file, index=False, encoding='utf-8')
            self.saved_files.append(csv_file)
            
            # Excel
            xlsx_file = f"{base}.xlsx"
            consolidated.to_excel(xlsx_file, index=False, engine='openpyxl')
            self.saved_files.append(xlsx_file)
            
            logger.info(
                f"Dataset consolidado salvo: {len(consolidated)} registros"
            )
            
        except Exception as e:
            logger.error(f"Erro ao salvar dataset consolidado: {str(e)}")
    
    def save_metadata(self, metadata: Dict[str, Dict]) -> None:
        """
        Salva metadados dos indicadores
        
        Args:
            metadata: Dicionário com metadados dos indicadores
        """
        logger.info("Salvando metadados")
        
        try:
            meta_file = os.path.join(
                self.data_directory,
                f"metadata_{self.start_year}_{self.end_year}.json"
            )
            
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            self.saved_files.append(meta_file)
            logger.info("Metadados salvos com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao salvar metadados: {str(e)}")
    
    def save_execution_report(
        self, 
        extraction_summary: Dict,
        data_stats: Dict,
        countries_count: int
    ) -> None:
        """
        Salva relatório de execução
        
        Args:
            extraction_summary: Resumo da extração
            data_stats: Estatísticas dos dados
            countries_count: Número de países processados
        """
        logger.info("Salvando relatório de execução")
        
        try:
            report = {
                "execution_time": datetime.now().isoformat(),
                "period": f"{self.start_year}-{self.end_year}",
                "countries_count": countries_count,
                "indicators_total": (
                    extraction_summary["successful_count"] + 
                    extraction_summary["failed_count"]
                ),
                "indicators_successful": extraction_summary["successful_count"],
                "indicators_failed": extraction_summary["failed_count"],
                "successful_indicators": extraction_summary["successful_indicators"],
                "failed_indicators": extraction_summary["failed_indicators"],
                "data_statistics": data_stats,
                "files_generated": self.saved_files
            }
            
            report_file = os.path.join(
                self.data_directory,
                f"execution_report_{self.start_year}_{self.end_year}.json"
            )
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logger.info("Relatório de execução salvo com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {str(e)}")
    
    def get_saved_files(self) -> List[str]:
        """
        Retorna lista de arquivos salvos
        
        Returns:
            Lista de caminhos dos arquivos salvos
        """
        return self.saved_files
