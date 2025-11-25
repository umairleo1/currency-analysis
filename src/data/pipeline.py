"""
Data Pipeline Module
Handles fetching, caching, and processing currency exchange rate data from US Treasury API.
"""

import requests
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
from config import (
    API_BASE,
    ENDPOINT,
    CURRENCIES,
    START_DATE,
    CACHE_ENABLED,
    CACHE_DIR
)


class CurrencyDataPipeline:
    """
    Manages data fetching and processing for currency exchange rates.

    This class provides functionality to:
    - Fetch data from the US Treasury API
    - Cache responses to minimize API calls
    - Clean and validate data
    - Transform data into analysis-ready format
    """

    def __init__(self):
        """Initialize the data pipeline with cache directory."""
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_data(self, currencies=None, start_date=START_DATE, use_cache=CACHE_ENABLED):
        """
        Fetch exchange rate data for specified currencies.

        Args:
            currencies: List of currency codes (EUR, GBP, CAD) or None for all
            start_date: Start date in YYYY-MM-DD format
            use_cache: Whether to use cached data if available

        Returns:
            pd.DataFrame: DataFrame with columns [date, currency, rate, currency_name]

        Raises:
            requests.RequestException: If API request fails
            ValueError: If data validation fails
        """
        if currencies is None:
            currencies = list(CURRENCIES.keys())

        # Check cache
        cache_file = self.cache_dir / f"data_{start_date}.csv"
        if use_cache and cache_file.exists():
            print(f"Loading cached data from {cache_file}")
            return pd.read_csv(cache_file, parse_dates=['date'])

        # Build currency filter
        currency_names = [CURRENCIES[c] for c in currencies]
        currency_filter = ','.join(currency_names)

        # Build API URL
        url = f"{API_BASE}{ENDPOINT}"
        params = {
            'fields': 'country_currency_desc,exchange_rate,record_date',
            'filter': f'country_currency_desc:in:({currency_filter}),record_date:gte:{start_date}',
            'page[size]': 10000
        }

        print(f"Fetching data from US Treasury API...")
        print(f"URL: {url}")
        print(f"Currencies: {', '.join(currencies)}")
        print(f"Start date: {start_date}")

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch data from API: {str(e)}")

        data = response.json()

        if 'data' not in data or len(data['data']) == 0:
            raise ValueError("No data returned from API")

        # Convert to DataFrame
        df = pd.DataFrame(data['data'])

        # Clean and transform
        df = self._process_data(df)

        # Cache it
        df.to_csv(cache_file, index=False)
        print(f"Data cached to {cache_file}")
        print(f"Total records fetched: {len(df)}")

        return df

    def _process_data(self, df):
        """
        Clean and transform raw API data.

        Args:
            df: Raw DataFrame from API

        Returns:
            pd.DataFrame: Cleaned and transformed DataFrame
        """
        # Rename columns to standardized names
        df = df.rename(columns={
            'record_date': 'date',
            'exchange_rate': 'rate',
            'country_currency_desc': 'currency_name'
        })

        # Convert data types
        df['date'] = pd.to_datetime(df['date'])
        df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

        # Drop any rows with invalid rates
        df = df.dropna(subset=['rate'])

        # Add currency code column
        currency_map = {v: k for k, v in CURRENCIES.items()}
        df['currency'] = df['currency_name'].map(currency_map)

        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)

        # Select and order columns
        df = df[['date', 'currency', 'rate', 'currency_name']]

        return df

    def get_data_summary(self, df):
        """
        Generate a summary of the fetched data.

        Args:
            df: DataFrame with currency data

        Returns:
            dict: Summary statistics
        """
        summary = {
            'total_records': len(df),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d')
            },
            'currencies': df['currency'].unique().tolist(),
            'records_per_currency': df['currency'].value_counts().to_dict()
        }
        return summary


if __name__ == "__main__":
    # Add parent directory to path for config import
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    # Test the pipeline
    pipeline = CurrencyDataPipeline()
    print("Testing data pipeline...")
    print("=" * 60)

    try:
        df = pipeline.fetch_data()
        summary = pipeline.get_data_summary(df)

        print("\nData Pipeline Test Results:")
        print(f"Total records: {summary['total_records']}")
        print(f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        print(f"Currencies: {', '.join(summary['currencies'])}")
        print(f"\nRecords per currency:")
        for curr, count in summary['records_per_currency'].items():
            print(f"  {curr}: {count} records")
        print("\nSample data (first 5 records):")
        print(df.head())
        print("\nSample data (last 5 records):")
        print(df.tail())
        print("\n" + "=" * 60)
        print("Data pipeline test successful")
        print("=" * 60)

    except Exception as e:
        print(f"\nError during pipeline test: {str(e)}")
        import traceback
        traceback.print_exc()
