# from sre_parse import State
from turtle import color
from dash import html, dcc, callback
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import pandas as pd

dash.register_page(__name__, path='/task2', name="Understanding Income")

#########Loading Dataset##############
df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

df1 = None
######################################

class support :
    
    @staticmethod
    def create_stacked_histogram(df):

        # Remove rows where 'Monthly_Inhand_Salary' is NaN or infinite

       
    
       

        fig = go.FigureWidget()

        poor_df = df[df["Credit_Score"] == "Poor"]
        # Add a Histogram trace for 'data_column1'
        fig.add_trace(
            go.Histogram(
                x=poor_df["Monthly_Inhand_Salary"],
                name="Monthly_Inhand_Salary",
                marker_color="indianred",
                opacity=0.75,
                cliponaxis=False
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
                cliponaxis=False
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
                cliponaxis=False
            )
        )

        # Set the barmode to 'stack'
        fig.update_layout(
            barmode="stack",
            title="Stacked Histogram Example",
            yaxis=dict(title="Count", fixedrange=False, autorange = True,),
            xaxis=dict(title='Monthly Income'),
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
        fig = go.Figure()

        # Filter the DataFrame for the selected range and calculate medians
        selected_df = df[(df['Monthly_Inhand_Salary'] >= clicked_range[0]) & (df['Monthly_Inhand_Salary'] <= clicked_range[1]) & (df['Credit_Score'] == credit_score)]
        if df1 is not None:
            selected_medians = df1[categories].median()
            total_medians = df[categories].median()
            percent_medians = (selected_medians / total_medians) * 100
            fig.add_trace(go.Scatterpolar(
            r=percent_medians[categories].tolist(),
            theta=categories,
            fill='toself',
            marker = dict(color = 'blue')
        ))
            
        selected_medians = selected_df[categories].median()

        increment(selected_df)
        total_medians = df[categories].median()

        # Calculate the percentages for the radar chart
        percent_medians = (selected_medians / total_medians) * 100

        # Define the categories for the radar chart
        # Create the radar chart
        fig.add_trace(go.Scatterpolar(
            r=percent_medians[categories].tolist(),
            theta=categories,
            fill='toself',
            marker = dict(color = 'orange')
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 200]
                )),
            showlegend=True
        )

        return fig

###################################################################3   
def increment(dfs):
     global df1
     df1 = dfs
 
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
            ], style={"width": "40%", "display": "inline-block"}),
     dcc.RangeSlider(
        id='my-range-slider',
        min=df['Monthly_Inhand_Salary'].min(),
        max=df['Monthly_Inhand_Salary'].max(),
        value=[df['Monthly_Inhand_Salary'].min(), df['Monthly_Inhand_Salary'].max()],
          dots=True,             # True, False - insert dots, only when step>1
            disabled=False,        # True,False - disable handle
            pushable=2,            # any number, or True with multiple handles
            updatemode='mouseup',  # 'mouseup', 'drag' - update value method
            included=True,         # True, False - highlight handle
            vertical=False,        # True, False - vertical, horizontal slider
            verticalHeight=900,    # hight of slider (pixels) when vertical=True
            className='None',
            tooltip={'always_visible':True,  # show current slider values
                     'placement':'bottom'},
            marks={1: '1', 2: '2', 3: '3', 4: '4', 5: '5'},
             allowCross=False
    )
            
            
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
    Output('m-plot','figure'),
    [Input('my-range-slider','value')]
)

def build_graph(salary):
    changed_df = df[(df['Monthly_Inhand_Salary'] >= salary[0]) & (df['Monthly_Inhand_Salary'] <= salary[1])]
    return support.create_stacked_histogram(changed_df)