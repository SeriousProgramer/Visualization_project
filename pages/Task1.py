import plotly.graph_objs as go
import dash
from dash import html, dcc, callback
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Register the page in Dash with a specific path and name
dash.register_page(__name__, path='/', name="Understanding Credit Score")

# Read data from a CSV file
df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

# Class containing methods for creating different types of plots
class com:           
    @staticmethod
    def create_box_plot(df, value):
        # Group entries by Customer_ID
        grouped = df.groupby(by=['Customer_ID'])

        # Create a box plot
        fig = go.Figure(data=[go.Box(y=grouped[value].apply(pd.Series.mode),
                                     x=grouped['Credit_Score'].apply(pd.Series.mode),
                                     boxpoints=False,
                                     pointpos=-1.8,
                                     quartilemethod='exclusive')])

        # Customize the layout
        fig.update_layout(
            title='Box Plot',
            yaxis=dict(title=value),
            xaxis=dict(title='Credit Score'),
            template='plotly_dark',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig.update_traces(quartilemethod="exclusive")
        return fig

    @staticmethod
    def kde_plot(df, attribute):
        # Filter the dataframe and calculate mode
        df_filtered = df.dropna().groupby(by=['Customer_ID'])
        df_mode = list(df_filtered[attribute].apply(pd.Series.mode))

        # Create KDE plot
        fig = ff.create_distplot([df_mode], [attribute], show_hist=False, colors=['Orange'])

        # Update layout
        fig.update_layout(
            title='KDE of ' + attribute,
            xaxis_title=attribute,
            yaxis_title='Density'
        )
        return fig

    @staticmethod
    def text_box(attribute):
        # Text descriptions for each attribute
        descriptions = {
            'Num_of_Loan': 'The number of loans taken from the bank',
            'Credit_Score': "A categorical measure of an individual's creditworthiness",
            'Annual_Income': "The total income of a customer each year",
            'Credit_Utilization_Ratio': "The percentage of available credit currently being used",
            'Amount_invested_monthly': "The monthly amount invested by the customer",
            'Num_of_Delayed_Payment': "The number of loan payments delayed beyond their due date",
            'Outstanding_Debt': "The total amount owed",
            'Interest_Rate': "The percentage of debt charged for its use"
        }
        return descriptions.get(attribute, "")

    @staticmethod
    def plot_bar_graph(df, attribute):
        # Filter to remove outliers
        Q1 = df[attribute].quantile(0.25)
        Q3 = df[attribute].quantile(0.75)
        IQR = Q3 - Q1
        filter = (df[attribute] >= Q1 - 1.5 * IQR) & (df[attribute] <= Q3 + 1.5 * IQR)
        filtered_df = df.loc[filter]

        # Ensure non-negative values
        filtered_df = filtered_df[filtered_df[attribute] >= 0]

        # Count non-zero values
        counts = filtered_df[attribute].value_counts().reset_index()
        counts.columns = [attribute, 'count']
        counts = counts[counts['count'] > 0]

        # Create bar graph
        fig = go.Figure(data=[go.Bar(x=counts[attribute], y=counts['count'])])

        # Customize layout
        fig.update_layout(
            title=f'Count of {attribute} values',
            xaxis_title=attribute,
            yaxis_title='Count',
            template='plotly_dark',
            xaxis=dict(type='category')
        )
        return fig

# Dictionary of tasks
TASKS = {
    'Num_of_Loan': 'Num_of_Loan',
    'Annual_Income': 'Annual_Income',
    'Num_of_Delayed_Payment': 'Num_of_Delayed_Payment',
    'Outstanding_Debt': 'Outstanding_Debt',
    'Credit_Utilization_Ratio': 'Credit_Utilization_Ratio',
    'Amount_invested_monthly': 'Amount_invested_monthly',
    'Interest_Rate': 'Interest_Rate'
}

# Layout of the Dash application
layout = html.Div([
    # Dropdown for attribute selection
    dcc.Dropdown(
        id='attribute-selector',
        options=[{'label': key, 'value': key} for key in TASKS.keys()],
        style={
            'backgroundColor': 'rgba(255, 255, 255, 0.5)',
            'color': 'black',
            'border': '1px solid #ddd',
            'fontWeight': 'bold'                      
        },
        value='Num_of_Loan'
    ),
    # Div for the main plot
    html.Div([
        dcc.Graph(id='main-plot', figure=com.create_box_plot(df, 'Num_of_Loan')),
        html.Div(id="left-panel")
    ], style={'width': '45%', 'display': 'inline-block', 'padding': '0px'}),
    # Div for the side plot and text box
    html.Div([
        html.Div(
            "The number of loans taken from the bank",
            id='text-box',
            style={
                'textAlign': 'center',
                'color': 'black',
                'fontSize': 24,
                'margin': 'auto',
                'padding': '20px',
                'fontWeight': 'bold',
                'border': '1px solid #ddd',
                'borderRadius': '8px',
                'width': '75%',
                'backgroundColor': 'rgba(255, 255, 255, 0.5)'
            }
        ),
        html.Div([
            dcc.Graph(id='side-plot-2', figure=com.kde_plot(df, 'Num_of_Loan')),
            html.Div(id='pie_chart') 
        ]),
        html.Div(id='right-panel')
    ], style={'width': '55%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '0px'})
], style={'padding': '0px'})

# Callback function to update plots and text box based on selected attribute
@callback(
    [Output('main-plot', 'figure'),
     Output('side-plot-2', 'figure'),
     Output('text-box', 'children')],
    [Input('attribute-selector', 'value')]
)
def update_output(new_attribute):
    return com.create_box_plot(df, new_attribute), com.kde_plot(df, new_attribute), com.text_box(new_attribute)
