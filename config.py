"""Configuration settings for the Currency Intelligence Platform."""

# API Configuration
API_BASE = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
ENDPOINT = "/v1/accounting/od/rates_of_exchange"

# Currencies to analyze
CURRENCIES = {
    'EUR': 'Euro Zone-Euro',
    'GBP': 'United Kingdom-Pound',
    'CAD': 'Canada-Dollar'
}

# Date range
START_DATE = "2020-01-01"  # ~5 years of data

# Cache settings
CACHE_ENABLED = True
CACHE_DIR = "data/cache"

# Output settings
OUTPUT_DIR = "outputs"
CHARTS_DIR = "outputs/charts"
