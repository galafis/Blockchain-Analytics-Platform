'''
Testes para portfolio_tracker.py
'''
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.portfolio_tracker import PortfolioTracker, Holding
from src.blockchain_analyzer import BlockchainAnalyzer, APIError

class TestPortfolioTracker(unittest.TestCase):

    def setUp(self):
        self.mock_analyzer = MagicMock(spec=BlockchainAnalyzer)
        self.mock_analyzer.validate_address.return_value = True
        self.mock_analyzer.get_balance.return_value = 1.5 # Exemplo de saldo
        self.mock_analyzer.get_address_history.return_value = [
            {"hash": "0x1", "value": "1000000000000000000", "from": "0xFrom1", "to": "0xTo1", "timeStamp": "1678886400", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123456"},
            {"hash": "0x2", "value": "500000000000000000", "from": "0xFrom2", "to": "0xTo2", "timeStamp": "1678886500", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123457"}
        ] # Exemplo de histórico
        self.tracker = PortfolioTracker(self.mock_analyzer)

    def test_add_address_success(self):
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        self.assertTrue(self.tracker.add_address(address, "ethereum"))
        self.assertIn(address, self.tracker._addresses["ethereum"])
        self.mock_analyzer.validate_address.assert_called_with(address)

    def test_add_address_invalid(self):
        self.mock_analyzer.validate_address.return_value = False
        address = "invalid_address"
        self.assertFalse(self.tracker.add_address(address, "ethereum"))
        self.assertNotIn("ethereum", self.tracker._addresses)

    def test_add_address_duplicate(self):
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        self.tracker.add_address(address, "ethereum")
        self.assertFalse(self.tracker.add_address(address, "ethereum"))

    def test_remove_address_success(self):
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        self.tracker.add_address(address, "ethereum")
        self.assertTrue(self.tracker.remove_address(address, "ethereum"))
        self.assertNotIn(address, self.tracker._addresses["ethereum"])

    def test_remove_address_not_found(self):
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        self.assertFalse(self.tracker.remove_address(address, "ethereum"))

    def test_list_addresses(self):
        address1 = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        address2 = "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
        self.tracker.add_address(address1, "ethereum")
        self.tracker.add_address(address2, "ethereum")

        listed = self.tracker.list_addresses()
        self.assertIn("ethereum", listed)
        self.assertIn(address1, listed["ethereum"])
        self.assertIn(address2, listed["ethereum"])

        listed_eth = self.tracker.list_addresses(network="ethereum")
        self.assertIn(address1, listed_eth["ethereum"])

    def test_get_portfolio_summary_success(self):
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        self.tracker.add_address(address, "ethereum")
        summary = self.tracker.get_portfolio_summary()

        self.assertIn(address, summary)
        self.assertEqual(summary[address]["balance"], 1.5)
        self.assertEqual(summary[address]["tx_count"], 2)
        self.assertIn("last_updated", summary[address])

    def test_get_portfolio_summary_api_error(self):
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        self.tracker.add_address(address, "ethereum")
        self.mock_analyzer.get_balance.side_effect = APIError("API Limit Exceeded")

        summary = self.tracker.get_portfolio_summary()
        self.assertIn(address, summary)
        self.assertEqual(summary[address]["balance"], 0.0)
        self.assertIn("error", summary[address])

    def test_get_transaction_history_success(self):
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        self.tracker.add_address(address, "ethereum")
        history = self.tracker.get_transaction_history(address, "ethereum")
        self.assertEqual(len(history), 2)
        self.mock_analyzer.get_address_history.assert_called_once_with(address)

    def test_get_transaction_history_invalid_address(self):
        self.mock_analyzer.validate_address.return_value = False
        address = "invalid_address"
        with self.assertRaisesRegex(ValueError, "Endereço inválido para a rede ethereum: invalid_address"):
            self.tracker.get_transaction_history(address, "ethereum")

if __name__ == "__main__":
    unittest.main()

