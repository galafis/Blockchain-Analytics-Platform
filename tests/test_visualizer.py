
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import pandas as pd
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Usar backend não-interativo para testes
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.visualizer import DataVisualizer, ExportFormat
from src.blockchain_analyzer import BlockchainAnalyzer, Transaction

class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.mock_analyzer = MagicMock(spec=BlockchainAnalyzer)
        self.visualizer = DataVisualizer(self.mock_analyzer, theme="light")

    def tearDown(self):
        plt.close('all')

    def test_initialization(self):
        self.assertEqual(self.visualizer.theme, "light")
        self.assertEqual(self.visualizer.figsize, (12, 6))
        self.assertEqual(self.visualizer.dpi, 100)

    def test_plot_price_evolution(self):
        data = pd.DataFrame({
            "timestamp": [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)],
            "price": [100, 105, 102]
        })
        fig = self.visualizer.plot_price_evolution(data, "BTC")
        self.assertIsInstance(fig, plt.Figure)

    def test_plot_price_evolution_with_output(self):
        data = pd.DataFrame({
            "timestamp": [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)],
            "price": [100, 105, 102]
        })
        with patch("matplotlib.pyplot.savefig") as mock_savefig:
            fig = self.visualizer.plot_price_evolution(data, "BTC", output="test.png")
            self.assertIsInstance(fig, plt.Figure)
            mock_savefig.assert_called_once()

    def test_plot_portfolio_allocation(self):
        holdings = {"ETH": 1000.0, "BTC": 500.0, "ADA": 200.0}
        fig = self.visualizer.plot_portfolio_allocation(holdings)
        self.assertIsInstance(fig, plt.Figure)

    def test_plot_transaction_volume_empty(self):
        fig = self.visualizer.plot_transaction_volume([])
        self.assertIsInstance(fig, plt.Figure)

    def test_plot_transaction_volume(self):
        transactions_raw = [
            {"hash": "0x1", "value": "1000000000000000000", "from": "0xFrom1", "to": "0xTo1", "timeStamp": "1678886400", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123456"},
            {"hash": "0x2", "value": "500000000000000000", "from": "0xFrom2", "to": "0xTo2", "timeStamp": "1678886400", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123457"},
            {"hash": "0x3", "value": "2000000000000000000", "from": "0xFrom3", "to": "0xTo3", "timeStamp": "1678972800", "txreceipt_status": "1", "gasUsed": "21000", "gasPrice": "20000000000", "blockNumber": "123458"}
        ]
        fig = self.visualizer.plot_transaction_volume(transactions_raw)
        self.assertIsInstance(fig, plt.Figure)

    def test_export_figure_success(self):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        result = self.visualizer.export(fig, "test_export.png", ExportFormat.PNG)
        # savefig on a real Figure will succeed (writes to disk)
        self.assertTrue(result)

    def test_export_figure_failure(self):
        fig = MagicMock(spec=plt.Figure)
        fig.savefig.side_effect = Exception("Save error")
        result = self.visualizer.export(fig, "test_export_fail.png", ExportFormat.PNG)
        self.assertFalse(result)

    def test_export_formats(self):
        self.assertEqual(ExportFormat.PNG.value, 'png')
        self.assertEqual(ExportFormat.SVG.value, 'svg')
        self.assertEqual(ExportFormat.PDF.value, 'pdf')
        # HTML and JSON were removed (matplotlib doesn't support them)
        self.assertEqual(len(ExportFormat), 3)

if __name__ == "__main__":
    unittest.main()
