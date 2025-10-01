"""
Blockchain-Analytics-Platform - Pacote Principal (src)
-----------------------------------------------------

Este pacote organiza os módulos principais da Blockchain Analytics Platform.
O objetivo é que cada componente (análise de blockchain, rastreamento de portfolio, visualização de dados) seja desenvolvido e mantido
independentemente, seguindo princípios SOLID e facilitando testes unitários.

Uso:
----
Este arquivo permite importações simplificadas como:
    from src import BlockchainAnalyzer
    
ao invés de:
    from src.main import BlockchainAnalyzer

Autor: Gabriel Demetrios Lafis
Data: 2025
Licença: MIT
"""

# Versão do pacote seguindo Semantic Versioning (semver.org)
__version__ = "1.0.0"

# Metadados do pacote
__author__ = "Gabriel Demetrios Lafis"
__email__ = "contact@galafis.dev"
__license__ = "MIT"

# ==============================================================================
# IMPORTAÇÕES PÚBLICAS DOS MÓDULOS PRINCIPAIS
# ==============================================================================
# Importa as classes principais de cada módulo para facilitar o acesso público.
# Isso permite que usuários da biblioteca façam:
#     from src import BlockchainAnalyzer
# ao invés de:
#     from src.main import BlockchainAnalyzer

# Módulo de Análise Blockchain
# Fornece funcionalidades para análise de transações e dados on-chain
from .main import BlockchainAnalyzer

# Módulo de Rastreamento de Portfolio
# Gerencia e monitora portfolios de criptomoedas com múltiplos ativos
# from .portfolio_tracker import PortfolioTracker

# Módulo de Visualização de Dados
# Cria gráficos, dashboards e visualizações interativas
# from .visualizer import DataVisualizer

# Módulo de Analytics Avançados
# Contém ferramentas para detecção de padrões, análise de risco e predições
# from .advanced_analytics import (
#     PatternAnalyzer,
#     RiskAnalyzer,
#     PredictiveModel,
# )

# ==============================================================================
# LISTA DE EXPORTAÇÕES PÚBLICAS
# ==============================================================================
# Define explicitamente quais classes/funções são exportadas quando alguém faz:
#     from src import *
# Esta é uma boa prática que previne poluição do namespace e deixa clara a API pública.

__all__ = [
    "BlockchainAnalyzer",
    # "PortfolioTracker",
    # "DataVisualizer",
    # "PatternAnalyzer",
    # "RiskAnalyzer",
    # "PredictiveModel",
]

# ==============================================================================
# CONFIGURAÇÕES GLOBAIS DO PACOTE
# ==============================================================================
# Configurações padrão que podem ser sobrescritas por config.yaml ou variáveis de ambiente

DEFAULT_CONFIG = {
    "api_rate_limit": 5,
    "cache_enabled": True,
    "cache_ttl": 3600,
    "log_level": "INFO",
    "default_network": "ethereum",
}

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def _init_message():
    """
    Mensagem informativa exibida ao importar o pacote.
    
    Útil para debugging e uso interativo (notebooks, REPL).
    """
    return f"Blockchain Analytics Platform v{__version__} carregado com sucesso."

# ==============================================================================
# INICIALIZAÇÃO EM MODO DE DESENVOLVIMENTO
# ==============================================================================
# Apenas exibe mensagem se a variável de ambiente DEV_MODE estiver ativa

import os
if os.getenv("DEV_MODE") == "true":
    print(_init_message())

# ==============================================================================
# NOTAS PARA COLABORADORES
# ==============================================================================
# - Ao adicionar novos módulos, importe as classes principais aqui
# - Sempre atualize a lista __all__ com as novas exportações públicas
# - Mantenha os comentários explicativos para facilitar a manutenção
# - Siga o padrão de importações relativas (.modulo)
# - Documente o propósito de cada módulo importado
# ==============================================================================

