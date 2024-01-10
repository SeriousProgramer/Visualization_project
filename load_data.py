import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import plotly.express as px

# replace <path on you computer to file, e.g. C:\....> with the path to the file
df = pd.read_csv(
    "C:\\Users\\20221498\\Desktop\\Visualization\\cleaned_data.csv",
    delimiter=";",
    on_bad_lines="skip",
)
dfs = df.head(50)

fig = px.scatter(dfs, x='Month', y='Num_of_Delayed_Payment', title='Scatter plot of Number of Delayed Payments over Month')

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)



