# import plotly.graph_objs as go
# import pandas as pd
# import numpy as np
# from dash import Dash, dcc, html, Input, Output

# # Generating a random dataset for demonstration
# np.random.seed(50)
# sample_data = pd.DataFrame({
#     'Category': np.random.choice(['A', 'B', 'C'], size=100),
#     'Values': np.random.randn(100)*100 + 1000,
#     'Ages': np.random.choice(range(20, 60), size=100)
# })

# # Creating a Dash application
# app = Dash(__name__)

# app.layout = html.Div([
#     dcc.Graph(id='bar-plot'),
#     dcc.Slider(
#         id='age-slider',
#         min=sample_data['Ages'].min(),
#         max=sample_data['Ages'].max(),
#         value=sample_data['Ages'].min(),
#         marks={str(age): str(age) for age in sample_data['Ages'].unique()},
#         step=None
#     )
# ])

# @app.callback(
#     Output('bar-plot', 'figure'),
#     [Input('age-slider', 'value')]
# )
# def update_bar_plot(selected_age):
#     # Filtering data based on the selected age from the slider
#     filtered_data = sample_data[sample_data['Ages'] == selected_age]

#     # Creating a bar plot
#     fig = go.Figure(
#         data=[
#             go.Bar(
#                 x=filtered_data['Category'],
#                 y=filtered_data['Values'],
#                 text=filtered_data['Values'],
#                 textposition='auto'
#             )
#         ],
#         layout=go.Layout(
#             title=f'Values by Category for Age {selected_age}',
#             xaxis_title='Category',
#             yaxis_title='Values',
#             template='plotly_dark'
#         )
#     )

#     # Add animation
#     fig.update_traces(marker_color='lightskyblue')
#     fig.update_layout(transition_duration=500)

#     return fig

# # Running the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

# Here's an example of how you can create an animated bar graph in Dash using Plotly.
# Please note that for the animation to work on the first load of the graph, 
# you may need to leverage Plotly's animation capabilities when creating the figure.

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

# Sample DataFrame to use for the bar graph
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 30, 40]
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Animated Bar Graph Example"),
    dcc.Graph(id='animated-bar-graph'),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat} for cat in df['Category'].unique()],
        value='A',  # default value to select
        clearable=False
    )
])

# Callback to update graph based on dropdown selection
@app.callback(
    Output('animated-bar-graph', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_graph(selected_category):
    # Filter the DataFrame based on selected category
    filtered_df = df[df['Category'] == selected_category]

    # Create a bar graph figure with animation
    fig = px.bar(
        filtered_df, 
        x='Category', 
        y='Value', 
        text='Value',
        range_y=[0, df['Value'].max() + 10]  # Setting the y-axis range for better animation effect
    )

    # Adding animation
    fig.update_layout(
        transition={'duration': 500},  # Duration of the animation in milliseconds
        updatemenus=[{
            'buttons': [{
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate'
            }],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]
    )

    # Adding frames for animation
    fig.frames = [go.Frame(data=[go.Bar(x=filtered_df['Category'], y=[0] * len(filtered_df))]),
                  go.Frame(data=[go.Bar(x=filtered_df['Category'], y=filtered_df['Value'])])]

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
