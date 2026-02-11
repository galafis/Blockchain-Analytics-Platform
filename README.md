# Blockchain Analytics Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

![Hero Image](docs/hero_image.png)

## Visão Geral (Português)

Esta plataforma de análise de blockchain é uma ferramenta robusta e extensível projetada para interagir com redes blockchain (atualmente Ethereum via Etherscan API), coletar dados, analisar transações e endereços, e visualizar informações de forma intuitiva. O objetivo é fornecer insights valiosos sobre atividades on-chain, detecção de anomalias e rastreamento de portfólio.

### Funcionalidades Principais

- **Análise de Blockchain (`BlockchainAnalyzer`):**
    - Conexão com APIs de blockchain (Etherscan).
    - Validação de endereços e hashes de transação.
    - Obtenção de saldos de endereços.
    - Recuperação do histórico de transações.
- **Rastreador de Portfólio (`PortfolioTracker`):**
    - Gerenciamento de múltiplos endereços e redes.
    - Sumarização de portfólios.
    - Cálculo de ganhos/perdas.
- **Análise Avançada (`PatternAnalyzer`, `RiskAnalyzer`, `PredictiveModel`):**
    - Detecção de anomalias em padrões de transação.
    - Análise de risco (volatilidade, Sharpe ratio, VaR).
    - Modelos preditivos básicos para forecasting.
- **Visualização de Dados (`DataVisualizer`):**
    - Geração de gráficos de evolução de preços, alocação de portfólio e volume de transações.
    - Suporte a diferentes temas visuais (claro/escuro).

### Instalação

1.  **Clonar o repositório:**
    ```bash
    git clone https://github.com/galafis/Blockchain-Analytics-Platform.git
    cd Blockchain-Analytics-Platform
    ```

2.  **Criar e ativar um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate   # Windows
    ```

3.  **Instalar dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração da API:**
    Crie um arquivo `config.yaml` na raiz do projeto com sua chave de API do Etherscan:
    ```yaml
    api_settings:
      etherscan_api_key: "SUA_CHAVE_API_ETHERSCAN"
      rate_limit: 5 # Requisições por segundo
    analysis:
      cache_ttl: 3600 # Tempo de vida do cache em segundos
    ```
    Obtenha sua chave de API em [Etherscan API](https://etherscan.io/apis).

### Uso

Exemplo de uso básico:

```python
import yaml
from src.blockchain_analyzer import BlockchainAnalyzer
from src.portfolio_tracker import PortfolioTracker
from src.visualizer import DataVisualizer
from src.advanced_analytics import PatternAnalyzer

# Carregar configurações da API
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
etherscan_api_key = config["api_settings"]["etherscan_api_key"]

# Inicializar o analisador
analyzer = BlockchainAnalyzer(network="ethereum", api_key=etherscan_api_key)

# Exemplo: Obter saldo de um endereço
address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
if analyzer.validate_address(address):
    balance = analyzer.get_balance(address)
    print(f"Saldo de {address}: {balance} ETH")

    # Exemplo: Obter histórico de transações
    history = analyzer.get_address_history(address)
    print(f"Total de transações: {len(history)}")

    # Exemplo: Rastrear portfólio
    tracker = PortfolioTracker(analyzer)
    tracker.add_address(address, "ethereum")
    summary = tracker.get_portfolio_summary()
    print("Sumário do Portfólio:", summary)

    # Exemplo: Visualização
    visualizer = DataVisualizer(analyzer)
    # Supondo que você tenha dados de preço e transações para plotar
    # price_data = pd.DataFrame(...)
    # visualizer.plot_price_evolution(price_data, "ETH", output="eth_price.png")
    # visualizer.plot_portfolio_allocation(summary["holdings"], output="portfolio_allocation.png")

    # Exemplo: Detecção de anomalias
    pattern_analyzer = PatternAnalyzer()
    # anomalies = pattern_analyzer.detect_anomalies(history, features=["value", "gasUsed"])
    # print(f"Anomalias detectadas: {len(anomalies)}")
else:
    print(f"Endereço inválido: {address}")
```

## Overview (English)

This blockchain analytics platform is a robust and extensible tool designed to interact with blockchain networks (currently Ethereum via Etherscan API), collect data, analyze transactions and addresses, and visualize information intuitively. The goal is to provide valuable insights into on-chain activities, anomaly detection, and portfolio tracking.

### Key Features

-   **Blockchain Analysis (`BlockchainAnalyzer`):**
    -   Connection with blockchain APIs (Etherscan).
    -   Validation of addresses and transaction hashes.
    -   Retrieval of address balances.
    -   Retrieval of transaction history.
-   **Portfolio Tracker (`PortfolioTracker`):**
    -   Management of multiple addresses and networks.
    -   Portfolio summarization.
    -   Calculation of gains/losses.
-   **Advanced Analytics (`PatternAnalyzer`, `RiskAnalyzer`, `PredictiveModel`):**
    -   Anomaly detection in transaction patterns.
    -   Risk analysis (volatility, Sharpe ratio, VaR).
    -   Basic predictive models for forecasting.
-   **Data Visualization (`DataVisualizer`):**
    -   Generation of price evolution, portfolio allocation, and transaction volume charts.
    -   Support for different visual themes (light/dark).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/galafis/Blockchain-Analytics-Platform.git
    cd Blockchain-Analytics-Platform
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate   # Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Configuration:**
    Create a `config.yaml` file in the project root with your Etherscan API key:
    ```yaml
    api_settings:
      etherscan_api_key: "YOUR_ETHERSCAN_API_KEY"
      rate_limit: 5 # Requests per second
    analysis:
      cache_ttl: 3600 # Cache time-to-live in seconds
    ```
    Get your API key from [Etherscan API](https://etherscan.io/apis).

### Usage

Basic usage example:

```python
import yaml
from src.blockchain_analyzer import BlockchainAnalyzer
from src.portfolio_tracker import PortfolioTracker
from src.visualizer import DataVisualizer
from src.advanced_analytics import PatternAnalyzer

# Load API configurations
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
etherscan_api_key = config["api_settings"]["etherscan_api_key"]

# Initialize the analyzer
analyzer = BlockchainAnalyzer(network="ethereum", api_key=etherscan_api_key)

# Example: Get address balance
address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
if analyzer.validate_address(address):
    balance = analyzer.get_balance(address)
    print(f"Balance of {address}: {balance} ETH")

    # Example: Get transaction history
    history = analyzer.get_address_history(address)
    print(f"Total transactions: {len(history)}")

    # Example: Track portfolio
    tracker = PortfolioTracker(analyzer)
    tracker.add_address(address, "ethereum")
    summary = tracker.get_portfolio_summary()
    print("Portfolio Summary:", summary)

    # Example: Visualization
    visualizer = DataVisualizer(analyzer)
    # Assuming you have price and transaction data to plot
    # price_data = pd.DataFrame(...)
    # visualizer.plot_price_evolution(price_data, "ETH", output="eth_price.png")
    # visualizer.plot_portfolio_allocation(summary["holdings"], output="portfolio_allocation.png")

    # Example: Anomaly detection
    pattern_analyzer = PatternAnalyzer()
    # anomalies = pattern_analyzer.detect_anomalies(history, features=["value", "gasUsed"])
    # print(f"Detected anomalies: {len(anomalies)}")
else:
    print(f"Invalid address: {address}")
```
