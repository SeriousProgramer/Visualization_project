from tarfile import FilterError
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

dash.register_page(__name__, path='/task5', name="Occupation")


# # Replace with your actual dataframe
# df = pd.DataFrame({
#     'Occupation': ['Doctor', 'Actress', 'Doctor', 'Actress'],
#     'Age': [25, 25, 26, 26],
#     'Debt': [20000, 15000, 21000, 16000],
#     'Income': [5000, 3000, 5200, 3200]
# })

df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

#cleaned = df.dropna()

# Filter out null or empty strings and a specific placeholder from the Occupation column.  _______ and df['Occupation'].notnull

def filter_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]



dfg = df[df['Occupation'].notnull()]
dff = dfg[dfg['Occupation'].str.isalnum()]

layout = html.Div([
    html.H1("Occupation Data Analysis"),
    dcc.Checklist(
        id='occupation-selector',
        options=[{'label': i, 'value': i} for i in (dff['Occupation'].unique().tolist())],
        value=['Engineer', 'Entrepreneur'],  # Default selected
        labelStyle={'display': 'block'}
    ),
    dcc.Graph(id='debt-graph'),
    dcc.Graph(id='income-graph'),
])

@callback(
    [Output('debt-graph', 'figure'),
     Output('income-graph', 'figure')],
    [Input('occupation-selector', 'value')]
)
def update_graph(selected_occupations):
    debt_traces = []
    income_traces = []
    
    for occupation in selected_occupations:
        # Filter the dataframe for the selected occupation and valid ages
        occupation_df = dff[(dff['Occupation'] == occupation) & (dff['Age'] > 0) & (dff['Age'] < 100)]
        
        occupation_df = filter_outliers(occupation_df, 'Annual_Income')
        
        # Group by age and calculate mean debt and median income
        age_group = occupation_df.groupby('Age').agg({'Outstanding_Debt':'mean', 'Annual_Income':'median'}).reset_index()
        
        # Append the traces for plotting
        debt_traces.append(
            go.Scatter(
                x=age_group['Age'],
                y=age_group['Outstanding_Debt'],
                mode='lines+markers',
                name=occupation
            )
        )
        income_traces.append(
            go.Scatter(
                x=age_group['Age'],
                y=age_group['Annual_Income'],
                mode='lines+markers',
                name=occupation
            )
        )
    
    # Define the layout for the debt graph
    debt_fig = go.Figure(
        data=debt_traces,
        layout=go.Layout(
            title='Debt vs Age by Occupation',
            xaxis={'title': 'Age'},
            yaxis={'title': 'Debt'},
            template='plotly_dark'
        )
    )
    
    # Define the layout for the income graph
    income_fig = go.Figure(
        data=income_traces,
        layout=go.Layout(
            title='Income vs Age by Occupation',
            xaxis={'title': 'Age'},
            yaxis={'title': 'Income'},
            template='plotly_dark'
        )
    )
    
    return debt_fig, income_fig





