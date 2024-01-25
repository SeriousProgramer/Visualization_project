import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback_context

# Load the dataset
df = pd.read_csv(
    "C:\\Users\\20221498\\Desktop\\Visualization\\cleaned_data.csv",
    delimiter=";",
    on_bad_lines="skip",
)

def string_to_float(dataframe):
    # Replace every comma with a decimal point and convert to float
    dataframe = dataframe.apply(lambda x: x.str.replace(',', '.').astype(float) if x.dtype == 'object' else x)
    return dataframe

# Optional: Clean/Filter the dataset for outliers if necessary
# For instance, you might want to remove rows where 'Num_of_Loan' or 'Num_Bank_Accounts' are extremely high

# Create a scatter plot
def create_scatter_plot(dataframe, credit_mix=None):
    # dataframe = dataframe[dataframe['Num_of_Loan'] < 20]
    # dataframe = dataframe[dataframe['Num_Bank_Accounts'] < 20]
    
    # if credit_mix:
    #     dataframe = dataframe[dataframe['Credit_Mix'] == credit_mix]
    fig = px.scatter(dataframe, x='Outstanding_Debt', y='Num_of_Loan', color='Month', custom_data=(['Name','Month']))
    return fig

# Initialize Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='credit-mix-dropdown',
        options=[{'label': i, 'value': i} for i in df['Credit_Mix'].unique()],
        value=df['Credit_Mix'].unique()[0]
    ),
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='bar-chart')  # New graph component for bar chart
])

# Define callback to update scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('credit-mix-dropdown', 'value')]
)
def update_scatter_plot(selected_credit_mix):
    return create_scatter_plot(df, credit_mix=selected_credit_mix)

# Define callback to update bar chart based on click event
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('scatter-plot', 'clickData'),
     Input('credit-mix-dropdown', 'value')]
)
def display_click_data(clickData, selected_credit_mix):
    # Default empty bar chart
    fig = px.bar()

    # Check if a point in the scatter plot was clicked
       # Check if a point in the scatter plot was clicked
    if clickData:
        # Extract name from the clicked point
        name = clickData['points'][0]['customdata'][0]

        # Filter dataframe for the selected user and credit mix
        filtered_df = df[(df['Name'] == name) & (df['Credit_Mix'] == selected_credit_mix)]

        # Map the month names to their corresponding numbers
        month_order = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        filtered_df['Month_Order'] = filtered_df['Month'].map(month_order)

        # Sort the DataFrame by the 'Month_Order' column
        filtered_df = filtered_df.sort_values('Month_Order')

        # Drop the 'Month_Order' column
        filtered_df = filtered_df.drop('Month_Order', axis=1)

        # Create bar chart showing user's progress
        fig = px.bar(filtered_df, x='Month', y='Num_of_Delayed_Payment', title=f"Credit Limit Change Over Time for {name}")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)