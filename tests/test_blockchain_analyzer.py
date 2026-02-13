import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime
import requests

# Adicionar o diretório pai ao sys.path para permitir importações relativas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.blockchain_analyzer import BlockchainAnalyzer, APIError, Transaction

class TestBlockchainAnalyzer(unittest.TestCase):

    @patch("src.blockchain_analyzer.requests.get")
    @patch("src.blockchain_analyzer.yaml.safe_load")
    def setUp(self, mock_yaml_load, mock_requests_get):
        # Mock do arquivo de configuração
        mock_yaml_load.return_value = {
            "api_settings": {
                "etherscan_api_key": "TEST_API_KEY",
                "rate_limit": 5
            },
            "analysis": {
                "cache_ttl": 3600
            }
        }
        # Mock da resposta da API para simular sucesso na inicialização
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "1", "message": "OK", "result": "1000000000000000000"}
        mock_requests_get.return_value = mock_response

        self.analyzer = BlockchainAnalyzer(network="ethereum", api_key="TEST_API_KEY", config_path="config.yaml")

    def test_initialization(self):
        self.assertEqual(self.analyzer.network, "ethereum")
        self.assertEqual(self.analyzer.api_key, "TEST_API_KEY")
        self.assertTrue(self.analyzer.cache_enabled)
        self.assertEqual(self.analyzer.timeout, 30)
        self.assertEqual(self.analyzer.base_url, "https://api.etherscan.io/api")

    def test_load_config_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertLogs("src.blockchain_analyzer", level="WARNING") as cm:
                analyzer = BlockchainAnalyzer(network="ethereum", api_key="TEST_API_KEY", config_path="non_existent_config.yaml")
                self.assertIn("Arquivo de configuração non_existent_config.yaml não encontrado", cm.output[0])

    @patch("src.blockchain_analyzer.requests.get")
    def test_make_api_request_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "1", "message": "OK", "result": "test_result"}
        mock_requests_get.return_value = mock_response

        params = {"module": "test", "action": "test"}
        result = self.analyzer._make_api_request(params)
        self.assertEqual(result, "test_result")
        mock_requests_get.assert_called_once_with(
            self.analyzer.base_url,
            params={
                "module": "test",
                "action": "test",
                "apikey": "TEST_API_KEY"
            },
            timeout=30
        )

    @patch("src.blockchain_analyzer.requests.get")
    def test_make_api_request_api_error(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "0", "message": "NOTOK", "result": "Error"}
        mock_requests_get.return_value = mock_response

        params = {"module": "test", "action": "test"}
        with self.assertRaisesRegex(APIError, "Erro da API do Etherscan: NOTOK"):
            self.analyzer._make_api_request(params)

    @patch("src.blockchain_analyzer.requests.get", side_effect=requests.exceptions.RequestException("Connection failed"))
    def test_make_api_request_connection_error(self, mock_requests_get):
        params = {"module": "test", "action": "test"}
        with self.assertRaisesRegex(ConnectionError, "Erro de conexão com a API do Etherscan: Connection failed"):
            self.analyzer._make_api_request(params)

    @patch("src.blockchain_analyzer.requests.get")
    def test_get_transaction_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "status": "1",
            "message": "OK",
            "result": {
                "hash": "0x123...abc",
                "from": "0xFromAddress",
                "to": "0xToAddress",
                "value": "1000000000000000000",
                "timeStamp": "1678886400",
                "txreceipt_status": "1",
                "gasUsed": "21000",
                "gasPrice": "20000000000",
                "blockNumber": "123456"
            }
        }
        mock_requests_get.return_value = mock_response

        tx_hash = "0x" + "a" * 64
        transaction = self.analyzer.get_transaction(tx_hash)
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction["hash"], "0x123...abc")

    def test_get_transaction_invalid_hash(self):
        with self.assertRaisesRegex(ValueError, "Hash de transação inválido."):
            self.analyzer.get_transaction("invalid_hash")
        with self.assertRaisesRegex(ValueError, "Hash de transação inválido."):
            self.analyzer.get_transaction("0x123")

    @patch("src.blockchain_analyzer.requests.get")
    def test_get_address_history_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "status": "1",
            "message": "OK",
            "result": [
                {"hash": "0x1", "value": "100", "from": "0xFrom1", "to": "0xTo1", "timeStamp": "1678886400", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123456"},
                {"hash": "0x2", "value": "200", "from": "0xFrom2", "to": "0xTo2", "timeStamp": "1678886500", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123457"}
            ]
        }
        mock_requests_get.return_value = mock_response

        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        history = self.analyzer.get_address_history(address)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["hash"], "0x1")

    def test_get_address_history_invalid_address(self):
        with self.assertRaisesRegex(ValueError, "Endereço inválido."):
            self.analyzer.get_address_history("invalid_address")

    def test_validate_address(self):
        self.assertTrue(self.analyzer.validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"))
        self.assertFalse(self.analyzer.validate_address("0x123"))
        self.assertFalse(self.analyzer.validate_address("invalid_address"))
        self.assertFalse(self.analyzer.validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbg")) # Caractere inválido
        self.assertFalse(self.analyzer.validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEBG")) # Caractere inválido maiúsculo

    @patch("src.blockchain_analyzer.requests.get")
    def test_get_balance_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "1", "message": "OK", "result": "1000000000000000000"}
        mock_requests_get.return_value = mock_response

        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"
        balance = self.analyzer.get_balance(address)
        self.assertAlmostEqual(balance, 1.0)

    def test_get_balance_invalid_address(self):
        with self.assertRaisesRegex(ValueError, "Endereço inválido."):
            self.analyzer.get_balance("invalid_address")

    def test_transaction_class(self):
        tx_data = {
            "hash": "0x123",
            "from": "0xFrom",
            "to": "0xTo",
            "value": "1000000000000000000",
            "timeStamp": "1678886400",
            "txreceipt_status": "1",
            "gasUsed": "21000",
            "gasPrice": "20000000000",
            "blockNumber": "123456"
        }
        tx = Transaction(tx_data)
        self.assertEqual(tx.hash, "0x123")
        self.assertEqual(tx.from_address, "0xFrom")
        self.assertEqual(tx.to_address, "0xTo")
        self.assertAlmostEqual(tx.value, 1.0)
        self.assertEqual(tx.timestamp, datetime.fromtimestamp(1678886400))
        self.assertEqual(tx.status, "1")
        self.assertEqual(tx.gas_used, 21000)
        self.assertEqual(tx.gas_price, 20000000000)
        self.assertEqual(tx.block_number, 123456)

if __name__ == "__main__":
    unittest.main()

