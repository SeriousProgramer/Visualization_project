from dash import Dash, html, dcc
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Load the CYBORG theme for Plotly figures
load_figure_template('CYBORG')

# Initialize the Dash application
app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

# Define the layout of the application
app.layout = html.Div([
    # Add a break for spacing
	html.Br(),
	# Add a title for the application
	html.P('Credit Classroom', className="text-dark text-center fw-bold fs-1"),
    # Create navigation links for each registered page
    html.Div(children=[
	    dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
			  for page in dash.page_registry.values()]
	),
	# Container for the content of the pages
	dash.page_container
], className="col-10 mx-auto")

# Run the application
if __name__ == '__main__':
	app.run(debug=True)
