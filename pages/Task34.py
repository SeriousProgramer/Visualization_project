import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/task34', name="Heatmap")

df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

layout = html.Div([
    dcc.Graph(id='heatmap-graph'),  # Graph placed at the top
    dcc.Dropdown(
        id='attribute-selector',
        options=[{'label': 'Annual_Income', 'value': 'Annual_Income'} for i in range(1, 3)],
        value='Annual_Income'
    ),
    dcc.Graph(id='scatter-plot-graph')  # Additional scatter plot graph
])

@callback(
    Output('heatmap-graph', 'figure'),
    [Input('attribute-selector', 'value')]
)
def update_heatmap(selected_attribute):
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

@callback(
    Output('scatter-plot-graph', 'figure'),
    [Input('value')]
)

def update_scatter_plot():
    Q1 = df['Interest_Rate'].quantile(0.25)
    Q3 = df['Interest_Rate'].quantile(0.75)
    IQR = Q3 - Q1

    # Filtering Values between Q1-1.5IQR and Q3+1.5IQR
    df_filtered = df.query('(@Q1 - 1.5 * @IQR) <= Interest_Rate <= (@Q3 + 1.5 * @IQR)')

    fig = px.scatter(df_filtered, x='Age', y='Interest_Rate')

    return fig

# Additional callback for scatter plot graph if needed
