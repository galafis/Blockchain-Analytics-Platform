
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .blockchain_analyzer import BlockchainAnalyzer, APIError

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)


    @dataclass
    class Holding:
        """Representa uma posição/posse de um ativo em um endereço."""
        asset: str
        amount: float
        network: str
        address: str
        last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


    class PortfolioTracker:
        """
        Rastreador de portfolio multi-rede e multi-ativo.

        Responsável por gerenciar endereços monitorados, consolidar saldos e
        expor métricas agregadas do portfolio.

        Example:
            >>> analyzer = BlockchainAnalyzer(network='ethereum', api_key='YOUR_API_KEY')
            >>> tracker = PortfolioTracker(analyzer, base_currency='USD')
            >>> tracker.add_address('0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B', network='ethereum')
            >>> summary = tracker.get_portfolio_summary()
        """

        def __init__(self, analyzer: BlockchainAnalyzer, base_currency: str = 'USD'):
            self.analyzer = analyzer
            self.base_currency = base_currency.upper()
            self._addresses: Dict[str, List[str]] = {}  # network -> [addresses]
            self._holdings: List[Holding] = []
            logger.info("PortfolioTracker inicializado")

        def add_address(self, address: str, network: str = 'ethereum') -> bool:
            """
            Adiciona um endereço para monitoramento.

            Args:
                address: Endereço da carteira
                network: Rede blockchain (ethereum, bitcoin, polygon, etc.)

            Returns:
                True se adicionado com sucesso.
            """
            network = network.lower()
            if not self.analyzer.validate_address(address):
                logger.warning(f"Endereço inválido para a rede {network}: {address}")
                return False

            self._addresses.setdefault(network, [])
            if address in self._addresses[network]:
                logger.warning(f"Endereço já cadastrado: {address} ({network})")
                return False

            self._addresses[network].append(address)
            logger.info(f"Endereço adicionado: {address} ({network})")
            return True

        def remove_address(self, address: str, network: str = 'ethereum') -> bool:
            """Remove um endereço do monitoramento."""
            network = network.lower()
            if network not in self._addresses:
                return False
            try:
                self._addresses[network].remove(address)
                logger.info(f"Endereço removido: {address} ({network})")
                return True
            except ValueError:
                return False

        def list_addresses(self, network: Optional[str] = None) -> Dict[str, List[str]]:
            """Lista endereços cadastrados por rede."""
            if network:
                return {network: self._addresses.get(network.lower(), [])}
            return dict(self._addresses)

        def get_portfolio_summary(self) -> Dict[str, Dict[str, Any]]:
            """
            Retorna um resumo consolidado do portfolio, incluindo saldos e contagem de transações.

            Returns:
                Dicionário onde a chave é o endereço e o valor é um dicionário com 'balance' e 'tx_count'.
            """
            summary = {}
            for network, addresses in self._addresses.items():
                for address in addresses:
                    try:
                        balance = self.analyzer.get_balance(address)
                        history = self.analyzer.get_address_history(address)
                        tx_count = len(history)
                        summary[address] = {
                            'network': network,
                            'balance': balance,
                            'tx_count': tx_count,
                            'last_updated': datetime.now(timezone.utc).isoformat()
                        }
                    except (APIError, ValueError, ConnectionError) as e:
                        logger.error(f"Erro ao obter dados para o endereço {address} na rede {network}: {e}")
                        summary[address] = {
                            'network': network,
                            'balance': 0.0,
                            'tx_count': 0,
                            'error': str(e),
                            'last_updated': datetime.now(timezone.utc).isoformat()
                        }
            return summary

        def get_transaction_history(self, address: str, network: str = 'ethereum', days: int = 30) -> List[Dict[str, Any]]:
            """
            Retorna histórico de transações para um endereço específico.

            Args:
                address: Endereço blockchain a ser analisado
                network: Rede blockchain do endereço
                days: Número de dias de histórico (Etherscan não filtra por dias diretamente)

            Returns:
                Lista de transações ordenadas cronologicamente.
            """
            if not self.analyzer.validate_address(address):
                raise ValueError(f"Endereço inválido para a rede {network}: {address}")

            try:
                history = self.analyzer.get_address_history(address)
                return history
            except (APIError, ValueError, ConnectionError) as e:
                logger.error(f"Erro ao obter histórico de transações para {address} na rede {network}: {e}")
                return []
