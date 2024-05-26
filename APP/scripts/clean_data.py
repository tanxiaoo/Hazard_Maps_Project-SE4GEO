import os
import pandas as pd
import json

# Define file paths
raw_data_path = os.path.join(os.path.dirname(__file__), '../data/raw/italia_pir.csv')
processed_data_path = os.path.join(os.path.dirname(__file__), '../data/processed/cleaned_italia_pir.csv')

# Create saving directory (if not exist)
os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)


def clean_data(input_path, output_path):
    """
    Clean data by keeping specific columns and renaming column names
    """
    with open(input_path, 'r', encoding='utf-8') as file:
        raw_data = file.read()

    data = json.loads(raw_data)
    df = pd.DataFrame([data])
    df = df[['ar_kmq', 'pop_res011', 'ed_tot']]
    df.columns = ['territory', 'population', 'buildings']

    # Save the cleaned data
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")


if __name__ == "__main__":
    clean_data(raw_data_path, processed_data_path)
