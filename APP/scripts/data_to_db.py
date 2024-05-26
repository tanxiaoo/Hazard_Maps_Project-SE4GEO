import os
import pandas as pd
from sqlalchemy import create_engine

# Define database connection
DATABASE_URL = 'postgresql://postgres:941005@localhost:5432/se4g24'
engine = create_engine(DATABASE_URL)


def save_to_database(file_path, engine):
    """
    Save the cleaned data to the database
    """
    data = pd.read_csv(file_path)

    data.to_sql('territory_data', engine, if_exists='replace', index=False)
    print("Data successfully saved to the database")


if __name__ == "__main__":
    cleaned_data_path = os.path.join(os.path.dirname(__file__), '../data/processed/cleaned_italia_pir.csv')
    save_to_database(cleaned_data_path, engine)
