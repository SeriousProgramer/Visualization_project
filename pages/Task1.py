import plotly.graph_objs as go
import dash
from dash import html, dcc, callback
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


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
                xaxis=dict(title='Credit Score'),
                # Adjust the width of the whiskers
                template='plotly_dark',
                margin=dict(l=20, r=20, t=40, b=20)  # Reduced margins

            )
            fig.update_traces(quartilemethod="exclusive")
            return fig
            #return go.Figure(data=[go.Box(y = self.df[str], boxpoints='all', jitter=0.3, pointpos=-1.8)])


    @staticmethod
    def kde_plot(df, attribute):
        
        df_filtered = (df.dropna()).groupby(by=['Customer_ID'])
    
        df_mode = list(df_filtered[attribute].apply(pd.Series.mode))
        
        var = [df_mode]
        
        fig = ff.create_distplot(var, [attribute], show_hist=False, colors=['Orange'])
        # Update layout for aesthetics and set the x-axis range
        fig.update_layout(
            title='KDE of ' + attribute,
            xaxis_title=attribute,
            yaxis_title='Density'
        )
        
        return fig

    
    @staticmethod
    def text_box(attribute):
        if attribute == 'Num_of_Loan':
            return 'The number of loans taken from the bank'
        elif(attribute == 'Credit_Score'):
            return "A categorical measure of an individual's creditworthiness"
        elif(attribute == 'Annual_Income'):
            return "The total income of a customer each year"
        elif(attribute == 'Credit_Utilization_Ratio'):
            return "The percentage of available credit currently being used"
        elif(attribute == 'Amount_invested_monthly'):
            return ""
        elif(attribute == 'Num_of_Delayed_Payment'):
            return "The number of loan payments delayed beyond their due date"
        elif(attribute == 'Outstanding_Debt'):
            return "The total amount owed"
        elif(attribute == 'Interest_Rate'):
            return "The percentage of debt charged for its use"

    @staticmethod
    def plot_bar_graph(df, attribute):
        # Filter to remove outliers
        Q1 = df[attribute].quantile(0.25)
        Q3 = df[attribute].quantile(0.75)
        IQR = Q3 - Q1
        filter = (df[attribute] >= Q1 - 1.5 * IQR) & (df[attribute] <= Q3 + 1.5 * IQR)
        filtered_df = df.loc[filter]

        # Ensure the attribute is non-negative
        filtered_df = filtered_df[filtered_df[attribute] >= 0]

        # Get the value counts for non-zero counts
        counts = filtered_df[attribute].value_counts().reset_index()
        counts.columns = [attribute, 'count']
        counts = counts[counts['count'] > 0]

        # Create the bar graph
        fig = go.Figure(data=[go.Bar(x=counts[attribute], y=counts['count'])])

        # Customize the layout
        fig.update_layout(
            title=f'Count of {attribute} values',
            xaxis_title=attribute,
            yaxis_title='Count',
            template='plotly_dark',
            # Set x-axis to 'category' to treat as discrete values
            xaxis=dict(type='category')
        )

        return fig
   

######################################################################################################


TASKS = {
    'Num_of_Loan' : 'Num_of_Loan' ,
    'Annual_Income': 'Annual_Income',
    'Num_of_Delayed_Payment': 'Num_of_Delayed_Payment',
    'Outstanding_Debt' : 'Outstanding_Debt',
    'Credit_Utilization_Ratio' : 'Credit_Utilization_Ratio',
    'Amount_invested_monthly' : 'Amount_invested_monthly' ,
    'Interest_Rate' : 'Interest_Rate'
    }





layout = html.Div([
                dcc.Dropdown(
                    id='attribute-selector',
                    options=[{'label': key, 'value': key} for key in TASKS.keys()],
                    style={
                            'backgroundColor': 'rgba(255, 255, 255, 0.5)',  # Semi-transparent white
                            'color': 'black',
                            'border': '1px solid #ddd' , # Light gray border
                            'fontWeight': 'bold'                      
                        },
                    value='Num_of_Loan'),
                html.Div([
                    ##dropdown
                    dcc.Graph(id = 'main-plot', figure = com.create_box_plot(df, 'Num_of_Loan')),
                    html.Div(id = "left-panel")], style={'width': '45%', 'display': 'inline-block','padding': '0px'} ),
                html.Div([
                        html.Div(
                           "The number of loans taken from the bank",style={
                                        'textAlign': 'center',
                                        'color': 'black',
                                        'fontSize': 24,
                                        'margin': 'auto',
                                        'padding': '20px',
                                        'fontWeight': 'bold',
                                        'border': '1px solid #ddd',
                                        'borderRadius': '8px',
                                        'width': '75%',
                                        'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                                    },id='text-box'
                            ),
                        html.Div([
                            dcc.Graph(id='side-plot-2', figure = com.kde_plot(df, 'Num_of_Loan')
                            ), html.Div(id='pie_chart') 
                    ]),
                    html.Div(id='right-panel')],style={'width': '55%', 'display': 'inline-block', 'vertical-align': 'top','padding': '0px'} )], style ={'padding' : '0px'}
            )



@callback(
    [Output('main-plot', 'figure'),
     Output('side-plot-2' , 'figure'),
     Output('text-box', 'children')],
    [Input('attribute-selector', 'value')]
)
def update_output(new_attribute):
    
    return com.create_box_plot(df, new_attribute), com.kde_plot(df, new_attribute), com.text_box(new_attribute)




        


    
