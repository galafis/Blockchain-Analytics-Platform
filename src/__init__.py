"""
Blockchain Analytics Platform - Source Package
===============================================

Este módulo inicializa o pacote principal da Blockchain Analytics Platform.

Propósito:
----------
O arquivo __init__.py transforma o diretório 'src' em um pacote Python válido,
permitindo importações organizadas e modularização adequada do código. Este é um
padrão fundamental em projetos Python profissionais que garante a estrutura correta
do namespace e facilita a distribuição do código.

Funcionalidades:
----------------
- Marca o diretório como um pacote Python importável
- Define quais módulos e classes são expostos publicamente via __all__
- Configura importações convenientes para facilitar o uso da API
- Centraliza configurações e metadados do pacote

Arquitetura:
------------
A estrutura modular permite que cada componente da plataforma (análise de blockchain,
rastreamento de portfolio, visualização de dados) seja desenvolvido e mantido
independentemente, seguindo princípios SOLID e facilitando testes unitários.

Uso:
----
Este arquivo permite importações simplificadas como:
    from src import BlockchainAnalyzer, PortfolioTracker
    
ao invés de:
    from src.blockchain_analyzer import BlockchainAnalyzer
    from src.portfolio_tracker import PortfolioTracker

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

# Lista de módulos públicos exportados (controla o comportamento de 'from src import *')
# Esta lista será expandida conforme novos módulos forem adicionados ao projeto
__all__ = [
    # Módulos de análise
    # "BlockchainAnalyzer",
    # "TransactionTracker",
    
    # Módulos de portfolio
    # "PortfolioTracker",
    # "AssetManager",
    
    # Módulos de visualização
    # "DataVisualizer",
    # "DashboardGenerator",
    
    # Módulos de utilidades
    # "APIClient",
    # "DataProcessor",
]

# Importações futuras dos módulos principais serão adicionadas aqui
# Exemplo:
# from .blockchain_analyzer import BlockchainAnalyzer
# from .portfolio_tracker import PortfolioTracker
# from .visualizer import DataVisualizer
# from .advanced_analytics import PatternAnalyzer

# Configurações globais do pacote (podem ser sobrescritas por config.yaml)
DEFAULT_CONFIG = {
    "api_rate_limit": 5,  # requisições por segundo
    "cache_enabled": True,
    "cache_ttl": 3600,  # segundos
    "log_level": "INFO",
    "default_network": "ethereum",
}

# Mensagem de boas-vindas para imports interativos (útil em notebooks)
def _init_message():
    """Mensagem informativa exibida ao importar o pacote."""
    return f"Blockchain Analytics Platform v{__version__} carregado com sucesso."

# Inicialização opcional (apenas em modo de desenvolvimento)
import os
if os.getenv("DEV_MODE") == "true":
    print(_init_message())
