import math
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np

# Register the page in Dash application
dash.register_page(__name__, path='/task34', name="Loans and Debts")

# Read data from a CSV file
df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

# Define the tasks
TASKS = {
    'Num_of_Delayed_Payment': 'Num_of_Delayed_Payment',
    'Annual_Income': 'Annual_Income',
    'Outstanding_Debt': 'Outstanding_Debt',
    'Credit_Utilization_Ratio': 'Credit_Utilization_Ratio',
    'Amount_invested_monthly': 'Amount_invested_monthly',
}

# Layout of the application
layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='attribute-selector',
            options=[{'label': key, 'value': key} for key in TASKS.keys()],
            style={
                'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                'color': 'black',
                'border': '1px solid #ddd',
                'fontWeight': 'bold'
            },
            value='Num_of_Delayed_Payment'
        ),
    ]),
    dcc.Graph(id='heatmap-graph'),
    dcc.Graph(id='scatter-plot-graph')
])

# Callback for updating the heatmap
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
    filtered_data = df[(df['Num_of_Loan'] >= lower_bound2) & (df['Num_of_Loan'] <= 10) & (df[selected_attribute] >= 0) & (df[selected_attribute] <= upper_bound1)]
     
    # Create heatmap
    fig = px.density_heatmap(
        filtered_data,
        x=selected_attribute,
        y='Num_of_Loan',
        nbinsx=10,  # Adjusted for better distribution
        nbinsy=10,  # Adjusted for better distribution
        color_continuous_scale=px.colors.sequential.Plasma  # High-contrast color scale
    )

    # Update layout
    fig.update_layout(
        title=f'Heatmap of Number of Loans and {selected_attribute}',
        yaxis_title='Number of Loans',
        xaxis_title=selected_attribute,
        coloraxis_colorbar=dict(
            title='Count',
            ticktext=['Low', 'Medium', 'High', 'Very High', 'Extreme']  # Custom tick labels
        )
    )

    return fig


# Callback for updating the scatter plot
@callback(
    Output('scatter-plot-graph', 'figure'),
    [Input('attribute-selector', 'value')]
)
def update_scatter_plot(selected_attribute):
    # Group data by Customer_ID
    df_filtered = df.groupby(by=['Customer_ID'])

    # Extract data for scatter plot
    xx = df_filtered['Annual_Income'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 0)
    yy = df_filtered['Total_EMI_per_month'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 0)
    credit_scores = df_filtered['Credit_Score'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown')
    out_debt = df_filtered['Outstanding_Debt'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else 0)

    # Define colors for credit score categories
    credit_score_colors = {
        'Poor': 'orange',
        'Standard': 'grey',
        'Good': 'blue',
    }

    # Map credit scores to colors
    color_mapped = list(map(credit_score_colors.get, credit_scores))

    # Initialize figure
    fig = go.Figure()

    # Add dummy traces for the legend
    for score, color in credit_score_colors.items():
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color=color, size=10),
            name=score
        ))

    # Add scatter plot data
    fig.add_trace(go.Scatter(
        x=xx,
        y=yy,
        mode="markers",
        marker=dict(
            color=color_mapped,
            size=[math.pow(x, 0.35) for x in out_debt],
            opacity=0.7
        ),
        name='A larger size indicates a higher outstanding debt',
    ))

    # Customize layout
    fig.update_layout(
        title="Scatter Plot of Annual Income and EMI per month",
        xaxis_title="Annual Income",
        yaxis_title="EMI Per Month",
        hovermode='closest',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=True
    )

    return fig
