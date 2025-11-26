"""
Visualization Module
Creates professional, interactive visualizations using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
from config import CHARTS_DIR


class CurrencyVisualizer:
    """
    Creates publication-quality interactive charts for currency analysis.

    This class generates various visualization types including:
    - Time series charts
    - Volatility analysis
    - Year-over-year comparisons
    - Correlation matrices
    - Distribution analysis
    - Performance dashboards
    """

    # Consistent color scheme for each currency
    COLORS = {
        'EUR': '#003399',  # Blue
        'GBP': '#C8102E',  # Red
        'CAD': '#FF0000'   # Bright Red
    }

    def __init__(self, df, metrics):
        """
        Initialize the visualizer with data and metrics.

        Args:
            df: DataFrame with currency data
            metrics: Dictionary of calculated metrics
        """
        self.df = df
        self.metrics = metrics
        self.theme = 'plotly_white'

    def create_all_charts(self, output_dir=CHARTS_DIR):
        """
        Generate all visualizations and save to files.

        Args:
            output_dir: Directory to save chart files

        Returns:
            dict: Dictionary of chart names and figure objects
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        charts = {
            'time_series': self.plot_time_series(),
            'volatility': self.plot_volatility(),
            'yoy_comparison': self.plot_yoy_comparison(),
            'correlation': self.plot_correlation_matrix(),
            'distribution': self.plot_distribution(),
            'performance_summary': self.plot_performance_dashboard()
        }

        # Save each chart
        for name, fig in charts.items():
            output_path = f"{output_dir}/{name}.html"
            fig.write_html(output_path)
            print(f"Saved {name}.html")

        return charts

    def plot_time_series(self):
        """
        Create time series chart showing exchange rates over time.

        Returns:
            plotly.graph_objects.Figure: Interactive time series chart
        """
        fig = go.Figure()

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency]

            fig.add_trace(go.Scatter(
                x=curr_data['date'],
                y=curr_data['rate'],
                name=f'{currency}/USD',
                line=dict(color=self.COLORS[currency], width=2),
                mode='lines',
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Date: %{x|%Y-%m-%d}<br>' +
                             'Rate: %{y:.4f}<br>' +
                             '<extra></extra>'
            ))

        fig.update_layout(
            title='USD Exchange Rates: EUR, GBP, CAD (2020-Present)',
            xaxis_title='Date',
            yaxis_title='Exchange Rate (Foreign Currency per 1 USD)',
            template=self.theme,
            hovermode='x unified',
            height=500,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return fig

    def plot_volatility(self, window=4):
        """
        Create rolling volatility chart.

        Args:
            window: Rolling window size in quarters (default: 4 = 1 year)

        Returns:
            plotly.graph_objects.Figure: Volatility chart
        """
        fig = go.Figure()

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency].copy()

            # Calculate rolling volatility (quarterly data)
            curr_data['returns'] = curr_data['rate'].pct_change()
            curr_data['volatility'] = curr_data['returns'].rolling(window=window).std() * 100

            fig.add_trace(go.Scatter(
                x=curr_data['date'],
                y=curr_data['volatility'],
                name=currency,
                line=dict(color=self.COLORS[currency], width=2),
                mode='lines'
            ))

        fig.update_layout(
            title=f'{window}-Quarter Rolling Volatility',
            xaxis_title='Date',
            yaxis_title='Volatility (% quarterly std dev)',
            template=self.theme,
            hovermode='x unified',
            height=500
        )

        return fig

    def plot_yoy_comparison(self):
        """
        Create year-over-year comparison chart.

        Returns:
            plotly.graph_objects.Figure: YoY comparison chart
        """
        yoy = self.metrics['yoy_changes']

        fig = px.bar(
            yoy,
            x='year',
            y='yoy_change_pct',
            color='currency',
            barmode='group',
            color_discrete_map=self.COLORS,
            title='Year-over-Year Exchange Rate Changes',
            labels={
                'year': 'Year',
                'yoy_change_pct': 'Change (%)',
                'currency': 'Currency'
            },
            template=self.theme
        )

        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.update_layout(height=500)

        return fig

    def plot_correlation_matrix(self):
        """
        Create correlation matrix heatmap.

        Returns:
            plotly.graph_objects.Figure: Correlation heatmap
        """
        corr = self.metrics['correlations']

        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale='RdBu',
            zmid=0,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 16},
            colorbar=dict(title="Correlation")
        ))

        fig.update_layout(
            title='Currency Correlation Matrix',
            template=self.theme,
            height=400,
            width=500
        )

        return fig

    def plot_distribution(self):
        """
        Create distribution chart for quarterly returns.

        Returns:
            plotly.graph_objects.Figure: Distribution chart
        """
        fig = go.Figure()

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency].copy()
            curr_data['returns'] = curr_data['rate'].pct_change() * 100

            fig.add_trace(go.Histogram(
                x=curr_data['returns'].dropna(),
                name=currency,
                opacity=0.7,
                marker_color=self.COLORS[currency],
                nbinsx=50
            ))

        fig.update_layout(
            title='Distribution of Quarterly Returns (%)',
            xaxis_title='Quarterly Return (%)',
            yaxis_title='Frequency',
            template=self.theme,
            barmode='overlay',
            height=500
        )

        return fig

    def plot_performance_dashboard(self):
        """
        Create multi-metric dashboard view.

        Returns:
            plotly.graph_objects.Figure: Performance dashboard
        """
        summary = self.metrics['summary_stats']
        trends = self.metrics['trends']

        # Create subplot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Current Rates', 'Rate Ranges', '1-Quarter Change', '1-Year Change'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )

        # Current rates
        fig.add_trace(
            go.Bar(x=summary['currency'], y=summary['current_rate'],
                   marker_color=[self.COLORS[c] for c in summary['currency']],
                   name='Current'),
            row=1, col=1
        )

        # Rate ranges
        fig.add_trace(
            go.Bar(x=summary['currency'], y=summary['max_rate'] - summary['min_rate'],
                   marker_color=[self.COLORS[c] for c in summary['currency']],
                   name='Range'),
            row=1, col=2
        )

        # 1-quarter change
        if 'change_1q' in trends.columns:
            fig.add_trace(
                go.Bar(x=trends['currency'], y=trends['change_1q'],
                       marker_color=[self.COLORS[c] for c in trends['currency']],
                       name='1Q Change'),
                row=2, col=1
            )

        # 1-year change
        if 'change_1y' in trends.columns:
            fig.add_trace(
                go.Bar(x=trends['currency'], y=trends['change_1y'],
                       marker_color=[self.COLORS[c] for c in trends['currency']],
                       name='1Y Change'),
                row=2, col=2
            )

        fig.update_layout(
            title_text="Currency Performance Dashboard",
            showlegend=False,
            height=700,
            template=self.theme
        )

        return fig


if __name__ == "__main__":
    # Add parent directory to path for imports
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    from src.data.pipeline import CurrencyDataPipeline
    from src.analysis.metrics import CurrencyAnalyzer

    print("Testing Visualization Module")
    print("=" * 60)

    # Load data and calculate metrics
    print("\nLoading data and calculating metrics...")
    pipeline = CurrencyDataPipeline()
    df = pipeline.fetch_data()

    analyzer = CurrencyAnalyzer(df)
    metrics = analyzer.calculate_all_metrics()

    # Create visualizer
    print("Creating visualizations...")
    viz = CurrencyVisualizer(df, metrics)
    charts = viz.create_all_charts()

    print(f"\n✓ Successfully created {len(charts)} visualizations:")
    for name in charts.keys():
        print(f"  - {name}.html")

    print("\n" + "=" * 60)
    print("Visualization module test complete")
    print("=" * 60)
