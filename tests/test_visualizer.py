
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.visualizer import DataVisualizer, ExportFormat
from src.blockchain_analyzer import BlockchainAnalyzer, Transaction # Importar Transaction real

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.mock_analyzer = MagicMock(spec=BlockchainAnalyzer)
        # Mockar a classe Transaction dentro do mock_analyzer
        self.mock_analyzer.Transaction = MagicMock(spec=Transaction)
        self.visualizer = DataVisualizer(self.mock_analyzer, theme="light")

    def test_initialization(self):
        self.assertEqual(self.visualizer.theme, "light")
        self.assertEqual(self.visualizer.figsize, (12, 6))
        self.assertEqual(self.visualizer.dpi, 100)

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_plot_price_evolution(self, mock_show, mock_savefig):
        data = pd.DataFrame({
            "timestamp": [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)],
            "price": [100, 105, 102]
        })
        cryptocurrency = "BTC"
        output_file = "test_price_evolution.png"
        
        fig = self.visualizer.plot_price_evolution(data, cryptocurrency, output=output_file)
        self.assertIsInstance(fig, plt.Figure)
        mock_savefig.assert_called_once_with(output_file, dpi=100, bbox_inches="tight")
        # mock_show.assert_not_called() # Em ambiente headless, show não deve ser chamado

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_plot_portfolio_allocation(self, mock_show, mock_savefig):
        holdings = {"ETH": 1000.0, "BTC": 500.0, "ADA": 200.0}
        output_file = "test_portfolio_allocation.png"

        fig = self.visualizer.plot_portfolio_allocation(holdings, output=output_file)
        self.assertIsInstance(fig, plt.Figure)
        mock_savefig.assert_called_once_with(output_file, dpi=100, bbox_inches="tight")

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_plot_transaction_volume(self, mock_show, mock_savefig):
        transactions_raw = [
            {"hash": "0x1", "value": "1000000000000000000", "from": "0xFrom1", "to": "0xTo1", "timeStamp": "1678886400", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123456"},
            {"hash": "0x2", "value": "500000000000000000", "from": "0xFrom2", "to": "0xTo2", "timeStamp": "1678886400", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123457"},
            {"hash": "0x3", "value": "2000000000000000000", "from": "0xFrom3", "to": "0xTo3", "timeStamp": "1678972800", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123458"}
        ]
        # Configurar o mock da classe Transaction para retornar instâncias mockadas
        self.mock_analyzer.Transaction.side_effect = lambda data: MagicMock(
            value=float(data.get('value', 0)) / (10**18),
            timestamp=datetime.fromtimestamp(int(data.get('timeStamp', 0)))
        )

        output_file = "test_transaction_volume.png"
        fig = self.visualizer.plot_transaction_volume(transactions_raw, output=output_file)
        self.assertIsInstance(fig, plt.Figure)
        mock_savefig.assert_called_once_with(output_file, dpi=100, bbox_inches="tight")

    @patch("matplotlib.pyplot.savefig")
    def test_export_figure(self, mock_savefig):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        filename = "test_export.png"
        self.visualizer.export(fig, filename, ExportFormat.PNG)
        mock_savefig.assert_called_once_with(filename, dpi=100, bbox_inches="tight")
        plt.close(fig) # Fechar a figura para evitar vazamento de memória em testes

    def test_export_figure_failure(self):
        fig = MagicMock(spec=plt.Figure)
        fig.savefig.side_effect = Exception("Save error")
        filename = "test_export_fail.png"
        self.assertFalse(self.visualizer.export(fig, filename, ExportFormat.PNG))

if __name__ == "__main__":
    unittest.main()

