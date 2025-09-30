"""
Testes para visualizer.py
-------------------------
Estrutura mínima com pytest, fixtures e testes stub/documentados.
Autor: Gabriel Demetrios Lafis
Data: 2025
Licença: MIT
"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def dados_simples():
    return {
        "timestamps": [1, 2, 3],
        "values": [10.0, 11.5, 9.7],
    }


class TestDataVisualizer:
    """Suite de testes do módulo DataVisualizer."""

    def test_init_sem_dependencias_pesadas(self):
        """Inicialização não deve carregar backends gráficos desnecessários em testes."""
        pytest.skip("Implementar DataVisualizer e injeção de dependências/light backends")

    def test_plot_price_evolution_cria_arquivo(self, tmp_path, dados_simples):
        """plot_price_evolution deve gerar arquivo de saída no formato esperado."""
        pytest.skip("Implementar geração de gráficos com backend offscreen e path de saída")

    def test_create_dashboard_exporta_html(self, tmp_path):
        """create_dashboard deve exportar HTML quando solicitado."""
        pytest.skip("Implementar exportação HTML e validações de conteúdo mínimo")
