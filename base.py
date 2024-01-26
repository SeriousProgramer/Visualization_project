# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# from abc import ABC, abstractmethod

# # Define the interface for tasks as an abstract base class
# class TaskInterface(ABC):
#     @abstractmethod
#     def create_plot(self):
#         pass

# # Concrete implementation of TaskInterface for a specific task
# class Task1(TaskInterface):
#     def create_plot(self):
#         # Return a sample plotly figure for demonstration
#         return go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 3, 2])])




import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from task1 import Task1
from task2 import Task2

# Define a dictionary to map task options to their corresponding Task implementations
TASKS = {
    'OPT1': Task1(),
    'OPT2': Task2(),
}

# Initialize the Dash app.
app = dash.Dash(__name__)

# Define the layout of the app.
app.layout = html.Div([
    dcc.Checklist(
        id='theme-switch',
        options=[{'label': 'Switch to Dark Mode', 'value': 'DARK'}],
        value=[]
    ),    
    html.Div([
        dcc.Dropdown(
            id='plot-selector',
            options=[{'label': key, 'value': key} for key in TASKS.keys()],
            value='OPT1'  # Default value
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '20px'}),
    html.Div([
        dcc.Graph(id='plot-area')
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '20px'}),
    html.Link(id='theme-link', rel='stylesheet', href='https://codepen.io/chriddyp/pen/brPBPO.css')
])

# Callback to update the plot area based on the selected task
@app.callback(
    Output('plot-area', 'figure'),
    [Input('plot-selector', 'value')]
)
def update_plot(selected_task_key):
    # Get the plot from the selected task
    task = TASKS.get(selected_task_key)
    return task.get_plot() if task else {}

# Callback to switch themes
@app.callback(
    Output('theme-link', 'href'),
    [Input('theme-switch', 'checked')]
)
def update_theme(checked):
    if checked:
        return 'https://codepen.io/chriddyp/pen/brPBPO.css'  # Dark theme URL
    else:
        return 'https://codepen.io/chriddyp/pen/bWLwgP.css'  # Light theme URL

# Run the app.
if __name__ == '__main__':
    app.run_server(debug=True)
