import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import plotly.express as px

# replace <path on you computer to file, e.g. C:\....> with the path to the file
df = pd.read_csv(
    "C:\\Users\\20221498\\Desktop\\Visualization\\cleaned_data.csv",
    delimiter=";",
    on_bad_lines="skip",
)
dfs = df.head(50)

def get_top_correlations(df, columns, target_column, n=6):
    # Select only the specified columns
    df = df[columns].copy()

    # Remove commas and convert to floats
    for column in columns:
       
        if df[column].dtypes == 'object':
            df.loc[:, column] = pd.to_numeric(df[column].str.replace(',', ''), errors='coerce')
       


# Remove outliers
        

    # Check if the target column exists in the DataFrame
    if target_column not in df.columns:
        raise ValueError(f"Column '{target_column}' does not exist in the DataFrame.")

    # Calculate the correlation matrix
    corr_matrix = df.corr()

    # Get the correlations with the target column
    correlations = corr_matrix[target_column]

    # Get the absolute values of the correlations
    abs_correlations = correlations.abs()

    # Sort the correlations by their absolute values in descending order
    sorted_correlations = abs_correlations.sort_values(ascending=False)

    # Exclude the correlation of the target column with itself
    sorted_correlations = sorted_correlations.drop(target_column)

    # Get the top n correlations
    top_correlations = sorted_correlations.head(n)

    return top_correlations

# Specify the columns to include in the correlation analysis
columns = ['Num_of_Loan', 'Monthly_Balance', 'Amount_invested_monthly', 'Total_EMI_per_month', 'Credit_Utilization_Ratio', 'Outstanding_Debt', 'Num_Credit_Inquiries', 'Changed_Credit_Limit', 'Num_of_Delayed_Payment', 'Delay_from_due_date', 'Interest_Rate', 'Num_Credit_Card', 'Num_Bank_Accounts', 'Annual_Income']

# Use the function to get the top 6 correlations with 'Num_of_loans'
top_correlations = get_top_correlations(df, columns, 'Num_of_Loan', 6)
print(top_correlations)
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

# Create a Dash app
app = dash.Dash(__name__)

# Get the values of the first person in the database
first_person_values = df.loc[1, top_correlations.index]

# Convert the values to a numeric type
first_person_values = pd.to_numeric(first_person_values, errors='coerce')

Q1 = df['Monthly_Balance'].astype(int).quantile(0.25)
Q3 = df['Monthly_Balance'].astype(int).quantile(0.75)
IQR = Q3 - Q1

# Define the range [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
dfs = df[(df['Monthly_Balance'] >= lower_bound) & (df['Monthly_Balance'] <= upper_bound)]
# Create a radar plot
fig = go.Figure(data=go.Scatter(x=df['Num_of_Loan'], y=dfs, mode='markers'))



# Add the plot to the app
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




print(dfs)





