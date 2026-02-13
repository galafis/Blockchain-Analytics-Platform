
import logging
import re
import requests
import yaml
from typing import Dict, List, Optional, Any
from datetime import datetime

# Configuração de logging profissional
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class APIError(Exception):
    """Exceção personalizada para erros de API."""
    pass

class BlockchainAnalyzer:
    """
    Classe principal para análise de dados blockchain.
    
    Esta classe serve como interface unificada para interação com diferentes
    redes blockchain, abstraindo complexidades de APIs específicas e fornecendo
    uma interface consistente para o restante da aplicação.
    
    Attributes:
        network (str): Nome da rede blockchain (ethereum, bitcoin, polygon, etc.)
        api_key (str): Chave de API para autenticação
        cache_enabled (bool): Flag para habilitar/desabilitar cache
        timeout (int): Timeout para requisições em segundos
        _cache (Dict): Cache interno para otimização de consultas
        base_url (str): URL base da API do Etherscan
    
    Example:
        >>> analyzer = BlockchainAnalyzer(network='ethereum')
        >>> analyzer.validate_address('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0')
        True
    """
    
    def __init__(
        self,
        network: str = 'ethereum',
        api_key: Optional[str] = None,
        cache_enabled: bool = True,
        timeout: int = 30,
        config_path: str = 'config.yaml'
    ):
        """
        Inicializa o analisador blockchain.
        
        Args:
            network: Nome da rede blockchain a ser analisada
            api_key: Chave de API para autenticação (opcional para redes públicas)
            cache_enabled: Se True, habilita cache de consultas para performance
            timeout: Timeout em segundos para requisições HTTP
            config_path: Caminho para o arquivo de configuração YAML
        
        Raises:
            ValueError: Se a rede especificada não for suportada
            ConnectionError: Se não conseguir estabelecer conexão inicial
        """
        self.network = network.lower()
        self.api_key = api_key
        self.cache_enabled = cache_enabled
        self.timeout = timeout
        self._cache: Dict[str, Any] = {}
        self.base_url = "https://api.etherscan.io/api"

        self._load_config(config_path)
        
        if self.network == 'ethereum' and not self.api_key:
            raise ValueError("API key is required for Ethereum network.")
        
        logger.info(f"BlockchainAnalyzer inicializado para rede {self.network}")
    
    def _load_config(self, config_path: str):
        """Carrega configurações do arquivo YAML."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            self.api_key = config['api_settings'].get('etherscan_api_key', self.api_key)
            self.rate_limit = config['api_settings'].get('rate_limit', 5)
            self.cache_ttl = config['analysis'].get('cache_ttl', 3600)
        except FileNotFoundError:
            logger.warning(f"Arquivo de configuração {config_path} não encontrado. Usando valores padrão.")
        except KeyError as e:
            logger.error(f"Chave ausente no arquivo de configuração: {e}")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")

    def _make_api_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Faz uma requisição genérica à API do Etherscan."""
        params['apikey'] = self.api_key
        try:
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status() # Levanta HTTPError para códigos de status ruins (4xx ou 5xx)
            data = response.json()
            if data['status'] == '0':
                raise APIError(data['message'])
            return data['result']
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erro de conexão com a API do Etherscan: {e}")
        except APIError as e:
            raise APIError(f"Erro da API do Etherscan: {e}")
        except Exception as e:
            raise Exception(f"Erro inesperado na requisição da API: {e}")

    def get_transaction(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações detalhadas de uma transação.
        
        Args:
            tx_hash: Hash da transação a ser consultada
        
        Returns:
            Dicionário com dados da transação ou None se não encontrada
        
        Raises:
            ValueError: Se o hash fornecido for inválido
            APIError: Se houver erro na comunicação com a API
        """
        logger.info(f"Consultando transação {tx_hash}")
        if not isinstance(tx_hash, str) or not tx_hash.startswith('0x') or len(tx_hash) != 66:
            raise ValueError("Hash de transação inválido.")

        params = {
            'module': 'proxy',
            'action': 'eth_getTransactionByHash',
            'txhash': tx_hash
        }
        try:
            result = self._make_api_request(params)
            return result if result else None
        except APIError as e:
            logger.error(f"Erro ao obter transação {tx_hash}: {e}")
            return None

    def get_address_history(
        self,
        address: str,
        startblock: int = 0,
        endblock: int = 99999999,
        sort: str = 'asc'
    ) -> List[Dict[str, Any]]:
        """
        Obtém histórico de transações de um endereço.
        
        Args:
            address: Endereço blockchain a ser analisado
            startblock: Bloco inicial para a busca
            endblock: Bloco final para a busca
            sort: Ordem de classificação ('asc' ou 'desc')
        
        Returns:
            Lista de transações ordenadas cronologicamente
        
        Raises:
            ValueError: Se o endereço for inválido
        """
        logger.info(f"Obtendo histórico de {address}")
        if not self.validate_address(address):
            raise ValueError("Endereço inválido.")

        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': startblock,
            'endblock': endblock,
            'sort': sort
        }
        try:
            result = self._make_api_request(params)
            return result if result else []
        except APIError as e:
            logger.error(f"Erro ao obter histórico do endereço {address}: {e}")
            return []

    def validate_address(self, address: str) -> bool:
        """
        Valida se um endereço é válido para a rede configurada (Ethereum).
        
        Args:
            address: Endereço a ser validado
        
        Returns:
            True se o endereço for válido, False caso contrário
        """
        # Endereços Ethereum são hexadecimais, 42 caracteres de comprimento e começam com '0x'
        # Usar regex para validação mais robusta e case-insensitive
        return re.fullmatch(r"0x[0-9a-fA-F]{40}", address) is not None

    def get_balance(self, address: str) -> float:
        """
        Obtém o saldo atual de um endereço em Ether.
        
        Args:
            address: Endereço a consultar
        
        Returns:
            Saldo em Ether
        
        Raises:
            ValueError: Se o endereço for inválido
        """
        logger.info(f"Consultando saldo de {address}")
        if not self.validate_address(address):
            raise ValueError("Endereço inválido.")

        params = {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest'
        }
        try:
            result = self._make_api_request(params)
            # O saldo é retornado em Wei, precisa ser convertido para Ether
            return float(result) / (10**18) if result else 0.0
        except APIError as e:
            logger.error(f"Erro ao obter saldo do endereço {address}: {e}")
            return 0.0

    def _clear_cache(self) -> None:
        """Limpa o cache interno de consultas."""
        self._cache.clear()
        logger.info("Cache limpo")
    
    def __repr__(self) -> str:
        """Representação string do objeto para debugging."""
        return f"BlockchainAnalyzer(network='{self.network}', cache_enabled={self.cache_enabled})"


class Transaction:
    """
    Classe para representar uma transação blockchain de forma normalizada.
    
    Abstrai diferenças entre redes, fornecendo interface consistente.
    """
    
    def __init__(self, data: Dict[str, Any]):
        """
        Inicializa uma transação a partir de dados brutos.
        
        Args:
            data: Dicionário com dados da transação
        """
        self.hash = data.get('hash')
        self.from_address = data.get('from')
        self.to_address = data.get('to')
        self.value = int(data.get('value', 0)) / (10**18) # Convert Wei to Ether
        self.timestamp = datetime.fromtimestamp(int(data.get('timeStamp', 0))) if data.get('timeStamp') else None
        self.status = data.get('txreceipt_status', 'unknown') # Etherscan specific
        self.gas_used = int(data.get('gasUsed', 0))
        self.gas_price = int(data.get('gasPrice', 0))
        self.block_number = int(data.get('blockNumber', 0))

    def __repr__(self) -> str:
        return f"Transaction(hash='{self.hash}', value={self.value} ETH)"

