
import pandas as pd
import os

from evidently import Report
from evidently.presets import DataDriftPreset


def run_monitoring():

    print("Starting Evidently monitoring...")

    reference_path = "data/reference.csv"
    current_path = "data/current.csv"

    # Check datasets
    if not os.path.exists(reference_path):
        raise FileNotFoundError("Reference CSV not found")

    if not os.path.exists(current_path):
        raise FileNotFoundError("Current CSV not found")

    # Load datasets
    reference = pd.read_csv(reference_path)
    current = pd.read_csv(current_path)

    print("Reference records:", len(reference))
    print("Current records:", len(current))

    if len(current) < 10:
        raise ValueError("At least 10 current records required")

    # Generate data drift report
    report = Report([
        DataDriftPreset()
    ])

    snapshot = report.run(
        current,
        reference
    )

    # Save report
    os.makedirs("reports", exist_ok=True)

    snapshot.save_html(
        "reports/data_drift_report.html"
    )

    print("Evidently monitoring completed!")
    print("HTML report generated successfully!")


if __name__ == "__main__":
    run_monitoring()
