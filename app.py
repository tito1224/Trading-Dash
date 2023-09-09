# Import libraries
import pandas as pd
import numpy as np 
from matplotlib.pyplot import figure
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from numpy import intp
import plotly.express as px
import pandas as pd 
from datetime import date,timedelta

# initialize app
app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP]) # the 'suppress_callback_exceptions=True' param should only be used for multi page apps

# load config layout styles
colors = {
    'background':'#f5f5f5',
    #'text': '#7FDBFF',
    'text':'#000000'
}

# load sample data
data = pd.read_csv("sampledata.csv")
tickerNames = data.columns[1:]
data = pd.melt(data, id_vars='Date', value_vars=tickerNames)
data.columns = ["Date","Name","Price"]
lstStockDropdown = data.loc[:,"Name"].unique()
lstInitialAssets = ["GOOG","AMZN"]

# make a figure of historical data
# will be used as input in the layout section
figHistoricalData = px.line(data, x = "Date", y = "Price",color="Name")

# add a few more designs to the figure (ie text and background color)
figHistoricalData.update_layout(
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],
    font_color=colors['text']
)

# use dcc.markdown() if you want to display this text
markdown_text = '''
Please note that the data is pulled from Yahoo Finance using the yfinance library (open source).
'''

####################### Layout ###############################
app.layout = html.Div([
    html.H1(children = "Trading Dashboard", # generates a <h1>Hello Dash</h1> HTML element
    style = {
        'textAlign':'center',
        'color':colors['text']
    }),

    # little useless text - might remove after
    html.Div(children='Data pulled using the yfinance library', style={
        'textAlign':'center',
        'color':colors['text']
    }),

    # graph of historical data  
    html.Div([
        dcc.Graph(
            id = 'historical-data-graph',
            figure=figHistoricalData
        )
    ],style = {'padding':'0px 0px 0px 40px'}),

    # options to choose assets & date
    html.Div([

        html.Div([
            # pick assets
            html.H4("Choose your assets"),
            dcc.Dropdown(lstStockDropdown,lstInitialAssets,id = "select-asset",multi=True)    
        ],style={"margin":"0px 0px"}),
        
        html.Div([
            html.H4("Choose a date range"),
            
            # choose date range
            dcc.DatePickerRange(
            # when I have better data I will use this!
            #start_date=date.today()-timedelta(30),
            #end_date = date.today() 
            id='historical-data-date-range',
            start_date = "2019-03-01",
            end_date = "2019-06-01")
        ],style={"margin":"10px 0px"})
    ], style={'width': '40%', 'display': 'flex','flex-direction':'column','padding':'0px 80px'})


]
    
    )


##################################### App Callbacks ####################################

# change graph based on inputs 
@app.callback(
    Output('historical-data-graph','figure'), # the output of the app is the 'figure' property of the dcc.Graph
    Input('select-asset','value'), # the "value" property of the dcc.Dropwdown is the input of the app
    Input('historical-data-date-range', 'start_date'),
    Input('historical-data-date-range', 'end_date'))
def update_figure(lstAssetName,startDate, endDate):
    filtered_df = data[data.Name.isin(lstAssetName)]
    # notice how the callback does not modify the original data, it only creates copies of the dataframe by filtering using pandas
    # IMPORTANT: the callbacks should never modify variables outside of their scope. If your callbacks moidfy global state, then one user's session might affect the next user's session
    
    # filter by date
    filtered_df = filtered_df[(filtered_df.Date >= startDate) & (filtered_df.Date <= endDate)]

    fig = px.line(filtered_df, x = "Date", y = "Price",color="Name")
    fig.update_layout(transition_duration=500) # we are turning on transitions with layout.transition to give an idea of how the dataset evolves with time
    # transitions allow the chart to update from one state to the next smoothly, as if it were animated 
    return fig





if __name__ == '__main__':
    app.run_server(debug=True)
