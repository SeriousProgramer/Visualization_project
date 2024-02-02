from dash import Dash, html, dcc
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template('CYBORG')

#px.defaults.template = "ggplot2"

#external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
	html.Br(),
	html.P('Finances', className="text-dark text-center fw-bold fs-1"),
    html.Div(children=[
	    dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
			  for page in dash.page_registry.values()]
	),
	dash.page_container
], className="col-11 mx-auto")

if __name__ == '__main__':
	app.run(debug=True)