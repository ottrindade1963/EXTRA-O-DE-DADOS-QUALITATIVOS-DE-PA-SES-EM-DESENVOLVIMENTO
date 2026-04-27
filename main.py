#!/usr/bin/env python3
"""
Script Principal de Extração de Dados do Banco Mundial

Este script coordena a extração de dados de indicadores de desenvolvimento
do Banco Mundial para países em desenvolvimento.

Uso:
    python main.py [--start-year YYYY] [--end-year YYYY]

Exemplos:
    python main.py
    python main.py --start-year 2010 --end-year 2023
"""

import sys
import os
import argparse
import warnings

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Suprimir warnings desnecessários
warnings.filterwarnings('ignore')

from src.config import DEFAULT_START_YEAR, DEFAULT_END_YEAR
from src.orchestrator import WorldBankOrchestrator
from src.logger import logger


def parse_arguments():
    """
    Processa argumentos da linha de comando
    
    Returns:
        Namespace com os argumentos processados
    """
    parser = argparse.ArgumentParser(
        description='Extrator de Dados do Banco Mundial',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py
  python main.py --start-year 2010 --end-year 2023
  python main.py -s 2015 -e 2020

O script irá:
  1. Obter lista de países em desenvolvimento
  2. Extrair indicadores de desenvolvimento
  3. Processar e limpar os dados
  4. Exportar em formatos CSV e Excel
  5. Gerar relatórios de execução
        """
    )
    
    parser.add_argument(
        '--start-year', '-s',
        type=int,
        default=DEFAULT_START_YEAR,
        help=f'Ano inicial (padrão: {DEFAULT_START_YEAR})'
    )
    
    parser.add_argument(
        '--end-year', '-e',
        type=int,
        default=DEFAULT_END_YEAR,
        help=f'Ano final (padrão: {DEFAULT_END_YEAR})'
    )
    
    return parser.parse_args()


def validate_years(start_year: int, end_year: int) -> bool:
    """
    Valida os anos fornecidos
    
    Args:
        start_year: Ano inicial
        end_year: Ano final
        
    Returns:
        True se válido, False caso contrário
    """
    if start_year > end_year:
        logger.error("Ano inicial não pode ser maior que ano final")
        return False
    
    if start_year < 1960:
        logger.error("Ano inicial não pode ser anterior a 1960")
        return False
    
    if end_year > 2030:
        logger.error("Ano final não pode ser posterior a 2030")
        return False
    
    return True


def main():
    """Função principal"""
    try:
        # Processar argumentos
        args = parse_arguments()
        
        # Validar anos
        if not validate_years(args.start_year, args.end_year):
            sys.exit(1)
        
        # Exibir configurações
        logger.info("=" * 60)
        logger.info("CONFIGURAÇÕES")
        logger.info("=" * 60)
        logger.info(f"Ano inicial: {args.start_year}")
        logger.info(f"Ano final: {args.end_year}")
        logger.info(f"Modo: Sequencial (evita problemas de threading)")
        logger.info("=" * 60)
        
        # Criar orquestrador e executar
        orchestrator = WorldBankOrchestrator(args.start_year, args.end_year)
        data = orchestrator.run()
        
        # Verificar se há dados
        if not data or all(df.empty for df in data.values()):
            logger.error("NENHUM DADO FOI EXTRAÍDO")
            sys.exit(1)
        
        logger.info("PROCESSO CONCLUÍDO COM SUCESSO!")
        sys.exit(0)
        
    except KeyboardInterrupt:
        logger.warning("\nProcesso interrompido pelo usuário")
        sys.exit(130)
        
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
