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
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


class Task2:
   

    @staticmethod
    def layout(df):
        return html.Div([
            html.H3("Task 2 Visualization"),
            html.Div([
                dcc.Graph(
                    id="main-plot",
                    figure=Task2.create_stacked_histogram(df),
                    # Enable relayoutData to track changes in layout
                    config={"editable": True, "edits": {"axisTitleText": True}}
                ),
                html.Div(id="left-panel"),
            ], style={"width": "60%", "display": "inline-block"}),
        ])

    @staticmethod
    def create_stacked_histogram(df, x_range=None):
        # df = pd.read_csv(
        #     "C:\\Users\\20221498\\Desktop\\Visualization\\cleaned_data.csv",
        #     delimiter=";",
        #     on_bad_lines="skip",
        # )
        
        fig = go.Figure()

        poor_df = df[df["Credit_Score"] == "Poor"]
        # Add a Histogram trace for 'data_column1'
        fig.add_trace(
            go.Histogram(
                x=poor_df["Monthly_Inhand_Salary"],
                name="Monthly_Inhand_Salary",
                marker_color="indianred",
                opacity=0.75,
            )
        )
        standard_df = df[df["Credit_Score"] == "Standard"]

        # Add a Histogram trace for 'data_column2'
        fig.add_trace(
            go.Histogram(
                x=standard_df["Monthly_Inhand_Salary"],
                name="Monthly_Inhand_Salary",
                marker_color="lightsalmon",
                opacity=0.75,
            )
        )

        good_df = df[df["Credit_Score"] == "Standard"]

        # Add a Histogram trace for 'data_column2'
        fig.add_trace(
            go.Histogram(
                x=good_df["Monthly_Inhand_Salary"],
                name="Monthly_Inhand_Salary",
                marker_color="gray",
                opacity=0.75,
            )
        )

        # Set the barmode to 'stack'
        fig.update_layout(
            barmode="stack",
            title="Stacked Histogram Example",
            yaxis=dict(title="Count"),
            xaxis=dict(rangeslider=dict(visible=True), type='-', title='Monthly Income'),

            
        )
        fig.update_layout(title_text="Time series with range slider and selectors")
        

        return fig
       
        # return go.Figure(data=[go.Box(y = self.df[str], boxpoints='all', jitter=0.3, pointpos=-1.8)])
   
    @staticmethod
    def register_callbacks(app, df):
        @app.callback(
            Output("main-plot", "figure"),
            [Input("main-plot", "relayoutData")]
        )
        def update_layout(relayoutData):
            
            if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
                x_range = [relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']]
                return Task2.create_stacked_histogram(df, x_range)
            else:
                # This will be called initially and whenever the relayoutData does not contain x-axis range info
                return Task2.create_stacked_histogram(df)


# Additional code for Dash app initialization and running
