from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
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
                    config={"editable": True, "edits": {"axisTitleText": True}}
                ),
                html.Div(id="left-panel"),
            ], style={"width": "60%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="radar-chart")
            ], style={"width": "40%", "display": "inline-block"})
            
        ])

    @staticmethod
    def create_stacked_histogram(df):

        # Remove rows where 'Monthly_Inhand_Salary' is NaN or infinite

       
    
       

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

    @staticmethod
    def create_radar_chart(df, clicked_bin,credit_score):
        # Clean the DataFrame to exclude non-finite values before calculating bin edges
        clean_df = df.dropna(subset=['Monthly_Inhand_Salary'])

        # Get the bin edges using clean data
        bin_edges = np.histogram_bin_edges(clean_df['Monthly_Inhand_Salary'], bins='auto')

        # Find the index of the bin to which the clicked value belongs
        bin_index = np.digitize(clicked_bin, bin_edges) - 1

        # Safety check if clicked_bin is out of range, return an empty figure
        if bin_index < 0 or bin_index >= len(bin_edges) - 1:
            return go.Figure()

        # Get the range for the clicked bin
        clicked_range = bin_edges[bin_index:bin_index+2]
        categories = ['Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan']

        # Filter the DataFrame for the selected range and calculate medians
        selected_df = df[(df['Monthly_Inhand_Salary'] >= clicked_range[0]) & (df['Monthly_Inhand_Salary'] <= clicked_range[1]) & (df['Credit_Score'] == credit_score)]
        selected_medians = selected_df[categories].median()

        total_medians = df[categories].median()

        # Calculate the percentages for the radar chart
        percent_medians = (selected_medians / total_medians) * 100

        # Define the categories for the radar chart
        
        # Create the radar chart
        fig = go.Figure(data=go.Scatterpolar(
            r=percent_medians[categories].tolist(),
            theta=categories,
            fill='toself'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 200]
                )),
            showlegend=False
        )

        return fig

    @staticmethod
    def register_callbacks(app, df):
       

        @app.callback(
            Output("radar-chart", "figure"),
            [Input("main-plot", "clickData")]
        )
        def display_radar_chart(clickData):
            if clickData:
                clicked_point = clickData['points'][0]

                clicked_bin = clickData['points'][0]['x']
                credit_score = clicked_point['curveNumber']
                credit_score_mapping = {0: 'Poor', 1: 'Standard', 2: 'Good'}  # Update this mapping as per your traces
                selected_credit_score = credit_score_mapping.get(credit_score, 'Poor')  # Default to 'Poor' if not found
                return Task2.create_radar_chart(df, clicked_bin,selected_credit_score)
            return go.Figure()

# Additional code for Dash app initialization and running may go below this line
# ...
