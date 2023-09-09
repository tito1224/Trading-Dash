# Import libraries
import pandas as pd
import numpy as np 
from matplotlib.pyplot import figure
import dash
from dash import dcc, html, Input, Output, State
from numpy import intp
import plotly.express as px
import pandas as pd 

# initialize app
app = dash.Dash(__name__,suppress_callback_exceptions=True) # the 'suppress_callback_exceptions=True' param should only be used for multi page apps

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
data = data.loc[data.Name != "AAPL",:]

# make a figure!
fig = px.line(data, x = "Date", y = "Price",color="Name")

fig.update_layout(
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],
    font_color=colors['text']
)

markdown_text = '''
Please note that the data is pulled from Yahoo Finance using the yfinance library (open source).
'''

####################### Layout ###############################
app.layout = html.Div(style = {'backgroundColor':colors['background']},children = [
    html.H1(children = "Trading Dashboard", # generates a <h1>Hello Dash</h1> HTML element
    style = {
        'textAlign':'center',
        'color':colors['text']
    }),

    html.Div(children='Data pulled using the yfinance library', style={
        'textAlign':'center',
        'color':colors['text']
    }),

    dcc.Graph(
        id = 'historical-data-graph',
        figure=fig
    ),

    dcc.Dropdown(lstStockDropdown,data.loc[:,"Name"].unique(),id = "select-asset",multi=True) 


]
    
    )





if __name__ == '__main__':
    app.run_server(debug=True)
