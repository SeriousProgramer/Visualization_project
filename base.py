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



import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from task1 import Task1
from task2 import Task2

# Define a dictionary to map task options to their corresponding Task implementations
TASKS = {
    'Understanding Credit Score': Task1(),
    'Understanding Income': Task2(),
}

df = pd.read_csv("C:\\Users\\yashs\\Downloads\\cleaned_data.csv")

# Initialize the Dash app.
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# ... [rest of your app's code] ...

# Define the layout of the app.
app.layout = html.Div([
    dcc.Dropdown(
        id='task-selector',
        options=[{'label': key, 'value': key} for key in TASKS.keys()],
        value='Task 1'
    ),
    html.Div(id='task-content')  # Placeholder for the task layout
])

Task1.register_callbacks(app)
#Task2.register_callbacks(app)

@app.callback(
    Output('task-content', 'children'),
    [Input('task-selector', 'value')]
)
def switch_task(selected_task):
    task = TASKS.get(selected_task)
    if task:
        return task.layout()
    else:
        return "Please select a task"


# Run the app.
if __name__ == '__main__':
    app.run_server(debug=True)
