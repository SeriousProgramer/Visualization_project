from task_interface import Task
import plotly.graph_objs as go

class Task2(Task):
    def get_plot(self):
        # Example plot for Task 2
        return go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[3, 1, 2], mode='lines+markers')])
