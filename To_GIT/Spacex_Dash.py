# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 15:10:37 2024

@author: ArthurRodrigues
"""

# -*- coding: utf-8 -*-
"""
SAPCEX DASH

"""



import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

#import data
URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(URL1)
spacex_df.drop(columns='Unnamed: 0', inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Spacex Launch Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
"""dropdown_options = [id = 'dropdown-statistics',
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]"""

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),#May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
              id='site-dropdown',
              options=[{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                       {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                       {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                       {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                       {'label': 'All', 'value': 'All'}],
              value='All',
              placeholder="Select a Launch Site here",
              searchable=True
              ),
        dcc.Graph(id='success-pie-chart'),
        html.Label("Payload range (Kg):"),
        dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       2500: '2500',
                       5000: '5000', 
                       7500: '7500',
                       10000: '10000'},
                value=[0,10000]),
        dcc.Graph(id='success-payload-scatter-chart'),
        
    ])
    ])
#TASK 2.4: Creating Callbacks

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.loc[spacex_df['Launch Site']==entered_site]
    filtered_df = filtered_df['class'].value_counts()#.groupby(filtered_df['Launch Site'])
    if entered_site == 'All':
        data = spacex_df.groupby(spacex_df['Launch Site'])['class'].sum()
        fig = px.pie(data, values=data.values, 
        names=data.index, 
        title='Total Success for all sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, values=filtered_df.values, 
        names=filtered_df.index, 
        title=f'Total Success for site {entered_site}')
        return fig
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload):
    filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
    filtered_df = filtered_df.loc[filtered_df['Payload Mass (kg)'] <= payload[1]]
    if entered_site == 'All':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', 
        color="Booster Version Category",                 
        #names=filtered_df['class'], 
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.scatter(filtered_df,  x='Payload Mass (kg)', y='class', 
        color="Booster Version Category",                 
        #names=filtered_df['class'], 
        title=f'Correlation between Payload and Success for {entered_site}')
        return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True,port=3003)