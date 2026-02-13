"""
Blockchain-Analytics-Platform - Pacote Principal (src)

Plataforma de análise de blockchain Ethereum via API Etherscan.
"""

__version__ = "1.0.0"
__author__ = "Gabriel Demetrios Lafis"
__license__ = "MIT"

from .blockchain_analyzer import BlockchainAnalyzer, Transaction, APIError
from .portfolio_tracker import PortfolioTracker, Holding
from .visualizer import DataVisualizer, ExportFormat
from .advanced_analytics import PatternAnalyzer

__all__ = [
    "BlockchainAnalyzer",
    "Transaction",
    "APIError",
    "PortfolioTracker",
    "Holding",
    "DataVisualizer",
    "ExportFormat",
    "PatternAnalyzer",
]
