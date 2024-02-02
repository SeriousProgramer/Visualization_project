import math
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np


dash.register_page(__name__, path='/task34', name="Loans and Debts")

df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

TASKS = {
    'Num_of_Delayed_Payment': 'Num_of_Delayed_Payment',
    'Annual_Income': 'Annual_Income',
    'Outstanding_Debt' : 'Outstanding_Debt',
    'Credit_Utilization_Ratio' : 'Credit_Utilization_Ratio',
    'Amount_invested_monthly' : 'Amount_invested_monthly' ,
    }


layout = html.Div([
    html.Div([
                    dcc.Dropdown(
                    id='attribute-selector',
                    options=[{'label': key, 'value': key} for key in TASKS.keys()],
                    style={
                            'backgroundColor': 'rgba(255, 255, 255, 0.5)',  # Semi-transparent white
                            'color': 'black',
                            'border': '1px solid #ddd' , # Light gray border
                            'fontWeight': 'bold'
                        },
                    value='Num_of_Delayed_Payment'),
            ]),
    dcc.Graph(id='heatmap-graph'),  # Graph placed at the top
    dcc.Graph(id='scatter-plot-graph')  # Additional scatter plot graph
])

@callback(
    Output('heatmap-graph', 'figure'),
    [Input('attribute-selector', 'value')]
)
def update_heatmap(selected_attribute):
    # Filter data by the IQR of the selected attribute
    lower_bound1 = df[selected_attribute].quantile(0.25)
    upper_bound1 = df[selected_attribute].quantile(0.75)
    lower_bound2 = df['Num_of_Loan'].quantile(0.25)
    upper_bound2 = df['Num_of_Loan'].quantile(0.75)
    filtered_data = df[(df['Num_of_Loan'] >= lower_bound2)& (df['Num_of_Loan'] <= 10) & (df[selected_attribute] >= 0) & (df[selected_attribute] <= upper_bound1) ]
     
    fig = px.density_heatmap(
    filtered_data,
    x=selected_attribute,
    y='Num_of_Loan',
    nbinsx=10,  # Adjusted for better distribution
    nbinsy=10,  # Adjusted for better distribution
    color_continuous_scale=px.colors.sequential.Plasma,  # High-contrast color scale
   
)

    fig.update_layout(
        title=f'Heatmap of Number of Loans and {selected_attribute}',
        yaxis_title='Number of Loans',
        xaxis_title=selected_attribute,
        coloraxis_colorbar=dict(
            title='Count',
            # tickvals=[0, 50, 100, 150, 200],  # Adjust tick values as needed
            ticktext=['Low', 'Medium', 'High', 'Very High', 'Extreme']  # Custom tick labels
        )
    )

    return fig


@callback(
    Output('scatter-plot-graph', 'figure'),
    [Input('attribute-selector','value')]
)

def update_scatter_plot(selected_attribute):
    

    df_filtered = df.groupby(by=['Customer_ID'])

    xx = df_filtered['Annual_Income'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 0)
    yy = df_filtered['Credit_Utilization_Ratio'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 0)
    credit_scores = df_filtered['Credit_Score'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown')
    out_debt = df_filtered['Outstanding_Debt'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 0)

    credit_score_colors = {
        'Poor': 'orange',
        'Standard': 'grey',
        'Good': 'blue',
        
        
        
    }

    # Map credit scores to colors
    color_mapped = list(map(credit_score_colors.get, credit_scores))

    fig = go.Figure()

    
    
    

    # Add dummy traces for the legend
    count =0
    for score, color in credit_score_colors.items():
        count+=1
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color=color, size=10),
            name=score
        ))
    # Add the actual scatter plot data
    fig.add_trace(go.Scatter(
        x=xx,
        y=yy,
        mode="markers",
        marker=dict(
            color=color_mapped,
            size=[math.pow(x, 0.4) for x in out_debt],
            opacity=0.7
        ),
        name='A larger size indicates a higher outstanding debt',
    ))

    # Customize layout
    fig.update_layout(
        title="Scater Plot of Annual Income and Credit Utilization Ratio",
        xaxis_title="Annual Income",
        yaxis_title="Credit Utilization Ratio",
        hovermode='closest',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=True
    )

    return fig

