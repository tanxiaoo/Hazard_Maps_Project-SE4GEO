### creating virtual environment
python -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
pip install -r requirement.txt

### the function of different files

#### assets:
- **images**: Contains image resources used in the project.

#### data:
- **processed**: Contains processed data files.
- **raw**: Contains raw data files.

#### notebooks:
- **data_analysis.py**: This is a Jupyter notebook file containing data analysis code.

#### scripts:
- **clean_data.py**: Contains scripts for cleaning data.
- **data_to_db.py**: Contains scripts for importing data into a database.
- **fetch_data.py**: Contains scripts for fetching data from external sources.

#### root directory:
- **app.py**: The main script file of the project.
