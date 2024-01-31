import plotly.graph_objs as go
import dash
from dash import html, dcc, callback
from dash.dependencies import Output, Input
import pandas as pd


dash.register_page(__name__, path='/', name="Understanding Credit Score")

df = pd.read_csv("cleaned_data.csv", delimiter=";", on_bad_lines="skip")

#############################################################################
class com:           
    @staticmethod
    def create_box_plot(df, value):        
            # Group entries by person
            grouped = df.groupby(by=['Customer_ID'])
            
            # Order Credit Score properly
            # credit_order = ["Poor", "Standard", "Good"]
            # grouped['Credit_Score'] = pd.Categorical(grouped['Credit_Score'], credit_order, ordered=True)
            
            
            # Create a box plot with 'data_column' on the x-axis
            fig = go.Figure(data=[go.Box(y = grouped[value].apply(pd.Series.mode),
                    x = grouped['Credit_Score'].apply(pd.Series.mode), boxpoints=False, pointpos=-1.8, quartilemethod = 'exclusive')])

            # Customize the layout
            fig.update_layout(
                title='Box Plot',
                yaxis=dict(title=value),
                xaxis=dict(title='Credit_Score'),
                # Adjust the width of the whiskers
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20)  # Reduced margins

            )
            fig.update_traces(quartilemethod="exclusive")
            return fig
            #return go.Figure(data=[go.Box(y = self.df[str], boxpoints='all', jitter=0.3, pointpos=-1.8)])
            
    @staticmethod
    def create_bar_plot(df, value):
            labels = ['Category A', 'Category B', 'Category C', 'Category D']
            values = [450, 300, 150, 100]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(title='Pie Chart Example',             margin=dict(l=20, r=20, t=40, b=20)  # Reduced margins
)
            return fig

######################################################################################################


TASKS = {
    'Annual_Income': 'Annual_Income',
    'Num_of_Delayed_Payment': 'Num_of_Delayed_Payment',
    'Num_of_Loan' : 'Num_of_Loan' ,
    'Outstanding_Debt' : 'Outstanding_Debt',
    'Credit_Utilization_Ratio' : 'Credit_Utilization_Ratio',
    'Amount_invested_monthly' : 'Amount_invested_monthly' ,
    'Credit_History_Age' : 'Credit_History_Age',
    'Interest_Rate' : 'Interest_Rate'
    }

#Annual Income, Num of Loan, Number of delayed payment, outstanding debt, credit utilization ratio
#Amount_invested_monthly, Credit_History_Age


layout = html.Div([
                html.H3("Task 1 Visualization"),
                dcc.Dropdown(
                    id='attribute-selector',
                    options=[{'label': key, 'value': key} for key in TASKS.keys()],
                    value='Num_of_Loan'),
                html.Div([
                    ##dropdown
                    dcc.Graph(id = 'main-plot', figure = com.create_box_plot(df, 'Num_of_Loan')),
                    html.Div(id = "left-panel")], style={'width': '60%', 'display': 'inline-block','padding': '0px'} ),
                html.Div([
                        html.Div(
                           "THis is some texr",style={
                                        'textAlign': 'center',
                                        'color': '#0074D9',
                                        'fontSize': 24,
                                        'margin': 'auto',
                                        'padding': '20px',
                                        'fontWeight': 'bold',
                                        'border': '1px solid #ddd',
                                        'borderRadius': '8px',
                                        'width': '50%',
                                        'backgroundColor': '#f9f9f9'
                                    }
                            ),
                        html.Div([
                            dcc.Graph(id='side-plot-2', figure = com.create_bar_plot(df, '')
                            ), html.Div(id='pie_chart') 
                    ]),
                    html.Div(id='right-panel')],style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top','padding': '0px'} )], style ={'padding' : '0px'}
            )



@callback(
    [Output('main-plot', 'figure'),
     Output('side-plot-2' , 'figure')],
    [Input('attribute-selector', 'value')]
)
def update_output(new_attribute):
    return com.create_box_plot(df, new_attribute), com.create_bar_plot(df, new_attribute)


        


    
