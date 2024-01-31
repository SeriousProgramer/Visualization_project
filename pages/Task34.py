import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

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
   
    xx = df_filtered['Annual_Income'].apply(pd.Series.mode)
    yy = df_filtered['Total_EMI_per_month'].apply(pd.Series.mode)
    credit_scores = df_filtered['Credit_Score'].apply(pd.Series.mode)
    out_debt = df_filtered['Outstanding_Debt'].apply(pd.Series.mode)

    my_dict = {
        'Poor': 'orange',
        'Standard': 'blue',
        'Good': 'violet'
    }

    # Apply the color mapping to the list of credit scores
    color_mapped = list(map(my_dict.get, credit_scores))

    fig = go.Figure(
        data=[
            go.Scatter(x=xx, y=yy, mode="markers", marker=dict(color=color_mapped, size=out_debt/100)),
        ],
        layout=go.Layout(title="Your Chart Title")
    )
    return fig

# Additional callback for scatter plot graph if needed
