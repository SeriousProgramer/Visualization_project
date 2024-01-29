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

# Filter out null or empty strings and a specific placeholder from the Occupation column.  _______
dfg = df[df['Occupation'].notnull()]
dff = dfg[dfg['Occupation'].str.isalnum()]['Occupation'].unique()

layout = html.Div([
    html.H1("Occupation Data Analysis"),
    dcc.Checklist(
        id='occupation-selector',
        options=[{'label': i, 'value': i} for i in (dff)],
        value=df['Occupation'].unique().tolist(),  # Default all selected
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
        filtered_df = df[df['Occupation'] == occupation]
        debt_traces.append(
            go.Scatter(
                x=filtered_df['Age'],
                y=filtered_df['Outstanding_Debt'],
                mode='lines+markers',
                name=occupation
            )
        )
        income_traces.append(
            go.Scatter(
                x=filtered_df['Age'],
                y=filtered_df['Annual_Income'],
                mode='lines+markers',
                name=occupation
            )
        )
    debt_fig = {
        'data': debt_traces,
        'layout': go.Layout(
            title='Debt vs Age by Occupation',
            xaxis={'title': 'Age'},
            yaxis={'title': 'Debt'}
        )
    }
    income_fig = {
        'data': income_traces,
        'layout': go.Layout(
            title='Income vs Age by Occupation',
            xaxis={'title': 'Age'},
            yaxis={'title': 'Income'}
        )
    }
    return debt_fig, income_fig

