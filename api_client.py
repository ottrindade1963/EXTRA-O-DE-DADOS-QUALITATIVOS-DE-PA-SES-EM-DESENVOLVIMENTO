"""
Módulo de Cliente API
Gerencia todas as interações com a API do Banco Mundial
"""

import requests
import time
from typing import List, Dict, Optional
from src.config import (
    API_BASE_URL, 
    API_TIMEOUT, 
    API_RETRY_ATTEMPTS,
    EXCLUDED_INCOME_LEVELS,
    EXCLUDED_REGIONS,
    EXCLUDED_COUNTRY_CODES,
    FALLBACK_COUNTRIES
)
from src.logger import logger


class WorldBankAPIClient:
    """Cliente para interagir com a API do Banco Mundial"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.retry_attempts = API_RETRY_ATTEMPTS
    
    def get_developing_countries(self) -> List[str]:
        """
        Obtém lista de países em desenvolvimento do Banco Mundial
        
        Returns:
            Lista de códigos de países (ISO 3166-1 alpha-3)
        """
        logger.info("Obtendo lista de países em desenvolvimento do Banco Mundial")
        
        try:
            url = f"{self.base_url}/country?format=json&per_page=300"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if len(data) < 2 or not data[1]:
                logger.error("Resposta da API não contém dados esperados")
                return self._get_fallback_countries()
            
            developing_countries = []
            
            for country in data[1]:
                income_level = country.get('incomeLevel', {})
                region = country.get('region', {})
                country_id = country.get('id', '')
                
                # Filtrar países de alta renda e regiões agregadas
                if (income_level.get('id') not in EXCLUDED_INCOME_LEVELS and 
                    region.get('id') not in EXCLUDED_REGIONS and 
                    country_id not in EXCLUDED_COUNTRY_CODES and
                    len(country_id) == 3):  # Códigos de país têm 3 caracteres
                    developing_countries.append(country_id)
            
            logger.info(f"Encontrados {len(developing_countries)} países em desenvolvimento")
            return developing_countries
            
        except Exception as e:
            logger.error(f"Erro ao obter lista de países: {str(e)}")
            return self._get_fallback_countries()
    
    def _get_fallback_countries(self) -> List[str]:
        """
        Retorna lista de fallback de países em desenvolvimento
        
        Returns:
            Lista de códigos de países
        """
        logger.info(f"Usando lista de fallback com {len(FALLBACK_COUNTRIES)} países")
        return FALLBACK_COUNTRIES
    
    def get_indicator_metadata(self, indicator_code: str) -> Dict:
        """
        Obtém metadados de um indicador específico
        
        Args:
            indicator_code: Código do indicador do Banco Mundial
            
        Returns:
            Dicionário com metadados do indicador
        """
        for attempt in range(self.retry_attempts):
            try:
                url = f"{self.base_url}/indicator/{indicator_code}?format=json"
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                if data and len(data) > 1 and data[1]:
                    ind = data[1][0]
                    return {
                        "id": ind.get("id"),
                        "name": ind.get("name"),
                        "source_organization": ind.get("sourceOrganization"),
                        "source_note": ind.get("sourceNote"),
                        "unit": ind.get("unit", ""),
                        "source": ind.get("source", {}).get("value", "")
                    }
                return {}
                
            except Exception as e:
                logger.warning(
                    f"Tentativa {attempt + 1} falhou ao obter metadados "
                    f"para {indicator_code}: {str(e)}"
                )
                if attempt < self.retry_attempts - 1:
                    time.sleep(1)
                else:
                    logger.error(f"Erro final ao obter metadados para {indicator_code}")
                    return {}
        
        return {}
    
    def get_all_indicators_metadata(self, indicators: Dict[str, str]) -> Dict[str, Dict]:
        """
        Obtém metadados de todos os indicadores
        
        Args:
            indicators: Dicionário com códigos e nomes dos indicadores
            
        Returns:
            Dicionário com metadados de todos os indicadores
        """
        logger.info(f"Obtendo metadados de {len(indicators)} indicadores")
        metadata = {}
        
        for code, name in indicators.items():
            metadata[code] = self.get_indicator_metadata(code)
            time.sleep(0.2)  # Evitar sobrecarga da API
        
        logger.info(f"Metadados obtidos para {len(metadata)} indicadores")
        return metadata
