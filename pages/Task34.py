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
    heatmap_data=df #.groupby(by=['Customer_ID'])
    heatmap_data = heatmap_data[['Num_of_Loan', selected_attribute]]
    
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
    [Input('attribute-selector','value')]
)

def update_scatter_plot(selected_attribute):
    df_filtered = df.groupby(by=['Customer_ID'])
    
    # Q1 = df['Total_EMI_per_month'].quantile(0.25)
    # Q3 = df['Total_EMI_per_month'].quantile(0.75)
    # IQR = Q3 - Q1

    # # Filtering Values between Q1-1.5IQR and Q3+1.5IQR
    # df_filtered = df.query('(@Q1 - 1.5 * @IQR) <= Total_EMI_per_month <= (@Q3 + 1.5 * @IQR)')
    # Q1 = df_filtered['Annual_Income'].quantile(0.25)
    # Q3 = df_filtered['Annual_Income'].quantile(0.75)
    # IQR = Q3 - Q1

    # Filtering Values between Q1-1.5IQR and Q3+1.5IQR
    # df_filtered = df_filtered.query('(@Q1 - 1.5 * @IQR) <= Annual_Income <= (@Q3 + 1.5 * @IQR)')
    
    fig =   px.scatter(df_filtered, y='Total_EMI_per_month', x='Annual_Income', size='Outstanding_Debt', color='Credit_Score', hover_data=['Total_EMI_per_month', 'Annual_Income', 'Outstanding_Debt', 'Credit_Score'])

    return fig

# Additional callback for scatter plot graph if needed
