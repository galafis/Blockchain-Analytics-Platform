"""
Testes para portfolio_tracker.py
--------------------------------
Estrutura mínima com pytest, fixtures básicas e testes stub/documentados.
Autor: Gabriel Demetrios Lafis
Data: 2025
Licença: MIT
"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# =========================
# Fixtures básicas
# =========================
@pytest.fixture
def carteira_vazia():
    return {"addresses": [], "fiat": "USD"}


@pytest.fixture
def carteira_com_endereco():
    return {"addresses": ["0xWallet1"], "fiat": "USD"}


# =========================
# Testes stub/documentados
# =========================
class TestPortfolioTracker:
    """Suite de testes do módulo PortfolioTracker.

    Os testes demonstram a intenção de design e serão implementados depois.
    """

    def test_init_estado_inicial(self, carteira_vazia):
        """Deve iniciar sem endereços e com moeda padrão."""
        pytest.skip("Implementar quando PortfolioTracker estiver disponível")
        # from src.portfolio_tracker import PortfolioTracker
        # tracker = PortfolioTracker(**carteira_vazia)
        # assert tracker.addresses == []
        # assert tracker.fiat == "USD"

    def test_add_address_valida_e_normaliza(self, carteira_vazia):
        """add_address deve validar e normalizar endereços antes de salvar."""
        pytest.skip("Implementar validação e normalização de endereços")

    def test_get_balance_agrega_valores(self, carteira_com_endereco):
        """get_balance deve agregar saldos por rede e converter para fiat."""
        pytest.skip("Implementar agregação de saldos e conversão cambial")

    def test_get_transaction_history_intervalo(self, carteira_com_endereco):
        """Histórico deve respeitar intervalo e ordenação cronológica."""
        pytest.skip("Implementar histórico com paginação e filtros")


@pytest.mark.integration
def test_fluxo_minimo_portfolio():
    """Fluxo: adicionar endereço, obter saldo e histórico."""
    pytest.skip("Adicionar quando integrações estiverem prontas")
