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
    'Annual_Income': 'Annual_Income',
    'Num_of_Delayed_Payment': 'Num_of_Delayed_Payment',
    
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
                            'border': '1px solid #ddd'  # Light gray border
                        },
                    value='Annual_Income'),
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

# @callback(
#     Output('kde-plot', 'figure'),
#     Input('attribute-selector', 'value')  # This input is just to trigger the callback
# )
# def update_kde_plot(selected_attribute):
#     # Create a KDE plot
#     fig = px.density_contour(
#         df, x='Num_of_Loan', y=selected_attribute, 
#         marginal_x='histogram', marginal_y='histogram'
#     )
    
#     # Update layout for aesthetics
#     fig.update_layout(
#         title='KDE of Number of Loans and Monthly Balance',
#         xaxis_title='Number of Loans',
#         yaxis_title=selected_attribute,
#     )
    
#     return fig

@callback(
    Output('scatter-plot-graph', 'figure'),
    [Input('attribute-selector','value')]
)

def update_scatter_plot(selected_attribute):
    df_filtered = df.groupby(by=['Customer_ID'])
   
    xx = df_filtered['Annual_Income'].apply(pd.Series.mode)
    yy = df_filtered['Credit_Utilization_Ratio'].apply(pd.Series.mode)
    credit_scores = df_filtered['Credit_Score'].apply(pd.Series.mode)
    out_debt = df_filtered['Outstanding_Debt'].apply(pd.Series.mode)

    # Normalize outstanding debt for marker intensity
    max_debt = max(out_debt)
    min_debt = min(out_debt)
    # Create a normalized luminance factor where higher debt corresponds to higher luminance
    luminance_factor = [(x - min_debt) / (max_debt - min_debt) for x in out_debt]
    # Use the luminance factor to adjust the opacity, can be between 0.5 (more transparent) and 1 (fully opaque)
    opacities = [0.2 + (lum * 0.3) for lum in luminance_factor]

    my_dict = {
        'Poor': 'orange',
        'Standard': 'grey',
        'Good': 'blue'
    }

    # Apply the color mapping to the list of credit scores
    color_mapped = list(map(my_dict.get, credit_scores))

    fig = go.Figure(
        data=[
            go.Scatter(
                x=xx,
                y=yy,
                mode="markers",
                marker=dict(
                    color=color_mapped,
                    # Adjust opacity for luminance effect
                    opacity = opacities,
                    size = [math.pow(x, 0.4) for x in out_debt]                    
                    #brightness=[math.pow(x, 0.4) for x in out_debt]  # Use size to further emphasize the effect
                )
            )
        ],
        layout=go.Layout(
            title="Scatter Plot of Annual Income and Total EMI per month",
            xaxis_title="Annual Income",
            yaxis_title="Total EMI per Month"
        )
    )

    # Customize layout for better interaction
    fig.update_layout(
        hovermode='closest',  # Shows tooltips for the closest points
        margin=dict(l=40, r=40, t=40, b=40)  # Adjust margins if needed
    )

    return fig
# Additional callback for scatter plot graph if needed
