# import dash
# from dash import dcc, html, callback
# from dash.dependencies import Input, Output
# import plotly.express as px
# import pandas as pd

# # Replace with your actual dataframe
# # df = pd.DataFrame({
# #     'Attribute1': [100, 200, 300, 400],
# #     'Attribute2': [50, 150, 250, 350],
# #     'NumOfLoans': [1, 2, 3, 4]
# # })

# dash.register_page(__name__, path='/task34', name="Heatmap")

# df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")


# layout = html.Div([
#     dcc.Dropdown(
#         id='attribute-selector',
#         options=[{'label': 'Annual_Income', 'value': 'Annual_Income'} for i in range(1, 3)],
#         value='Annual_Income'
#     ),
#     dcc.Graph(id='heatmap-graph'),
# ])

# @callback(
#     Output('heatmap-graph', 'figure'),
#     [Input('attribute-selector', 'value')]
# )
# def update_heatmap(selected_attribute):
#     # Assuming 'NumOfLoans' is one of the axes and selected attribute is the other
#     heatmap_data = df[['Num_of_Loan', selected_attribute]]
#     fig = px.density_heatmap(
#         heatmap_data,
#         x='Num_of_Loan',
#         y=selected_attribute,
#         nbinsx=20,
#         nbinsy=20,
#         color_continuous_scale='Viridis'
#     )
#     fig.update_layout(
#         title='Heatmap of Number of Loans and Monthly Balance',
#         xaxis_title='Number of Loans',
#         yaxis_title=selected_attribute
#     )
#     return fig



import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np


dash.register_page(__name__, path='/task34', name="Heatmap")

df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

layout = html.Div([
    dcc.Graph(id='kde-plot'),  # Graph placed at the top
    dcc.Dropdown(
        id='attribute-selector',
        options=[{'label': 'Annual_Income', 'value': 'Annual_Income'} for i in range(1, 3)],
        value='Annual_Income'
    ),
    dcc.Graph(id='scatter-plot-graph')  # Additional scatter plot graph
])

# @callback(
#     Output('heatmap-graph', 'figure'),
#     [Input('attribute-selector', 'value')]
# )
# def update_heatmap(selected_attribute):
#     heatmap_data=df #.groupby(by=['Customer_ID'])
#     heatmap_data = heatmap_data[['Num_of_Loan', selected_attribute]]
    
#     fig = px.density_heatmap(
#         heatmap_data,
#         x='Num_of_Loan',
#         y=selected_attribute,
#         nbinsx=20,
#         nbinsy=20,
#         color_continuous_scale='Viridis'
#     )
#     fig.update_layout(
#         title='Heatmap of Number of Loans and Monthly Balance',
#         xaxis_title='Number of Loans',
#         yaxis_title=selected_attribute
#     )
#     return fig

@callback(
    Output('kde-plot', 'figure'),
    Input('attribute-selector', 'value')
)
def update_kde_plot(selected_attribute):
    var = [df['Num_of_Loan'].dropna()]  # Make sure to drop NA values for the plot
    fig = ff.create_distplot(var, ['Num_of_Loan'], show_hist=False, colors=['Orange'])
    
    # Update layout for aesthetics
    fig.update_layout(
        title='KDE of Number of Loans',
        xaxis_title='Number of Loans',
        yaxis_title='Density'
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
