# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot

import pandas as pd
import dash
from dash import html
import plotly.express as px

data = pd.read_csv("datasets/lab_7_spacex_launch_dash.csv")

# Create a dash app
app = dash.Dash(__name__)

dash_title = html.H1(
    "SpaceX Launch Records Dashboard", style = {"textAlign": "center", "font-size": 24}
)

# TASK 1: Add a Launch Site Drop-down Input Component
opts = []
for opt in data["Launch Site"].unique():
   opts.append({"label": opt, "value": opt})

dropdown_ls_comp_id = "site-dropdown"
dropdown_ls_options = [
    {"label": "All sites", "value": "All"},
    *opts # alternative to spread operator
]


dropdown_ls_comp = dash.dcc.Dropdown(
    id = dropdown_ls_comp_id,
    options = dropdown_ls_options,
    value="All",
    placeholder="Select a Launch Site here",
    searchable=True
)
output_pie_chart_id = "success-pie-chart"

# TASK 3: Add a Range Slider to Select Payload
range_slider_comp_id = "payload-slider"
min_value = data["Payload Mass (kg)"].min()
max_value = data["Payload Mass (kg)"].max()
step = 500
range_slider_comp = dash.dcc.RangeSlider(
    id= range_slider_comp_id,
    min = min_value,
    max = max_value + step,
    step = step,
    marks={
        0:"0",
        2121: "Q1: 2121",
        3412.5: "Q2: 3412.5",
        5042.5: "Q3: 5042.5",
        9600: "max: 9600"
    },
    value=[min_value, max_value]
)
output_scatter_plot_id = "success-payload-scatter-chart"


# Define app layout
app.layout = html.Div([
    dash_title,
    html.Div([
        html.Label("Select Launch Site"),
        dropdown_ls_comp,
        dash.dcc.Graph(id=output_pie_chart_id)
    ]),
    html.Div([
        html.Label("Payload Range"),
        range_slider_comp,
        dash.dcc.Graph(id=output_scatter_plot_id)
    ]),
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(
    dash.Output(component_id=output_pie_chart_id, component_property="figure"),
    dash.Input(component_id=dropdown_ls_comp_id, component_property="value")
)
def get_pie_chart(entered_site):
    filtered_df = data
    if entered_site != "All":
        filtered_df = data[data["Launch Site"] == entered_site]
        fig = px.pie(
            filtered_df[["Launch Site", "class"]], 
            names="class",
            title="Succeed by Launch Site"
        )
        return fig
    else:
        fig = px.pie(
            filtered_df[["Launch Site", "class"]], 
            values="class", 
            names="Launch Site",
            title="Succeed by Launch Site"
        )
        return fig
    
@app.callback(
    dash.Output(component_id=output_scatter_plot_id, component_property="figure"),
    [
        dash.Input(component_id=dropdown_ls_comp_id, component_property="value"),
        dash.Input(component_id=range_slider_comp_id, component_property="value")
    ]
)
def get_pie_chart(entered_site, range):
    min = range[0]   
    max = range[1]   
    filtered_df = data[(data["Payload Mass (kg)"] <= max) & (data["Payload Mass (kg)"] >= min) ]

    if entered_site != "All":
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color = "Booster Version Category",
            title="Correlation between Payload and Success"
        )

        return fig
    else: 
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color = "Booster Version Category",
            title="Correlation between Payload and Success"
        )
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)

