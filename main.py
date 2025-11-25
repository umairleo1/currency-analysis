"""
Main Execution Script
Runs the complete currency analysis pipeline.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.data.pipeline import CurrencyDataPipeline
from src.analysis.metrics import CurrencyAnalyzer
from src.visualization.charts import CurrencyVisualizer
import json
from config import OUTPUT_DIR


def main():
    """Execute the complete analysis pipeline."""
    print("=" * 80)
    print("Currency Intelligence Platform")
    print("=" * 80)

    # Step 1: Fetch data
    print("\nStep 1: Fetching data from US Treasury API...")
    print("-" * 80)

    pipeline = CurrencyDataPipeline()
    df = pipeline.fetch_data()

    summary = pipeline.get_data_summary(df)
    print(f"Loaded {summary['total_records']} records")
    print(f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"Currencies: {', '.join(summary['currencies'])}")

    # Step 2: Analyze
    print("\nStep 2: Analyzing currency data...")
    print("-" * 80)

    analyzer = CurrencyAnalyzer(df)
    metrics = analyzer.calculate_all_metrics()

    print("Calculated metrics:")
    print("  - Summary statistics")
    print("  - Year-over-year changes")
    print("  - Volatility analysis")
    print("  - Trend analysis")
    print("  - Extreme periods")
    print("  - Correlation matrix")

    # Step 3: Visualize
    print("\nStep 3: Creating visualizations...")
    print("-" * 80)

    viz = CurrencyVisualizer(df, metrics)
    charts = viz.create_all_charts()

    print(f"Created {len(charts)} interactive visualizations")

    # Step 4: Save summary report
    print("\nStep 4: Generating summary report...")
    print("-" * 80)

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    summary_report = {
        'data_summary': summary,
        'summary_stats': metrics['summary_stats'].to_dict('records'),
        'trends': metrics['trends'].to_dict('records'),
        'volatility': metrics['volatility'].to_dict('records'),
        'extremes': metrics['extremes'].to_dict('records')
    }

    report_path = Path(OUTPUT_DIR) / 'summary_report.json'
    with open(report_path, 'w') as f:
        json.dump(summary_report, f, indent=2, default=str)

    print(f"Summary report saved to {report_path}")

    # Final summary
    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)
    print(f"\nOutputs saved to:")
    print(f"  - Visualizations: outputs/charts/")
    print(f"  - Summary report: {report_path}")
    print("\nTo view visualizations, open the HTML files in outputs/charts/")
    print("To run the interactive dashboard, use: streamlit run app.py")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError during execution: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
