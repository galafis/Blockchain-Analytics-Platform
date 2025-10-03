
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import pandas as pd
import logging

# Configurar o logger para capturar mensagens durante o teste
logging.getLogger("src.advanced_analytics").setLevel(logging.ERROR)
logging.getLogger("src.advanced_analytics").propagate = True



from sklearn.ensemble import IsolationForest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.advanced_analytics import PatternAnalyzer

class TestPatternAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = PatternAnalyzer(contamination=0.05)

    def test_initialization(self):
        self.assertIsInstance(self.analyzer.model, IsolationForest)
        self.assertEqual(self.analyzer.model.contamination, 0.05)

    def test_detect_anomalies_no_data(self):
        anomalies = self.analyzer.detect_anomalies([])
        self.assertEqual(len(anomalies), 0)

    def test_detect_anomalies_success(self):
        data = [
            {"value": 10, "gas_used": 21000, "block_number": 100},
            {"value": 12, "gas_used": 22000, "block_number": 101},
            {"value": 1000, "gas_used": 500000, "block_number": 102}, # Anomaly
            {"value": 11, "gas_used": 21500, "block_number": 103},
            {"value": 9, "gas_used": 20000, "block_number": 104},
        ]
        anomalies = self.analyzer.detect_anomalies(data)
        self.assertGreater(len(anomalies), 0)
        self.assertEqual(anomalies[0]["value"], 1000)
        self.assertEqual(anomalies[0]["anomaly_type"], "Comportamento Incomum")

    def test_detect_anomalies_specific_features(self):
        data = [
            {"value": 10, "gas_used": 21000, "other_feature": 1},
            {"value": 12, "gas_used": 22000, "other_feature": 2},
            {"value": 1000, "gas_used": 21000, "other_feature": 3}, # Anomaly based on value
        ]
        anomalies = self.analyzer.detect_anomalies(data, features=["value"])
        self.assertGreater(len(anomalies), 0)
        self.assertEqual(anomalies[0]["value"], 1000)

    def test_detect_anomalies_no_numeric_features(self):
        data = [
            {"feature_str": "a", "feature_bool": True},
            {"feature_str": "b", "feature_bool": False},
        ]
        with self.assertLogs("src.advanced_analytics", level="ERROR") as cm:
            anomalies = self.analyzer.detect_anomalies(data, features=["feature_str", "feature_bool"])
            self.assertEqual(len(anomalies), 0)
            self.assertIn("Nenhuma das features selecionadas é numérica. Não é possível detectar anomalias.", cm.output[0])


if __name__ == "__main__":
    unittest.main()

