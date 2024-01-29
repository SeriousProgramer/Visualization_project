import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Replace with your actual dataframe
# df = pd.DataFrame({
#     'Attribute1': [100, 200, 300, 400],
#     'Attribute2': [50, 150, 250, 350],
#     'NumOfLoans': [1, 2, 3, 4]
# })

dash.register_page(__name__, path='/task34', name="Heatmap")

df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")


layout = html.Div([
    dcc.Dropdown(
        id='attribute-selector',
        options=[{'label': 'Annual_Income', 'value': 'Annual_Income'} for i in range(1, 3)],
        value='Annual_Income'
    ),
    dcc.Graph(id='heatmap-graph'),
])

@callback(
    Output('heatmap-graph', 'figure'),
    [Input('attribute-selector', 'value')]
)
def update_heatmap(selected_attribute):
    # Assuming 'NumOfLoans' is one of the axes and selected attribute is the other
    heatmap_data = df[['Num_of_Loan', selected_attribute]]
    fig = px.density_heatmap(
        heatmap_data,
        x='Num_of_Loan',
        y=selected_attribute,
        nbinsx=20,
        nbinsy=20,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        title='Heatmap of Number of Loans and Monthly Balance',
        xaxis_title='Number of Loans',
        yaxis_title=selected_attribute
    )
    return fig
