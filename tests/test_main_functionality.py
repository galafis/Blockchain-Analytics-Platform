import unittest
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.main import BlockchainAnalyzer

class TestBlockchainAnalyzerFunctionality(unittest.TestCase):

    def setUp(self):
        self.analyzer = BlockchainAnalyzer()
        self.analyzer.load_data() # Load sample data for tests
        self.output_file = 'blockchain_analytics_platform_analysis.png'
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_load_data(self):
        self.assertIsNotNone(self.analyzer.data)
        self.assertIsInstance(self.analyzer.data, pd.DataFrame)
        self.assertGreater(len(self.analyzer.data), 0)

    def test_analyze(self):
        results = self.analyzer.analyze()
        self.assertIn('statistics', results)
        self.assertIn('classification_report', results)
        self.assertIsNotNone(self.analyzer.model)

    def test_visualize(self):
        # This test primarily checks if the visualize method runs without errors
        # and creates a file. Actual visual content is harder to test programmatically.
        try:
            self.analyzer.visualize()
            self.assertTrue(os.path.exists(self.output_file))
        except Exception as e:
            self.fail(f"Visualização falhou com erro: {e}")

if __name__ == '__main__':
    unittest.main()

