"""
Interactive Dashboard
Professional Streamlit web application for currency exchange rate analysis.

Run with: streamlit run app.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd
from datetime import datetime
from src.data.pipeline import CurrencyDataPipeline
from src.analysis.metrics import CurrencyAnalyzer
from src.visualization.charts import CurrencyVisualizer

# Page configuration
st.set_page_config(
    page_title="Currency Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Currency Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Professional Analysis of USD Exchange Rates: EUR, GBP, CAD</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Dashboard Controls")

    # Refresh button
    if st.button("🔄 Refresh Data", help="Clear cache and reload data from Treasury API", use_container_width=True):
        st.cache_data.clear()
        st.success("Cache cleared! Data will refresh on next interaction.")
        st.rerun()

    st.markdown("---")

    # Information section
    st.header("Information")

    with st.expander("📊 About This Dashboard", expanded=False):
        st.markdown("""
        This platform provides comprehensive analysis of currency exchange rates using official data from the US Treasury.

        **Features:**
        - Real-time data analysis
        - Interactive visualizations
        - Statistical metrics
        - Risk assessment
        - Data export capabilities
        """)

    with st.expander("📈 Data Source", expanded=False):
        st.markdown("""
        **Source:** US Department of Treasury
        **API:** Fiscal Data Service
        **Endpoint:** Treasury Reporting Rates of Exchange
        **Frequency:** Quarterly (End of quarter)
        **Period:** 2020-01-01 to Present
        """)

    with st.expander("💱 Currencies Analyzed", expanded=False):
        st.markdown("""
        - **EUR** - Euro (European Union)
        - **GBP** - British Pound (United Kingdom)
        - **CAD** - Canadian Dollar (Canada)

        All rates are quoted as foreign currency per 1 USD.
        """)

    st.markdown("---")

    st.caption("**Project:** Sapphire Capital Partners")
    st.caption("**Platform:** Currency Intelligence Platform v1.0")
    st.caption(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Load data function
@st.cache_data
def load_data():
    """Load and process currency data with caching."""
    try:
        pipeline = CurrencyDataPipeline()
        df = pipeline.fetch_data()

        if df is None or len(df) == 0:
            return None, None, "No data returned from API"

        analyzer = CurrencyAnalyzer(df)
        metrics = analyzer.calculate_all_metrics()
        return df, metrics
    except Exception as e:
        import traceback
        error_details = f"{str(e)}\n{traceback.format_exc()}"
        return None, None, error_details

# Load data with progress indicator
with st.spinner("Loading currency data from US Treasury API..."):
    result = load_data()

    if len(result) == 3:
        df, metrics, error = result
        if df is None:
            st.error("Failed to load data from US Treasury API")
            with st.expander("Error Details"):
                st.code(error)
            st.info("Please check your internet connection and try refreshing.")
            st.stop()
    else:
        df, metrics = result
        if df is None or metrics is None:
            st.error("Failed to load data. Please check your connection and try again.")
            st.stop()

# Data loaded successfully
st.success(f"✓ Loaded {len(df)} records from {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")

# Debug: Show what currencies were actually loaded
with st.expander("Debug: Data Loading Info"):
    st.write(f"**Total Records:** {len(df)}")
    st.write(f"**Date Range:** {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")
    st.write(f"**Currencies in Data:**")
    for curr in df['currency'].unique():
        count = len(df[df['currency'] == curr])
        st.write(f"  - {curr}: {count} records")
    if df['currency'].isna().any():
        st.warning(f"⚠️ Found {df['currency'].isna().sum()} records with missing currency codes")
        st.write("**Currency names that failed to map:**")
        unmapped = df[df['currency'].isna()]['currency_name'].unique()
        for name in unmapped:
            st.write(f"  - '{name}'")

# Create visualizer
viz = CurrencyVisualizer(df, metrics)

# Helper function for safe data access
def get_currency_data(dataframe, currency):
    """Safely get currency data, return None if not found."""
    filtered = dataframe[dataframe['currency'] == currency]
    if len(filtered) == 0:
        return None
    return filtered.iloc[0]

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "📈 Detailed Analysis",
    "⚠️ Risk & Volatility",
    "🎯 Performance Dashboard",
    "📋 Data Explorer"
])

# TAB 1: Overview
with tab1:
    st.header("Executive Summary")
    st.markdown("Current exchange rates and key performance indicators")

    # Key metrics in cards
    col1, col2, col3 = st.columns(3)

    summary = metrics['summary_stats']
    trends = metrics['trends']

    currencies = ['EUR', 'GBP', 'CAD']
    colors = ['#003399', '#C8102E', '#FF0000']

    for idx, currency in enumerate(currencies):
        curr_summary = get_currency_data(summary, currency)
        curr_trends = get_currency_data(trends, currency)

        with [col1, col2, col3][idx]:
            if curr_summary is None or curr_trends is None:
                st.error(f"{currency} data not available")
                continue

            # Calculate change for display
            change_1q = curr_trends.get('change_1q', 0)
            change_1y = curr_trends.get('change_1y', 0)

            st.metric(
                label=f"{currency}/USD",
                value=f"{curr_summary['current_rate']:.4f}",
                delta=f"{change_1q:.2f}% (1Q)",
                help=f"1-Year Change: {change_1y:.2f}%"
            )

            # Additional stats in expander
            with st.expander("View Details"):
                st.write(f"**Range:** {curr_summary['min_rate']:.4f} - {curr_summary['max_rate']:.4f}")
                st.write(f"**Mean:** {curr_summary['mean_rate']:.4f}")
                st.write(f"**Std Dev:** {curr_summary['std_rate']:.4f}")

    st.markdown("---")

    # Time series chart
    st.subheader("Historical Exchange Rates")
    st.markdown("Interactive chart showing quarterly exchange rates over time")
    fig = viz.plot_time_series()
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Key insights
    st.subheader("Key Insights")

    col1, col2 = st.columns([2, 1])

    with col1:
        for _, row in trends.iterrows():
            change_1q = row.get('change_1q', 0)
            change_1y = row.get('change_1y', 0)
            direction_symbol = "↑" if change_1q > 0 else "↓"

            # Color based on change
            color = "green" if change_1q > 0 else "red"

            st.markdown(f"""
            **{row['currency']}**: {direction_symbol} **{abs(change_1q):.2f}%** over last quarter,
            **{abs(change_1y):.2f}%** over last year
            """)

    with col2:
        st.info("""
        **Note:** All rates are quarterly official Treasury rates.

        Positive values indicate USD weakening (foreign currency appreciating).
        """)

# TAB 2: Detailed Analysis
with tab2:
    st.header("Detailed Analysis")
    st.markdown("Year-over-year comparison and correlation analysis")

    # Year-over-year
    st.subheader("Year-over-Year Comparison")
    st.markdown("Annual percentage changes in exchange rates")
    fig_yoy = viz.plot_yoy_comparison()
    st.plotly_chart(fig_yoy, use_container_width=True)

    st.markdown("---")

    # Two columns for correlation and extremes
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Currency Correlations")
        st.markdown("How currencies move together")
        fig_corr = viz.plot_correlation_matrix()
        st.plotly_chart(fig_corr, use_container_width=True)

        st.info("""
        **Interpretation:**
        - 1.0: Perfect positive correlation
        - 0.0: No correlation
        - -1.0: Perfect negative correlation
        """)

    with col2:
        st.subheader("Extreme Periods")
        st.markdown("Highest and lowest rates recorded")

        extremes = metrics['extremes']
        for _, row in extremes.iterrows():
            with st.container():
                st.markdown(f"**{row['currency']}**")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric(
                        "Highest Rate",
                        f"{row['highest_rate']:.4f}",
                        help=f"Date: {row['highest_date']:%Y-%m-%d}"
                    )
                with col_b:
                    st.metric(
                        "Lowest Rate",
                        f"{row['lowest_rate']:.4f}",
                        help=f"Date: {row['lowest_date']:%Y-%m-%d}"
                    )

                st.write(f"Range: {row['range_pct']:.2f}%")
                st.markdown("---")

# TAB 3: Risk & Volatility
with tab3:
    st.header("Risk & Volatility Analysis")
    st.markdown("Comprehensive risk assessment and volatility metrics")

    # Volatility metrics summary
    st.subheader("Current Volatility Overview")

    vol_metrics = metrics['volatility']
    col1, col2, col3 = st.columns(3)

    for idx, currency in enumerate(['EUR', 'GBP', 'CAD']):
        curr_vol = get_currency_data(vol_metrics, currency)

        with [col1, col2, col3][idx]:
            if curr_vol is None:
                st.error(f"{currency} volatility data not available")
                continue

            current_vol = curr_vol['current_volatility']
            avg_vol = curr_vol['average_volatility']

            st.metric(
                label=f"{currency} Volatility",
                value=f"{current_vol*100:.2f}%" if pd.notna(current_vol) else "N/A",
                delta=f"{((current_vol - avg_vol) / avg_vol * 100):.1f}% vs avg" if pd.notna(current_vol) and pd.notna(avg_vol) else None,
                help="Annualized volatility based on 4-quarter rolling window"
            )

    st.markdown("---")

    # Rolling volatility chart
    st.subheader("Rolling Volatility Over Time")
    st.markdown("4-quarter (1-year) rolling volatility comparison")
    fig_vol = viz.plot_volatility()
    st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("---")

    # Return distribution
    st.subheader("Return Distribution")
    st.markdown("Distribution of period-to-period returns (risk profile)")
    fig_dist = viz.plot_distribution()
    st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")

    # Volatility table
    st.subheader("Volatility Metrics Table")
    vol_display = vol_metrics.copy()
    vol_display['current_volatility'] = vol_display['current_volatility'].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")
    vol_display['average_volatility'] = vol_display['average_volatility'].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")
    vol_display['volatility_percentile'] = vol_display['volatility_percentile'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")

    st.dataframe(
        vol_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "currency": "Currency",
            "current_volatility": "Current Volatility",
            "average_volatility": "Average Volatility",
            "volatility_percentile": "Percentile"
        }
    )

# TAB 4: Performance Dashboard
with tab4:
    st.header("Performance Dashboard")
    st.markdown("Comprehensive multi-metric performance overview")

    # Performance dashboard chart
    fig_perf = viz.plot_performance_dashboard()
    st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("---")

    # Summary statistics table
    st.subheader("Complete Summary Statistics")

    summary_display = summary.copy()
    summary_display['current_date'] = pd.to_datetime(summary_display['current_date']).dt.strftime('%Y-%m-%d')

    st.dataframe(
        summary_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "currency": "Currency",
            "current_rate": st.column_config.NumberColumn("Current Rate", format="%.4f"),
            "current_date": "As of Date",
            "min_rate": st.column_config.NumberColumn("Min Rate", format="%.4f"),
            "max_rate": st.column_config.NumberColumn("Max Rate", format="%.4f"),
            "mean_rate": st.column_config.NumberColumn("Mean Rate", format="%.4f"),
            "std_rate": st.column_config.NumberColumn("Std Dev", format="%.4f")
        }
    )

    st.markdown("---")

    # Year-over-year table
    st.subheader("Year-over-Year Performance")

    yoy = metrics['yoy_changes']
    yoy_display = yoy.copy()
    yoy_display['yoy_change_pct'] = yoy_display['yoy_change_pct'].apply(lambda x: f"{x:+.2f}%")
    yoy_display['rate'] = yoy_display['rate'].apply(lambda x: f"{x:.4f}")

    st.dataframe(
        yoy_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "currency": "Currency",
            "year": "Year",
            "rate": "Rate",
            "yoy_change_pct": "YoY Change"
        }
    )

# TAB 5: Data Explorer
with tab5:
    st.header("Data Explorer")
    st.markdown("Explore and export raw currency data")

    # Filter controls
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Filter Options")
        selected_currency = st.multiselect(
            "Select currencies to display",
            options=df['currency'].unique().tolist(),
            default=df['currency'].unique().tolist(),
            help="Choose which currencies to include in the table"
        )

    with col2:
        st.subheader("Quick Stats")
        if selected_currency:
            st.metric("Records", len(df[df['currency'].isin(selected_currency)]))
            st.metric("Currencies", len(selected_currency))

    st.markdown("---")

    if selected_currency:
        # Filter data
        filtered_df = df[df['currency'].isin(selected_currency)].copy()
        filtered_df['date'] = pd.to_datetime(filtered_df['date']).dt.strftime('%Y-%m-%d')

        # Display data
        st.subheader("Currency Data Table")
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400,
            column_config={
                "date": "Date",
                "currency": "Currency",
                "rate": st.column_config.NumberColumn("Exchange Rate", format="%.4f"),
                "currency_name": "Full Name"
            }
        )

        # Download section
        st.markdown("---")
        st.subheader("Export Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            # CSV download
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"currency_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            # JSON download
            json_data = filtered_df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"currency_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

        with col3:
            # Summary download
            summary_text = f"""Currency Data Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Records: {len(filtered_df)}
Currencies: {', '.join(selected_currency)}
Date Range: {filtered_df['date'].min()} to {filtered_df['date'].max()}

Data Source: US Department of Treasury
API: Fiscal Data Service
"""
            st.download_button(
                label="📥 Download Summary",
                data=summary_text,
                file_name=f"summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )

    else:
        st.info("Please select at least one currency to display data")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("**Data Source:** U.S. Department of Treasury - Fiscal Data API")

with col2:
    st.caption("**Platform:** Currency Intelligence Platform")

with col3:
    st.caption(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
