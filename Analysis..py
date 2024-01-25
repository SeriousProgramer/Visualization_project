# import pandas as pd
# import plotly.express as px
# import dash
# from dash import callback_context
# from dash import dcc, html
# from dash.dependencies import Input, Output

# app = dash.Dash(__name__)

# # Load your dataset
# df = pd.read_csv("C:\\Users\\yashs\\Downloads\\cleaned_data.csv")

# # Convert non-numeric columns to numeric
# non_numeric_columns = df.select_dtypes(exclude=['number']).columns
# for column in non_numeric_columns:
#     df[column] = pd.to_numeric(df[column], errors='coerce')

# # Calculate the correlation matrix
# correlation_matrix = df.corr()

# # Threshold for high correlation
# threshold = 0.7

# # Find high correlation pairs
# high_correlation_pairs = [
#     (correlation_matrix.columns[i], correlation_matrix.columns[j])
#     for i in range(len(correlation_matrix.columns))
#     for j in range(i+1, len(correlation_matrix.columns))
#     if abs(correlation_matrix.iloc[i, j]) > threshold
# ]

# # Assume we have a function to generate figures based on a dataset
# def create_figure(pair, df):
#     # Extract the variable names from the pair
#     variable1, variable2 = pair
    
#     # Create a scatter plot
#     fig = px.scatter(
#         df, 
#         x=variable1, 
#         y=variable2, 
#         title=f'Scatter Plot of {variable1} vs. {variable2}',
#         labels={variable1: variable1, variable2: variable2} # This can be customized or omitted
#     )
    
#     # Customizations can be added here, e.g. setting axis labels, themes, etc.
#     fig.update_layout(
#         xaxis_title=variable1,
#         yaxis_title=variable2,
#         margin=dict(l=40, r=40, t=40, b=40),
#         hovermode='closest'
#     )
    
#     return fig

# app.layout = html.Div([
#     # Main plot area
#     html.Div([
#         dcc.Graph(id='main-plot', figure=create_figure(high_correlation_pairs[0], df))
#     ], style={'width': '75%', 'display': 'inline-block'}),

#     # Side plots area
#     html.Div([
#         dcc.Graph(id='side-plot-1', figure=create_figure(high_correlation_pairs[1], df)),
#         dcc.Graph(id='side-plot-2', figure=create_figure(high_correlation_pairs[2], df)),
#         # More graphs can be added here
#     ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'})
# ])

# # Callbacks to update main plot based on clicks on side plots
# @app.callback(
#     Output('main-plot', 'figure'),
#     [Input('side-plot-1', 'clickData'), Input('side-plot-2', 'clickData')],
#     [dash.callback_context]
# )
# def display_click_data(clickData1, clickData2, context):
#     if not context.triggered:
#         # No plot clicked yet, return default plot
#         return create_figure(high_correlation_pairs[0], df)

#     # Determine which input was triggered
#     trigger_id = context.triggered[0]['prop_id'].split('.')[0]
#     if trigger_id == 'side-plot-1':
#         return create_figure(high_correlation_pairs[1], df)
#     elif trigger_id == 'side-plot-2':
#         return create_figure(high_correlation_pairs[2], df)
#     else:
#         return dash.no_update
 
# # ... (other parts of your code) ...

# @app.callback(
#     Output('main-plot', 'figure'),
#     [Input('side-plot-1', 'n_clicks'), Input('side-plot-2', 'n_clicks')],
# )
# def display_click_data(n_clicks_1, n_clicks_2):
#     ctx = callback_context
#     if not ctx.triggered:
#         # No plot clicked yet, return default plot
#         return create_figure(high_correlation_pairs[0], df)

 
# def display_click_data(n_clicks_1, n_clicks_2):
#     # Use callback_context inside the function to get the triggered input
#     ctx = callback_context
#     if not ctx.triggered:
#         # No plot clicked yet, return default plot
#         return create_figure(high_correlation_pairs[0])
#     # Determine which input was triggered
#     trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     if trigger_id == 'side-plot-1':
#         return create_figure(high_correlation_pairs[1], df)
#     elif trigger_id == 'side-plot-2':
#         return create_figure(high_correlation_pairs[2], df)
#     else:
#         return dash.no_update


       

# #Run the app
# if __name__ == 'main':
#     app.run_server(debug=True)


import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Load your dataset
df = pd.read_csv("C:\\Users\\yashs\\Downloads\\cleaned_data.csv")

print(df)

# Convert non-numeric columns to numeric
non_numeric_columns = df.select_dtypes(exclude=['number']).columns
for column in non_numeric_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Calculate the correlation matrix
correlation_matrix = df.corr()


# Threshold for high correlation
threshold = 0.7

# Find high correlation pairs
high_correlation_pairs = [
    (correlation_matrix.columns[i], correlation_matrix.columns[j])
    for i in range(len(correlation_matrix.columns))
    for j in range(i+1, len(correlation_matrix.columns))
    if abs(correlation_matrix.iloc[i, j]) > threshold
]

print(high_correlation_pairs)

# Function to generate figures based on a dataset
def create_figure(pair, df):
    variable1, variable2 = pair
    fig = px.scatter(df, x=variable1, y=variable2, title=f'Scatter Plot of {variable1} vs. {variable2}')
    fig.update_layout(xaxis_title=variable1, yaxis_title=variable2, margin=dict(l=40, r=40, t=40, b=40), hovermode='closest')
    return fig

app.layout = html.Div([
    html.Div([dcc.Graph(id='main-plot', figure=create_figure(high_correlation_pairs[0], df))], style={'width': '60%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='side-plot-1', figure=create_figure(high_correlation_pairs[1], df)),
        dcc.Graph(id='side-plot-2', figure=create_figure(high_correlation_pairs[2], df)),
    ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top'})
])

@app.callback(
    Output('main-plot', 'figure'),
    [Input('side-plot-1', 'clickData'), Input('side-plot-2', 'clickData')]
)
def display_click_data(clickData1, clickData2):
    ctx = dash.callback_context
    if not ctx.triggered:
        # No plot clicked yet, return default plot
        return create_figure(high_correlation_pairs[0], df)
    # Determine which input was triggered
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger_id == 'side-plot-1' and clickData1:
        return create_figure(high_correlation_pairs[1], df)
    elif trigger_id == 'side-plot-2' and clickData2:
        return create_figure(high_correlation_pairs[2], df)
    else:
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)

