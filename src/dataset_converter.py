"""
Dataset Format Converter for Vulnerability Detection
-----------------------------------------------------

This script converts paired vulnerability datasets from a wide format (func_before/func_after columns)
to a long format suitable for binary classification training. It creates alternating rows with labels
where vulnerable code is labeled as 1 and fixed/benign code is labeled as 0.

Input Format (CSV):
The input CSV file should contain paired vulnerable/fixed code samples with the following columns:
- func_before: The vulnerable version of the code
- func_after: The fixed/benign version of the code

Example Input (dataset.csv):
func_before,func_after
"def get_user(id):\n    query = 'SELECT * FROM users WHERE id = ' + id\n    return db.execute(query)","def get_user(id):\n    query = 'SELECT * FROM users WHERE id = ?'\n    return db.execute(query, (id,))"

Output Format (CSV):
The script generates a CSV file with the following columns:
- label: Binary label (1 for vulnerable, 0 for benign)
- code: The source code

For each input row, two output rows are created:
1. Row with label=1 containing the func_before (vulnerable) code
2. Row with label=0 containing the func_after (fixed) code

Example Output (converted.csv):
label,code
"1","def get_user(id):\n    query = 'SELECT * FROM users WHERE id = ' + id\n    return db.execute(query)"
"0","def get_user(id):\n    query = 'SELECT * FROM users WHERE id = ?'\n    return db.execute(query, (id,))"

Features:
- Automatic duplicate removal based on func_before/func_after combinations
- Preserves the relationship between vulnerable and fixed code pairs
- All fields are quoted in the output for CSV compatibility

Usage:
# Run the script interactively
python dataset_converter.py

# When prompted, provide the input and output file paths
Input file: data/raw_dataset.csv
Target file: data/processed_dataset.csv

The script will:
1. Read the input CSV file
2. Remove any duplicate pairs
3. Create alternating rows with proper labels
4. Save the converted dataset to the target file

Environment Requirements:
- Python 3.8+
- pandas
"""

import csv
import pandas as pd
import sys
import os


def convert_csv_format(input_file, output_file):
    """
    Convert a CSV file with func_before and func_after columns
    to a format that alternates between label 1 (before) and label 0 (after).
    Removes duplicates based on before and after columns as composite keys.

    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the output CSV file
    """
    try:
        # Read the input CSV file
        df = pd.read_csv(input_file)

        # Define required columns
        required_cols = ['func_before', 'func_after']
        before_col = 'func_before'
        after_col = 'func_after'

        # Check if required columns exist
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Error: Input CSV must contain 'func_before' and 'func_after' columns.")
            print(f"Found columns: {', '.join(df.columns)}")
            print(f"Missing columns: {', '.join(missing_cols)}")
            return False

        # Remove duplicates based on before and after columns as composite keys
        original_count = len(df)
        df_deduplicated = df.drop_duplicates(subset=[before_col, after_col], keep='first')
        duplicates_removed = original_count - len(df_deduplicated)

        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate rows based on func_before/func_after combinations")

        # Create the output CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out, quoting=csv.QUOTE_ALL)

            # Write header
            header = ['label', 'code']
            writer.writerow(header)

            # Write alternating rows
            for _, row in df_deduplicated.iterrows():
                # Write before column with label 1
                writer.writerow(['1', row[before_col]])

                # Write after column with label 0
                writer.writerow(['0', row[after_col]])

        print(f"Successfully converted {input_file} to {output_file}")
        print(
            f"Processed {len(df_deduplicated)} unique input rows (from {original_count} total), created {2 * len(df_deduplicated)} output rows")
        return True

    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        return False


if __name__ == "__main__":
    input_file = input('Input dataset file: ')
    output_file = input('Target dataset file: ')

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist")
        sys.exit(1)

    success = convert_csv_format(input_file, output_file)
    sys.exit(0 if success else 1)
