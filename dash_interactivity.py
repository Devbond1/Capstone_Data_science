# Import required libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load SpaceX dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min and max payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize Dash App
app = dash.Dash(__name__)

# Extract unique launch sites
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
]

# Define Layout
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),

    # TASK 1: Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Success Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    # TASK 3: Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Success Payload Scatter Chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2: Callback Function for Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    """ Update the pie chart based on the selected launch site. """
    
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', 
                     title="Total Successful Launches for All Sites")
    else:
        # Filter for selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count success (class=1) vs failure (class=0) for the selected site
        filtered_df = filtered_df.groupby('class').size().reset_index(name='count')
        fig = px.pie(filtered_df, values='count', names='class', 
                     title=f"Launch Success Rate for {entered_site}")
    
    return fig

# TASK 4: Callback Function for Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(entered_site, payload_range):
    """ Update the scatter plot based on selected site and payload range. """
    
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Success count on Payload mass for all sites'
        )
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title=f"Success count on Payload mass for {entered_site}"
        )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
