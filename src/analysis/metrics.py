"""
Analysis Module
Statistical analysis and metrics calculation for currency exchange rates.
"""

import pandas as pd
import numpy as np


class CurrencyAnalyzer:
    """
    Performs statistical analysis on currency exchange rate data.

    This class calculates various metrics including:
    - Summary statistics (mean, min, max, std)
    - Year-over-year changes
    - Volatility analysis
    - Trend analysis
    - Correlation analysis
    - Extreme period identification
    """

    def __init__(self, df):
        """
        Initialize the analyzer with currency data.

        Args:
            df: DataFrame with columns [date, currency, rate]
        """
        self.df = df
        self.metrics = {}

    def calculate_all_metrics(self):
        """
        Calculate all available metrics and return consolidated results.

        Returns:
            dict: Dictionary containing all calculated metrics
        """
        self.metrics = {
            'summary_stats': self.get_summary_stats(),
            'yoy_changes': self.get_yoy_changes(),
            'volatility': self.get_volatility(),
            'trends': self.get_trends(),
            'extremes': self.get_extreme_periods(),
            'correlations': self.get_correlations()
        }
        return self.metrics

    def get_summary_stats(self):
        """
        Calculate summary statistics for each currency.

        Returns:
            pd.DataFrame: Summary statistics including current rate, min, max, mean, std
        """
        stats = []

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency]

            stats.append({
                'currency': currency,
                'current_rate': curr_data.iloc[-1]['rate'],
                'current_date': curr_data.iloc[-1]['date'],
                'min_rate': curr_data['rate'].min(),
                'max_rate': curr_data['rate'].max(),
                'mean_rate': curr_data['rate'].mean(),
                'std_rate': curr_data['rate'].std()
            })

        return pd.DataFrame(stats)

    def get_yoy_changes(self):
        """
        Calculate year-over-year percentage changes.

        Returns:
            pd.DataFrame: Year-over-year changes for each currency
        """
        results = []

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency].copy()
            curr_data['year'] = curr_data['date'].dt.year

            # Get latest rate per year
            yearly = curr_data.groupby('year')['rate'].last()

            for year in yearly.index[1:]:
                prev_year = year - 1
                if prev_year in yearly.index:
                    change = ((yearly[year] - yearly[prev_year]) / yearly[prev_year]) * 100
                    results.append({
                        'currency': currency,
                        'year': year,
                        'rate': yearly[year],
                        'yoy_change_pct': change
                    })

        return pd.DataFrame(results)

    def get_volatility(self, window=4):
        """
        Calculate rolling volatility for each currency.

        Args:
            window: Rolling window size in periods (default: 4 quarters = 1 year)

        Returns:
            pd.DataFrame: Volatility metrics for each currency
        """
        results = []

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency].copy()

            # Calculate period-to-period returns
            curr_data['returns'] = curr_data['rate'].pct_change()

            # Rolling volatility (annualized for quarterly data)
            curr_data['volatility'] = curr_data['returns'].rolling(window=window).std() * np.sqrt(4)

            # Current and average volatility
            current_vol = curr_data['volatility'].iloc[-1] if not curr_data['volatility'].empty else np.nan
            avg_vol = curr_data['volatility'].mean()

            # Volatility percentile
            if not pd.isna(current_vol):
                vol_percentile = (curr_data['volatility'] < current_vol).mean() * 100
            else:
                vol_percentile = np.nan

            results.append({
                'currency': currency,
                'current_volatility': current_vol,
                'average_volatility': avg_vol,
                'volatility_percentile': vol_percentile
            })

        return pd.DataFrame(results)

    def get_trends(self):
        """
        Analyze trends over different time periods.

        For quarterly data: 1 quarter, 4 quarters (1 year), and 8 quarters (2 years)

        Returns:
            pd.DataFrame: Trend analysis for different periods
        """
        results = []

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency].copy()
            current_rate = curr_data.iloc[-1]['rate']

            changes = {'currency': currency}

            # For quarterly data: look back by number of quarters
            for periods, label in [(1, '1q'), (4, '1y'), (8, '2y')]:
                if len(curr_data) > periods:
                    past_rate = curr_data.iloc[-(periods + 1)]['rate']
                    change_pct = ((current_rate - past_rate) / past_rate) * 100
                    changes[f'change_{label}'] = change_pct
                    changes[f'direction_{label}'] = 'up' if change_pct > 0 else 'down'

            results.append(changes)

        return pd.DataFrame(results)

    def get_extreme_periods(self):
        """
        Identify periods of extreme rates (highest and lowest).

        Returns:
            pd.DataFrame: Extreme periods for each currency
        """
        results = []

        for currency in self.df['currency'].unique():
            curr_data = self.df[self.df['currency'] == currency].copy()

            # Find max and min rate points
            max_idx = curr_data['rate'].idxmax()
            min_idx = curr_data['rate'].idxmin()

            max_rate = curr_data.loc[max_idx, 'rate']
            min_rate = curr_data.loc[min_idx, 'rate']

            results.append({
                'currency': currency,
                'highest_rate': max_rate,
                'highest_date': curr_data.loc[max_idx, 'date'],
                'lowest_rate': min_rate,
                'lowest_date': curr_data.loc[min_idx, 'date'],
                'range_pct': ((max_rate - min_rate) / min_rate) * 100
            })

        return pd.DataFrame(results)

    def get_correlations(self):
        """
        Calculate correlation matrix between currencies.

        Returns:
            pd.DataFrame: Correlation matrix
        """
        # Pivot to wide format (use pivot_table to handle potential duplicates)
        pivot = self.df.pivot_table(
            index='date',
            columns='currency',
            values='rate',
            aggfunc='mean'  # Average if there are duplicates on same date
        )

        # Calculate correlations
        corr = pivot.corr()

        return corr


if __name__ == "__main__":
    print("Analysis module created successfully")
