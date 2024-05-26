import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go

# Setup db connection (generic connection path : 'postgresql://user:password@localhost:5432/mydatabase')
DATABASE_URL = 'postgresql://postgres:000000@localhost:5432/se4g24'
engine = create_engine(DATABASE_URL)


def load_data():
    """
    Load cleaned data from the database
    """
    query = "SELECT * FROM territory_data"
    data = pd.read_sql(query, engine)
    return data


def create_plot(data):
    """
    Create Plotly chart
    """
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data.columns),
                    fill_color='pale turquoise',
                    align='left'),
        cells=dict(values=[data[col] for col in data.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    return fig


if __name__ == "__main__":
    data = load_data()
    print(data.head())
    fig = create_plot(data)
    fig.show()
