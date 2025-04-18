# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into the pandas dataframe
airline_url_dataset = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv'
airline_data =  pd.read_csv(airline_url_dataset, 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})


# Create a dash application layout
app = dash.Dash(__name__)
# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
dashboard_title = html.H1(
    'Airline Performance Dashboard',
    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
)

input_year_component_id = "input-year"
dashboard_year_input = html.Div(
    [ 
        "Input Year: ", 
        dcc.Input(
            id=input_year_component_id, 
            value='2010', 
            type='number', 
            style={'height':'50px', 'font-size': 35}
        ),
    ], 
    style={'font-size': 40}
)

graph_component_id = "line-plot"
bar_graph_component_id = "bar-plot"

app.layout = html.Div(
    children=[
        dashboard_title,
        dashboard_year_input,
        html.Br(),
        html.Br(),
        dcc.Graph(id=graph_component_id),        
        html.Br(),
        html.Br(),
        html.H1('Total number of flights to the destination state split by reporting airline',
                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
        ),
        html.Div(dcc.Graph(id=bar_graph_component_id))
    ]
)


# add callback decorator
@app.callback( Output(component_id=graph_component_id, component_property="figure"),
               Input(component_id=input_year_component_id, component_property="value"))
# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select data based on the entered year
    df =  airline_data[airline_data['Year']==int(entered_year)]
    
    # Group the data by Month and compute the average over arrival delay time.
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    

    fig = go.Figure(
        data=go.Scatter(
            x=line_data['Month'], y=line_data['ArrDelay'], 
            mode='lines', 
            marker=dict(color='green')
        )
    )
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig


@app.callback( Output(component_id=bar_graph_component_id,component_property='figure'),
             Input(component_id=input_year_component_id, component_property='value'))
def get_graph(entered_year):
    df =  airline_data[airline_data['Year']==int(entered_year)]
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()

    fig = px.bar(
        bar_data, 
        x= "DestState", y= "Flights", 
        title='Total number of flights to the destination state split by reporting airline'
    ) 

    fig.update_layout(title='Flights to Destination State')
    fig.update_xaxes(title='DestState')
    fig.update_yaxes(title='Flights')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
