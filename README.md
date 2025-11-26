# Currency Intelligence Platform

A professional data analysis platform for USD exchange rates (EUR, GBP, CAD) using US Treasury data.

**Live Application:** [https://umairleo1-currency-analysis-app-l0fbth.streamlit.app/](https://umairleo1-currency-analysis-app-l0fbth.streamlit.app/)

**Author:** Muhammad Umair
**Project:** Digital Platform Developer - KTP Associate Role
**Organization:** Sapphire Capital Partners & Queen's University Belfast
**Date:** November 2025

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Data Source](#data-source)
- [Analysis Components](#analysis-components)
- [Visualizations](#visualizations)
- [Future Enhancements](#future-enhancements)

---

## Overview

This platform provides actionable intelligence on currency exchange rates through:

- Automated data collection from the US Treasury API
- Comprehensive statistical analysis and metrics calculation
- Interactive visualizations for pattern identification
- Professional web-based dashboard for data exploration

The system is designed to support financial decision-making by providing timely, accurate, and actionable currency market intelligence using official government data.

---

## Features

### Data Pipeline
- Automated fetching from US Treasury Fiscal Data API
- Intelligent caching system to minimize API calls
- Data validation and cleaning
- Robust error handling and logging
- Quarterly data processing (official Treasury reporting periods)

### Statistical Analysis
- Summary statistics (current, min, max, mean, standard deviation)
- Year-over-year comparison and trend analysis
- Volatility metrics (rolling and annualized)
- Correlation analysis between currencies
- Extreme period identification
- Quarterly trend analysis (1Q, 1Y, 2Y)

### Visualizations
- Interactive time series charts
- Volatility analysis graphs (4-quarter rolling)
- Year-over-year comparison charts
- Correlation matrices
- Distribution analysis
- Multi-metric performance dashboards

### Web Dashboard
- Interactive Streamlit application
- Real-time data filtering and exploration
- Multiple export formats (CSV, JSON, TXT)
- Professional styling and responsive design
- Five comprehensive analysis tabs

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Internet connection for API access

### Setup Instructions

```bash
# 1. Navigate to project directory
cd currency-analysis

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Option 1: Run Complete Analysis Pipeline

Execute the main script to run the full analysis:

```bash
python main.py
```

This will:
1. Fetch currency data from the US Treasury API
2. Calculate all metrics and statistics
3. Generate interactive visualizations (saved to `outputs/charts/`)
4. Create a summary report (`outputs/summary_report.json`)

### Option 2: Launch Interactive Dashboard

Start the Streamlit web application:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

The dashboard provides:
- Executive summary with key metrics
- Historical exchange rate visualizations
- Detailed statistical analysis
- Risk and volatility assessment
- Raw data exploration and export capabilities

### Option 3: Explore Data with Jupyter Notebook

Open the data exploration notebook for in-depth analysis:

```bash
jupyter notebook data_exploration.ipynb
```

The notebook includes:
- Comprehensive data quality assessment
- Statistical analysis and visualizations
- Volatility and correlation analysis
- Trend identification and insights
- Export functionality for further analysis

---

## Project Structure

```
currency-analysis/
├── src/                          # Source code modules
│   ├── __init__.py
│   ├── data/                     # Data pipeline module
│   │   ├── __init__.py
│   │   └── pipeline.py           # API client and data processing
│   ├── analysis/                 # Analysis module
│   │   ├── __init__.py
│   │   └── metrics.py            # Statistical calculations
│   └── visualization/            # Visualization module
│       ├── __init__.py
│       └── charts.py             # Plotly chart generation
├── tests/                        # Test suite
│   └── __init__.py
├── data/                         # Data storage
│   └── cache/                    # Cached API responses
├── outputs/                      # Generated outputs
│   ├── charts/                   # HTML visualization files
│   └── summary_report.json       # Analysis summary
├── main.py                       # Main execution script
├── app.py                        # Streamlit dashboard application
├── data_exploration.ipynb        # Jupyter notebook for data exploration
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

---

## Technologies

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **pandas** | Data manipulation and analysis |
| **numpy** | Numerical computing |
| **requests** | HTTP client for API calls |
| **plotly** | Interactive data visualization |
| **streamlit** | Web dashboard framework |
| **python-dotenv** | Environment variable management |
| **pyyaml** | Configuration file handling |

---

## Data Source

**US Department of Treasury - Fiscal Data API**

- Website: https://fiscaldata.treasury.gov
- API Documentation: https://fiscaldata.treasury.gov/api-documentation/
- Dataset: Treasury Reporting Rates of Exchange
- Endpoint: `/v1/accounting/od/rates_of_exchange`
- Update Frequency: Quarterly (End of quarter)
- Coverage Period: 2020-01-01 to Present

The API provides official exchange rates used by the US Treasury for government accounting and currency conversion purposes. Data is updated quarterly to reflect official reporting periods.

---

## Analysis Components

### 1. Summary Statistics
- Current exchange rate for each currency
- Historical minimum and maximum rates
- Mean rate over the analysis period
- Standard deviation as a measure of dispersion

### 2. Trend Analysis
- 1-quarter short-term trend (~3 months)
- 1-year long-term trend (4 quarters)
- 2-year extended trend (8 quarters)
- Direction of travel (appreciation/depreciation)
- Percentage changes for each period

### 3. Volatility Analysis
- 4-quarter rolling volatility calculation
- Annualized volatility metrics
- Current vs. historical volatility comparison
- Volatility percentile ranking

### 4. Year-over-Year Comparison
- Annual rate changes
- Multi-year performance trends
- Identification of strong/weak performance years

### 5. Correlation Analysis
- Pairwise correlation between currencies
- Correlation matrix visualization
- Portfolio diversification insights

### 6. Extreme Period Identification
- Highest rate periods and dates
- Lowest rate periods and dates
- Maximum fluctuation ranges
- Historical volatility events

---

## Visualizations

The platform generates six interactive HTML visualizations:

### 1. Time Series Chart
- Line chart showing historical exchange rates
- All three currencies on a single chart
- Interactive hover tooltips with exact values
- Zoom and pan capabilities

### 2. Volatility Analysis
- 4-quarter rolling volatility over time
- Comparison across all currencies
- Identification of high-risk periods
- Annualized volatility metrics

### 3. Year-over-Year Comparison
- Grouped bar chart of annual changes
- Percentage change visualization
- Multi-year trend identification

### 4. Correlation Matrix
- Heatmap showing currency correlations
- Numerical correlation coefficients
- Portfolio risk assessment support

### 5. Distribution Analysis
- Histogram of quarterly returns
- Return distribution by currency
- Risk profile visualization

### 6. Performance Dashboard
- Multi-panel summary view
- Current rates, ranges, and quarterly/annual changes
- Comprehensive overview at a glance

All visualizations are:
- Interactive (hover, zoom, pan)
- Responsive and mobile-friendly
- Exportable as static images
- Styled with professional color schemes

---

## Future Enhancements

### Phase 2: Data Expansion
- Additional currency pairs (JPY, CHF, AUD, CNY, etc.)
- Commodity price integration (gold, oil, natural gas)
- Bond yield analysis
- Stock index correlations

### Phase 3: Predictive Analytics
- Time series forecasting (ARIMA, Prophet)
- Machine learning models for trend prediction
- Anomaly detection algorithms
- Regime change identification

### Phase 4: Real-Time Capabilities
- Live data feeds and streaming updates
- Automated alert system for threshold breaches
- Email/SMS notifications
- Real-time dashboard updates
- WebSocket integration

### Phase 5: API Development
- RESTful API for programmatic access
- Authentication and rate limiting
- JSON/XML response formats
- Comprehensive API documentation
- Client libraries (Python, JavaScript, R)

### Phase 6: Enterprise Features
- White-label solution for financial institutions
- Multi-tenant SaaS platform
- Custom branding and configuration
- Enterprise support and SLAs
- Advanced security features

---

## Development Status

**Current Version:** 1.0.0

| Component | Status |
|-----------|--------|
| Data Pipeline | ✓ Complete |
| Statistical Analysis | ✓ Complete |
| Visualizations (6 charts) | ✓ Complete |
| Web Dashboard | ✓ Complete |
| Documentation | ✓ Complete |
| Testing | In Progress |

---

## Author

**Muhammad Umair**

Candidate for Digital Platform Developer - KTP Associate
Sapphire Capital Partners & Queen's University Belfast
November 2025

---

## License

This project was created as part of the recruitment process for the KTP Associate role at Sapphire Capital Partners and Queen's University Belfast.

Data source: U.S. Department of Treasury (Public Domain)

---

## Acknowledgments

- U.S. Department of Treasury for providing open financial data through the Fiscal Data API
- Plotly development team for excellent interactive visualization capabilities
- Streamlit team for the intuitive and powerful web application framework

---

## Contact

For inquiries regarding this project, please contact through the KTP application process.

---

*Last Updated: November 25, 2025*
*Version: 1.0.0*
