
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime
from enum import Enum
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from .blockchain_analyzer import BlockchainAnalyzer, Transaction

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)


    class ExportFormat(Enum):
        """Formatos de exportação suportados pelo matplotlib."""
        PNG = 'png'
        SVG = 'svg'
        PDF = 'pdf'


    class DataVisualizer:
        """
        Classe para criação de visualizações de dados blockchain.

        Centraliza lógica de geração de gráficos, aplicando configurações de
        estilo consistentes e otimizando renderização conforme tipo de output.

        Example:
            >>> analyzer = BlockchainAnalyzer(network='ethereum', api_key='YOUR_API_KEY')
            >>> viz = DataVisualizer(analyzer, theme='professional')
            >>> # Para plotar, você precisaria de dados reais ou mockados
            >>> # viz.plot_price_evolution(data={'BTC': [...]}, output='btc_chart.png')
        """

        def __init__(
            self,
            analyzer: BlockchainAnalyzer,
            theme: str = 'professional',
            figsize: Tuple[int, int] = (12, 6),
            dpi: int = 100
        ):
            """
            Inicializa o visualizador com configurações de estilo.

            Args:
                analyzer: Instância de BlockchainAnalyzer para buscar dados.
                theme: Tema visual ('professional', 'dark', 'light')
                figsize: Tamanho padrão das figuras (largura, altura)
                dpi: Resolução para exportação de imagens
            """
            self.analyzer = analyzer
            self.theme = theme
            self.figsize = figsize
            self.dpi = dpi
            self._set_style()
            logger.info(f"DataVisualizer inicializado (tema: {theme})")

        def _set_style(self):
            """Configura o estilo visual dos gráficos com base no tema."""
            plt.style.use('seaborn-v0_8-darkgrid')
            if self.theme == 'dark':
                plt.rcParams.update({
                    "figure.facecolor": "#282C34",
                    "axes.facecolor": "#282C34",
                    "text.color": "white",
                    "axes.labelcolor": "white",
                    "xtick.color": "white",
                    "ytick.color": "white",
                    "grid.color": "#444444",
                    "grid.linestyle": ":",
                    "grid.linewidth": 0.5,
                    "axes.edgecolor": "white",
                    "savefig.facecolor": "#282C34"
                })
            elif self.theme == 'light':
                plt.rcParams.update({
                    "figure.facecolor": "white",
                    "axes.facecolor": "white",
                    "text.color": "black",
                    "axes.labelcolor": "black",
                    "xtick.color": "black",
                    "ytick.color": "black",
                    "grid.color": "#DDDDDD",
                    "grid.linestyle": ":",
                    "grid.linewidth": 0.5,
                    "axes.edgecolor": "black",
                    "savefig.facecolor": "white"
                })

        def plot_price_evolution(
            self,
            data: pd.DataFrame,
            cryptocurrency: str,
            output: Optional[str] = None
        ) -> plt.Figure:
            """
            Cria gráfico de evolução de preços ao longo do tempo.

            Args:
                data: DataFrame com colunas 'timestamp' e 'price'.
                cryptocurrency: Símbolo da criptomoeda (ex: 'BTC').
                output: Caminho para salvar o gráfico (None = apenas exibir).

            Returns:
                Objeto figura do matplotlib.
            """
            logger.info(f"Gerando gráfico de evolução de preços para {cryptocurrency}")
            fig, ax = plt.subplots(figsize=self.figsize)
            sns.lineplot(x='timestamp', y='price', data=data, ax=ax)
            ax.set_title(f'Evolução do Preço de {cryptocurrency}')
            ax.set_xlabel('Data')
            ax.set_ylabel('Preço (USD)')
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            if output:
                plt.savefig(output, dpi=self.dpi, bbox_inches="tight")
                logger.info(f"Gráfico salvo em {output}")
            return fig

        def plot_portfolio_allocation(
            self,
            holdings: Dict[str, float],
            output: Optional[str] = None
        ) -> plt.Figure:
            """
            Cria gráfico de pizza mostrando alocação do portfolio.

            Args:
                holdings: Dicionário {ativo: valor_em_usd}
                output: Caminho para salvar
            """
            logger.info("Gerando gráfico de alocação de portfólio")
            labels = holdings.keys()
            sizes = holdings.values()

            fig, ax = plt.subplots(figsize=self.figsize)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
            ax.axis('equal')
            ax.set_title('Alocação do Portfólio')
            plt.tight_layout()
            if output:
                plt.savefig(output, dpi=self.dpi, bbox_inches="tight")
                logger.info(f"Gráfico salvo em {output}")
            return fig

        def plot_transaction_volume(
            self,
            transactions: List[Dict[str, Any]],
            output: Optional[str] = None
        ) -> plt.Figure:
            """
            Cria gráfico de barras com volume de transações por período.

            Args:
                transactions: Lista de dicionários de transações (como retornado pelo BlockchainAnalyzer).
                output: Caminho para salvar o gráfico.
            """
            logger.info("Gerando gráfico de volume de transações")
            if not transactions:
                logger.warning("Nenhuma transação fornecida para plotar o volume.")
                fig, ax = plt.subplots(figsize=self.figsize)
                ax.text(0.5, 0.5, "Nenhum dado de transação disponível", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                ax.set_title('Volume de Transações')
                if output:
                    plt.savefig(output, dpi=self.dpi, bbox_inches="tight")
                return fig

            # Converter para DataFrame usando Transaction diretamente (não é método do analyzer)
            df = pd.DataFrame([Transaction(tx).__dict__ for tx in transactions])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)

            # Agrupar por dia e somar o valor das transações
            daily_volume = df['value'].resample('D').sum().fillna(0)

            fig, ax = plt.subplots(figsize=self.figsize)
            daily_volume.plot(kind='bar', ax=ax)
            ax.set_title('Volume Diário de Transações (ETH)')
            ax.set_xlabel('Data')
            ax.set_ylabel('Volume (ETH)')
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            if output:
                plt.savefig(output, dpi=self.dpi, bbox_inches="tight")
                logger.info(f"Gráfico salvo em {output}")
            return fig

        def create_dashboard(
            self,
            data_sources: Dict[str, Any],
            metrics: Optional[List[str]] = None,
            export_html: bool = False
        ) -> Any:
            """
            Cria dashboard consolidado com múltiplas métricas.

            Args:
                data_sources: Fontes de dados para compor o dashboard
                metrics: Lista de métricas a exibir
                export_html: Se True, exporta para HTML (não implementado)

            Returns:
                Objeto figura do matplotlib
            """
            logger.info("Criando dashboard (funcionalidade básica)")
            fig, axes = plt.subplots(nrows=len(metrics) if metrics else 1, ncols=1, figsize=(10, 5 * (len(metrics) if metrics else 1)))
            if not isinstance(axes, (list, tuple, pd.Series, pd.DataFrame)):
                axes = [axes]

            for i, metric in enumerate(metrics or []):
                ax = axes[i]
                ax.text(0.5, 0.5, f"Placeholder para {metric}", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                ax.set_title(f"Métrica: {metric}")
                ax.set_xticks([])
                ax.set_yticks([])

            plt.tight_layout()
            if export_html:
                logger.warning("Exportação para HTML não implementada para dashboards matplotlib.")
                return None
            return fig

        def export(
            self,
            figure: plt.Figure,
            filename: str,
            format: ExportFormat = ExportFormat.PNG
        ) -> bool:
            """
            Exporta figura em formato especificado.

            Args:
                figure: Objeto figura (matplotlib)
                filename: Nome do arquivo de saída
                format: Formato de exportação (PNG, SVG, PDF)

            Returns:
                True se exportação bem-sucedida
            """
            logger.info(f"Exportando para {filename} ({format.value})")
            try:
                figure.savefig(filename, dpi=self.dpi, format=format.value)
                return True
            except Exception as e:
                logger.error(f"Erro ao exportar figura para {filename}: {e}")
                return False

        def set_style(
            self,
            colors: Optional[List[str]] = None,
            font_family: Optional[str] = None
        ) -> None:
            """Customiza estilo visual dos gráficos."""
            if colors:
                sns.set_palette(colors)
            if font_family:
                plt.rcParams["font.family"] = font_family
            logger.info("Estilo visual atualizado.")
