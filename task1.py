import plotly.graph_objs as go
from dash import html, dcc
from dash.dependencies import Output, Input
import pandas as pd

class Task1:
    @staticmethod
    def layout():
        # Example layout for Task 1
        return html.Div([
                html.H3("Task 1 Visualization"),
                html.Div([
                    dcc.Dropdown(
                    id='attribute-selector',
                    options=[{'label': 'box-plot', 'value': 'box'}, {'label' : 'pi', 'value': 'pi'}],
                    value='box-plot'),
                    dcc.Graph(id = 'main-plot', figure = Task1.create_box_plot()),
                    html.Div(id = "left-panel")], style={'width': '60%', 'display': 'inline-block'}),
                html.Div([
                        html.Div([
                            dcc.Graph(
                            id='task1-graph',
                            figure=go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 3, 2])])
                            ),html.Div(id='credit_info')
                            ]),
                        html.Div([
                            dcc.Graph(id='side-plot-2', figure = Task1.create_box_plot()
                            ), html.Div(id='pie_chart') 
                    ]),
                    html.Div(id='right-panel')],style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top'})]
            )
            
    @staticmethod
    def create_box_plot():
        df = pd.DataFrame({
            'data_column': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 5, 6, 7, 8]
        })
        fig = go.Figure(data=[go.Box(y=df['data_column'], boxpoints='all', jitter=0.3, pointpos=-1.8)])
        fig.update_layout(title='Box Plot Example', yaxis=dict(title='Values'), xaxis=dict(title='Data Column'))
        return fig
        #return go.Figure(data=[go.Box(y = self.df[str], boxpoints='all', jitter=0.3, pointpos=-1.8)])
           
    @staticmethod
    def create_pi_chart():
        labels = ['Category A', 'Category B', 'Category C', 'Category D']
        values = [450, 300, 150, 100]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Pie Chart Example')
        return fig
        


    @staticmethod
    def register_callbacks(app):
        @app.callback(
            Output('main-plot', 'figure'),
            [Input('attribute-selector', 'value')]
        )
        def update_output(new_attribute):
            if new_attribute == 'pi':
                return Task1.create_pi_chart()
            else:
                return Task1.create_box_plot()
