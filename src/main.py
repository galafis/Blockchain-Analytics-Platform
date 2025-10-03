
import argparse
import logging
import yaml
from src.blockchain_analyzer import BlockchainAnalyzer, APIError
from src.portfolio_tracker import PortfolioTracker
from src.visualizer import DataVisualizer

# Configuração de logging profissional
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_config(config_path: str = 'config.yaml') -> dict:
    """Carrega configurações do arquivo YAML."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Arquivo de configuração {config_path} não encontrado.")
        return {}
    except Exception as e:
        logger.error(f"Erro ao carregar configuração: {e}")
        return {}

def main():
    """Função principal de execução da plataforma de análise de blockchain."""
    parser = argparse.ArgumentParser(description="Blockchain Analytics Platform")
    parser.add_argument('--config', type=str, default='config.yaml', help='Caminho para o arquivo de configuração YAML')
    parser.add_argument('--network', type=str, default='ethereum', help='Rede blockchain a ser analisada (ex: ethereum)')
    parser.add_argument('--address', type=str, help='Endereço blockchain para análise')
    parser.add_argument('--tx', type=str, help='Hash de transação para análise')
    parser.add_argument('--action', type=str, choices=['analyze_tx', 'analyze_address', 'track_portfolio', 'visualize_data'], help='Ação a ser executada')

    args = parser.parse_args()

    config = load_config(args.config)
    api_key = config.get('api_settings', {}).get('etherscan_api_key')

    try:
        analyzer = BlockchainAnalyzer(network=args.network, api_key=api_key)

        if args.action == 'analyze_tx' and args.tx:
            print(f"\n--- Análise de Transação: {args.tx} ---")
            transaction_data = analyzer.get_transaction(args.tx)
            if transaction_data:
                transaction = analyzer.Transaction(transaction_data)
                print(f"Hash: {transaction.hash}")
                print(f"De: {transaction.from_address}")
                print(f"Para: {transaction.to_address}")
                print(f"Valor: {transaction.value} ETH")
                print(f"Timestamp: {transaction.timestamp}")
                print(f"Status: {transaction.status}")
                print(f"Bloco: {transaction.block_number}")
                print(f"Gás Usado: {transaction.gas_used}")
                print(f"Preço do Gás: {transaction.gas_price}")
            else:
                print(f"Transação {args.tx} não encontrada ou erro na API.")

        elif args.action == 'analyze_address' and args.address:
            print(f"\n--- Análise de Endereço: {args.address} ---")
            if analyzer.validate_address(args.address):
                balance = analyzer.get_balance(args.address)
                print(f"Saldo: {balance} ETH")
                history = analyzer.get_address_history(args.address)
                print(f"Total de transações nos últimos 10000 blocos: {len(history)}")
                if history:
                    print("Últimas 5 transações:")
                    for tx_data in history[:5]:
                        tx = analyzer.Transaction(tx_data)
                        print(f"  - Hash: {tx.hash[:10]}..., Valor: {tx.value} ETH, De: {tx.from_address[:10]}..., Para: {tx.to_address[:10]}...")
                else:
                    print("Nenhuma transação encontrada para este endereço.")
            else:
                print(f"Endereço {args.address} inválido para a rede {args.network}.")

        elif args.action == 'track_portfolio':
            print("\n--- Rastreamento de Portfólio ---")
            tracker = PortfolioTracker(analyzer)
            # Exemplo: Adicionar alguns endereços para rastreamento
            # Estes endereços são apenas para demonstração e podem não ter transações reais
            tracker.add_address('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb') # Exemplo de endereço Ethereum
            tracker.add_address('0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B') # Exemplo de endereço Ethereum
            
            portfolio_summary = tracker.get_portfolio_summary()
            print("Resumo do Portfólio:")
            for address, data in portfolio_summary.items():
                print(f"  Endereço: {address}")
                print(f"    Saldo: {data['balance']} ETH")
                print(f"    Total de Transações: {data['tx_count']}")

        elif args.action == 'visualize_data':
            print("\n--- Visualização de Dados ---")
            visualizer = DataVisualizer(analyzer)
            # Exemplo de visualização (pode precisar de dados reais ou mockados)
            # Para um exemplo funcional, precisaríamos de dados históricos de preços
            # ou de transações de um endereço específico.
            print("Gerando visualização de exemplo (requer dados)...")
            # Para demonstrar, vamos gerar um gráfico simples de um endereço mockado
            mock_address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
            history = analyzer.get_address_history(mock_address)
            if history:
                visualizer.plot_transaction_volume(history, 'transaction_volume.png')
                print("Gráfico de volume de transações gerado: transaction_volume.png")
            else:
                print("Não foi possível gerar visualização: Sem dados de transação para o endereço mockado.")

        else:
            parser.print_help()

    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
    except APIError as e:
        logger.error(f"Erro na API: {e}")
    except ConnectionError as e:
        logger.error(f"Erro de conexão: {e}")
    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()

