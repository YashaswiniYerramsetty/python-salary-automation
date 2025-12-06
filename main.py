"""
Python Salary Automation Project
---------------------------------
This script reads employee salary data from a CSV file,
calculates salary based on attendance, allowances, and deductions,
and generates a final payroll summary CSV.

How to run:
    python main.py --input sample_input.csv --output payroll_summary.csv
    OR
    python main.py -i sample_input.csv -o output\payroll_summary.csv
"""

import argparse
import pandas as pd
import os


def calculate_salary(row):
    """
    Calculate prorated salary based on attendance.
    Salary Formula:
        prorated_salary = base_salary * (days_present / total_working_days)
        gross_salary = prorated_salary + allowances
        tax = 10% of gross_salary
        net_salary = gross_salary - (tax + other_deductions)
    """
    base = float(row["base_salary"])
    present = float(row["days_present"])
    total = float(row["total_working_days"])
    allowances = float(row["allowances"])
    other_deductions = float(row["other_deductions"])

    # Avoid division by zero
    if total == 0:
        total = 1

    prorated = base * (present / total)
    gross = prorated + allowances
    tax = gross * 0.10  # 10% tax
    deductions = tax + other_deductions
    net_salary = gross - deductions

    return {
        "prorated_salary": round(prorated, 2),
        "gross_salary": round(gross, 2),
        "tax": round(tax, 2),
        "total_deductions": round(deductions, 2),
        "net_salary": round(net_salary, 2)
    }


def generate_payroll(input_csv, output_csv):
    # Read input CSV
    df = pd.read_csv(input_csv)

    # Apply salary calculation to each row
    results = df.apply(lambda r: pd.Series(calculate_salary(r)), axis=1)

    # Merge original data + calculated results
    final_df = pd.concat([df, results], axis=1)

    # Create output folder if a folder is specified
    folder = os.path.dirname(output_csv)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Save final payroll CSV
    final_df.to_csv(output_csv, index=False)

    # Print summary
    print("\n✅ Payroll Generated Successfully!")
    print(f"📁 Output File: {output_csv}")
    print(f"👨‍💼 Total Employees: {len(final_df)}")
    print(f"💰 Total Payout: {final_df['net_salary'].sum():.2f}")

    return final_df


def main():
    parser = argparse.ArgumentParser(description="Salary Automation Script")
    parser.add_argument(
        "--input", "-i", required=True, help="Path to input CSV file"
    )
    parser.add_argument(
        "--output", "-o", required=True, help="Path to output CSV file"
    )

    args = parser.parse_args()

    generate_payroll(args.input, args.output)


if __name__ == "__main__":
    main()
