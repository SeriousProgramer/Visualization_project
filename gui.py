import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Sample data
import pandas as pd
df = pd.DataFrame({
    'Category': ['A', 'B', 'C'],
    'Value': [1, 2, 3]
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1("Interactive Visualization Tool"),
        html.Div(
            children=[
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[
                        {'label': category, 'value': category}
                        for category in df['Category']
                    ],
                    value=df['Category'][0],
                    multi=False,
                    style={'width': '50%'}
                ),
            ],
            style={'margin-bottom': '20px'}
        ),
        dcc.Graph(
            id='bar-chart'
        ),
    ],
    style={'textAlign': 'center', 'margin': '50px'}
)

# Define callbacks to update the graph based on user input
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_graph(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    fig = px.bar(filtered_df, x='Category', y='Value', title=f'Bar Chart for {selected_category}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
