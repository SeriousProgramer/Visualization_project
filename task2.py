# from task_interface import Task
# import plotly.graph_objs as go

# class Task2(Task):
    
#     def get_hist(self): 
#         return
    
    
#     def get_plot(self, df):
        
#         #plot the hist on left side
        
#         #click point
        
#         # Example plot for Task 2
#         # return go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[3, 1, 2], mode='lines+markers')])
#         pass


from dash import html, dcc
import plotly.graph_objs as go

class Task2:
    def layout(self):
        layout = html.Div([
            html.H3('Understanding Income Visualization'),
            dcc.Graph(
                figure=go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[2, 3, 1])])
            )
        ])
        return layout

