
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)


    class PatternAnalyzer:
        """
        Classe para detecção de anomalias em dados blockchain usando IsolationForest.

        Utiliza o algoritmo IsolationForest do scikit-learn para identificar
        transações ou atividades incomuns que podem indicar fraudes.

        Example:
            >>> analyzer = PatternAnalyzer(contamination=0.05)
            >>> anomalies = analyzer.detect_anomalies(transaction_data)
        """

        def __init__(self, contamination: float = 0.01):
            """
            Inicializa o analisador de padrões.

            Args:
                contamination: A proporção esperada de anomalias nos dados.
                               Usado pelo IsolationForest.
            """
            self.model = IsolationForest(contamination=contamination, random_state=42)
            logger.info(f"PatternAnalyzer inicializado com contamination={contamination}")

        def detect_anomalies(self, data: List[Dict[str, Any]], features: Optional[List[str]] = None) -> List[Dict[str, Any]]:
            """
            Detecta anomalias em um conjunto de dados de transações.

            Args:
                data: Lista de dicionários, onde cada dicionário representa uma transação.
                      Deve conter dados numéricos para análise.
                features: Lista de nomes das features a serem usadas para detecção.
                          Se None, tentará usar features padrão como 'value', 'gas_used', etc.

            Returns:
                Lista de dicionários representando as anomalias detectadas,
                incluindo os dados originais e um rótulo de anomalia.
            """
            if not data:
                logger.warning("Nenhum dado fornecido para detecção de anomalias.")
                return []

            df = pd.DataFrame(data)

            # Tentar inferir features se não forem fornecidas
            if features is None:
                potential_features = [col for col in ["value", "gas_used", "gas_price", "block_number"] if col in df.columns]
                if not potential_features:
                    logger.error("Nenhuma feature numérica adequada encontrada nos dados para detecção de anomalias.")
                    return []
                features = potential_features

            # Garantir que as features selecionadas são numéricas
            numeric_features = [f for f in features if pd.api.types.is_numeric_dtype(df[f])]
            if not numeric_features:
                logger.error("Nenhuma das features selecionadas é numérica. Não é possível detectar anomalias.")
                return []

            X = df[numeric_features]

            # Treinar o modelo e prever anomalias
            self.model.fit(X)
            predictions = self.model.predict(X)

            # -1 para anomalias, 1 para inliers
            anomalies_indices = df[predictions == -1].index

            anomalies_list = []
            for idx in anomalies_indices:
                anomaly_data = df.loc[idx].to_dict()
                anomaly_data["anomaly_type"] = "Comportamento Incomum"
                anomalies_list.append(anomaly_data)

            logger.info(f"Detectadas {len(anomalies_list)} anomalias.")
            return anomalies_list
