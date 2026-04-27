"""
Módulo de Logging
Configuração centralizada do sistema de logs
"""

import logging
import sys
from typing import Optional
from src.config import LOG_FILE, LOG_FORMAT, LOG_LEVEL


class WindowsFileHandler(logging.FileHandler):
    """Handler customizado para compatibilidade com Windows"""
    def __init__(self, filename, mode='a', encoding='utf-8', delay=False):
        super().__init__(filename, mode, encoding, delay)


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Configura e retorna um logger
    
    Args:
        name: Nome do logger (opcional)
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name or __name__)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Handler para arquivo
    file_handler = WindowsFileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Logger padrão do módulo
logger = setup_logger('worldbank_extractor')
