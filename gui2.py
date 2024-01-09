import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import seaborn as sns

# Load the Iris dataset for demonstration purposes
iris = sns.load_dataset('iris')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1("Interactive Visualization Tool"),
        html.Div(
            children=[
                dcc.Dropdown(
                    id='x-axis-dropdown',
                    options=[
                        {'label': col, 'value': col}
                        for col in iris.columns
                    ],
                    value='species',
                    multi=False,
                    style={'width': '50%'},
                    placeholder='Select X-axis variable'
                ),
                dcc.Dropdown(
                    id='y-axis-dropdown',
                    options=[
                        {'label': col, 'value': col}
                        for col in iris.columns
                    ],
                    value='sepal_length',
                    multi=False,
                    style={'width': '50%'},
                    placeholder='Select Y-axis variable'
                ),
                dcc.Dropdown(
                    id='plot-type-dropdown',
                    options=[
                        {'label': 'Scatter Plot', 'value': 'scatter'},
                        {'label': 'Box Plot', 'value': 'box'}
                    ],
                    value='scatter',
                    multi=False,
                    style={'width': '50%'},
                    placeholder='Select Plot Type'
                ),
            ],
            style={'margin-bottom': '20px'}
        ),
        dcc.Graph(
            id='plot-output'
        ),
    ],
    style={'textAlign': 'center', 'margin': '50px'}
)

# Define callbacks to update the scatter plot or box plot based on user input
@app.callback(
    Output('plot-output', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('plot-type-dropdown', 'value')]
)
def update_plot(x_axis, y_axis, plot_type):
    if plot_type == 'scatter':
        fig = px.scatter(iris, x=x_axis, y=y_axis, color='species', title=f'Scatter Plot for {x_axis} vs {y_axis}')
    elif plot_type == 'box':
        fig = px.histogram(iris, x=x_axis, y=y_axis, color='species', title=f'Box Plot of {y_axis} by {x_axis}')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
