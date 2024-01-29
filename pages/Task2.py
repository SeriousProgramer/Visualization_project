# from sre_parse import State
from dash import html, dcc, callback
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import pandas as pd

dash.register_page(__name__, path='/task2', name="Understanding Income")

#########Loading Dataset##############
df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")
######################################

class support :
    
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
            xaxis=dict(rangeslider=dict(visible=True), title='Monthly Income'),
        #, type='-'
            
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
        categories = ['Age', 'Num_of_Delayed_Payment', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan']

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

###################################################################3   

 
layout = html.Div([
            html.H3("Task 2 Visualization"),
            html.Div([
                dcc.Graph(
                    id="m-plot",
                    figure=support.create_stacked_histogram(df),
                    config={"editable": True, "edits": {"axisTitleText": True}}
                ),
                html.Div(id="left-panel"),
            ], style={"width": "60%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="radar-chart")
            ], style={"width": "40%", "display": "inline-block"})
            
        ])

   
@callback(
            Output("radar-chart", "figure"),
            [Input("m-plot", "clickData")]
        )
def display_radar_chart(clickData):
            if clickData:
                clicked_point = clickData['points'][0]

                clicked_bin = clickData['points'][0]['x']
                credit_score = clicked_point['curveNumber']
                credit_score_mapping = {0: 'Poor', 1: 'Standard', 2: 'Good'}  # Update this mapping as per your traces
                selected_credit_score = credit_score_mapping.get(credit_score, 'Poor')  # Default to 'Poor' if not found
                return support.create_radar_chart(df, clicked_bin,selected_credit_score)
            return go.Figure()
      
@callback(
            Output('m-plot', 'figure'),
            [Input('m-plot', 'relayoutData')],
            [State('m-plot', 'figure')]
        )
def update_y_axis_range(relayoutData, figure):
            # Convert the figure JSON into a plotly Figure object
            fig = go.Figure(figure)
            if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
                # Extract the current x-axis range
                x_start, x_end = relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']

                # Filter the DataFrame based on the current x-axis range
                filtered_df = df[(df['Monthly_Inhand_Salary'] >= x_start) & (df['Monthly_Inhand_Salary'] <= x_end)]

                # Calculate the maximum y value (count) for the new filtered range
                # If there are multiple histograms stacked, you should sum their counts
                max_count = 0
                for trace in fig.data:
                    if trace.name == "Monthly_Inhand_Salary":  # Assuming this is the name of your histogram trace
                        counts, _ = np.histogram(
                            trace.x, bins=np.histogram_bin_edges(filtered_df['Monthly_Inhand_Salary'], bins='auto')
                        )
                        max_count = max(max_count, counts.max())

                # Update the y-axis range to accommodate the maximum count
                new_yaxis_range = [0, max_count + max_count * 0.1]  # Add 10% padding
                fig.update_layout(yaxis_range=new_yaxis_range)

            # Return the updated figure
            return fig.to_dict()

      

# Additional code for Dash app initialization and running may go below this line
# ...
