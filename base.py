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



# import pandas as pd
# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# from dash import callback_context
# from task1 import Task1
# from task2 import Task2

# # Define a dictionary to map task options to their corresponding Task implementations
# TASKS = {
#     'Understanding Credit Score': Task1(),
#     'Understanding Income': Task2(),
# }
# #df = pd.read_csv("C:\\Users\\yashs\\Downloads\\cleaned_data.csv")
# # df = pd.read_csv(
# #     #"C:\\Users\\20221498\\Desktop\\Visualization\\cleaned_data.csv",
# #     "C:\\Users\\yashs\\Downloads\\cleaned_data.csv",
# # #    "cleaned_data.csv",
# #     delimiter=";",
# #     on_bad_lines="skip",
# # )

# df = pd.read_csv(
#     "cleaned_data.csv",
#     delimiter=";",
#     on_bad_lines="skip",
# )
# # Initialize the Dash app.
# app = dash.Dash(__name__, suppress_callback_exceptions=True)#, allow_duplicate=True)

# # ... [rest of your app's code] ...

# # Define the layout of the app.
# app.layout = html.Div([
#     dcc.Dropdown(
#         id='task-selector',
#         options=[{'label': key, 'value': key} for key in TASKS.keys()],
#         value='Task 1'
#     ),
#     html.Div(id='task-content')  # Placeholder for the task layout
# ])

# Task1.register_callbacks(app, df)
# Task2.register_callbacks(app,df)

# @app.callback(
#     Output('task-content', 'children'),
#     [Input('task-selector', 'value')]
# )
# def switch_task(selected_task):
#     task = TASKS.get(selected_task)
#     if task:
#         # task.register_callbacks(app, df)
#         return task.layout(df)
#     else:
#         return "Please select a task"



# # Run the app.
# if __name__ == '__main__':
#     app.run_server(debug=True)



# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import pandas as pd
# from task1 import Task1
# from task2 import Task2

# # Load your DataFrame
# df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

#  #Define a dictionary to map task options to their corresponding Task implementations
# TASKS = {
#     'Understanding Credit Score': Task1(),
#     'Understanding Income': Task2(),
# }


# app = dash.Dash(__name__, suppress_callback_exceptions=True)

# # Define the layout of the app.
# app.layout = html.Div([
#     dcc.Dropdown(
#         id='task-selector',
#         options=[{'label': key, 'value': key} for key in TASKS.keys()],
#         value='Task 1'  # Make sure this matches one of the keys in TASKS
#     ),
#     html.Div(id='task-content')  # Placeholder for the task layout
# ])

# #This function is outside the tasks and will switch between task layouts
# @app.callback(
#     Output('task-content', 'children'),
#     [Input('task-selector', 'value')]
# )
# def switch_task(selected_task_key):
#     # Clear previous callbacks to prevent duplicates
#     #app.callback_map.clear()

#     # Get the task class from the TASKS dictionary
#     task_instance = TASKS.get(selected_task_key)
#     if task_instance:
#         content = task_instance.layout(df)
#         # Register the task's callbacks with the app
#         task_instance.register_callbacks(app, df)
#         # Return the task's layout to be rendered
#         return content
#     else:
#         return "Please select a task"

# # Start the app
# if __name__ == '__main__':
#     app.run_server(debug=True)
    
    
    
    
    
    
    
    
    
    
# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import pandas as pd
# from task1 import Task1
# from task2 import Task2

# df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

# TASKS = {
#     'Understanding Credit Score': Task1(),
#     'Understanding Income': Task2(),
# }

# app = dash.Dash(__name__, suppress_callback_exceptions=True)

# app.layout = html.Div([
#     dcc.Dropdown(
#         id='task-selector',
#         options=[{'label': key, 'value': key} for key in TASKS.keys()],
#         value='Understanding Credit Score'
#     ),
#     html.Div(id='task-content')
# ])

# @app.callback(
#     Output('task-content', 'children'),
#     [Input('task-selector', 'value')]
# )
# def switch_task(selected_task_key):
#     task_instance = TASKS.get(selected_task_key)
#     if task_instance:
#         # Update the layout based on the task
#         return task_instance.layout(df)
#     else:
#         return "Please select a task"

# # You may register callbacks here if they are common and not task-specific

# if __name__ == '__main__':
#     app.run_server(debug=True)
    