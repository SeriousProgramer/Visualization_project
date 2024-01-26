from task_interface import Task
import plotly.graph_objs as go

class Task1(Task):
    def get_plot(self):
        # Example plot for Task 1
        #return 
        return go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])])
