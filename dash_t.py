import dash  # (version 1.11.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
from github import Github
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
from datetime import date, datetime
from pprint import pprint
from json import dumps
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import geopandas as gpd
from PIL import Image
import requests
from io import BytesIO
import plotly.io as pio
import plotly.offline as pyo
import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])  # https://bootswatch.com/default/ for more themes
token = "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"

# ------------------------------------------------------------------------
app.layout = html.Div([
    html.H1("Enter user to be Visualized"),
    html.Div([
        dcc.Input(
            id='user_input',
            type='text',
            debounce=True,           # changes to input are sent to Dash server only on enter or losing focus
          #  pattern=r"^[A-Za-z].*",  # Regex: string must start with letters only
            spellCheck=True,
            inputMode='latin',       # provides a hint to browser on type of data that might be entered by the user.
            name='text',             # the name of the control, which is submitted with the form data
            list='browser',          # identifies a list of pre-defined options to suggest to the user
            n_submit=0,              # number of times the Enter key was pressed while the input had focus
            n_submit_timestamp=-1,   # last time that Enter was pressed
            autoFocus=True,          # the element should be automatically focused after the page loaded
            n_blur=0,                # number of times the input lost focus
            n_blur_timestamp=-1,     # last time the input lost focus.
            # selectionDirection='', # the direction in which selection occurred
            # selectionStart='',     # the offset into the element's text content of the first selected character
            # selectionEnd='',       # the offset into the element's text content of the last selected character
        ),
    ]),
  


    # html.Datalist(id='browser', children=[
    #     html.Option(value="blue"),
    #     html.Option(value="yellow"),
    #     html.Option(value="green")
    # ]),

    html.Br(),
    html.Br(),
    html.Br(),
    
    html.H2("Commits Per Day"),
    dcc.Graph(id='line_plot', animate = True),
    html.Br(),
    html.H2("Sunchart of Languages and Projects"),

    dcc.Graph(id='Sun_plot', animate = True),
    html.Br(),
    html.H2("Time Versus Commits"),

    dcc.Graph(id='Time_Bub_Plot', animate = True),
    html.Br(),
    html.H2("Size Versus Commits"),

    dcc.Graph(id='Size_Bub_Plot', animate = True),
    html.Br(),
    html.H2("Globe of Followers"),
    dcc.Graph(id='Geo_Plot', animate = True)



])

# ------------------------------------------------------------------------
@app.callback(
    
    [Output(component_id='line_plot',component_property='figure'),
    Output(component_id='Sun_plot',component_property='figure'),
    Output(component_id='Time_Bub_Plot',component_property='figure'),
    Output(component_id='Size_Bub_Plot',component_property='figure'),
    Output(component_id='Geo_Plot',component_property='figure')]

    ,
    Input(component_id='user_input', component_property='value'),
     
)
def update_graph(username):
    print(username)

    g = Github(username, token)
    user = g.get_user(username)
    dates = []
    unique = []
    followers  = []
    Lat = []
    Lon = []
    locator = Nominatim(user_agent="myGeocoder")
    df_Rep = pd.DataFrame(columns = ['Name', 'Commits', 'Time', 'Size','Language', 'Date Created'])
    df_Fol = pd.DataFrame(columns = ['Name', 'Avatar', 'Lat', 'Lon'])   
    df_Com = pd.DataFrame(columns = ['Date', 'Commits'])
    print("Searching")
    for repo in user.get_repos(): 
        timeSpent = repo.pushed_at - repo.created_at
        df_Rep = df_Rep.append({'Name': repo.full_name, 'Commits':repo.get_commits().totalCount, 'Time':timeSpent, 'Size':repo.size,'Language':repo.language, 'Date Created': repo.created_at}, ignore_index=True)   
 
        for commit in repo.get_commits():
            x = commit.commit.author.date.strftime('%d/%m/%Y')
            dates.append(x)
            if x not in unique:
                unique.append(x)
    print("Stuck")
  
    #unique.sort(key = lambda date: datetime.strptime(date, '%d/%m/%Y'))
    #unique.sort(key = lambda dt: datetime.strptime(dt, '%d/%m/%Y'))
    
    for item in unique:
        df_Com = df_Com.append({'Date':item, 'Commits':dates.count(item)},ignore_index=True)
    print("Searching Followers")

    for follower in user.get_followers():
        userInfo = (follower.url)
        response = requests.get(follower.avatar_url)
        img = Image.open(BytesIO(response.content))
        location = locator.geocode(follower.location)
        if location is None:
            location = locator.geocode("Champ de Mars, Paris, France")
        df_Fol = df_Fol.append({'Name':follower.name,'Avatar':img,'Lat':location.latitude,'Lon':location.longitude,'Location':follower.location}, ignore_index=True)
    

    print("Lock n Load")
    

#(2021, 10, 7, 11, 10, 5) Need to sort better and add details
    
    print("Making Graphs")
    fig_Line = px.line(df_Com, x='Date', y='Commits')
    print("0")
    figSun = px.sunburst(df_Rep, path=['Language', 'Name'], values = 'Size')
    print("A")
    figBubTime = px.scatter(df_Rep, x = "Time", y = "Commits", color = "Language", hover_data=['Name'])
    print("B")
    figBubSize = px.scatter(df_Rep, x = "Size", y = "Commits", color = "Language", hover_data=['Name'])
    print("C")
    fig_Map = px.scatter_geo(df_Fol, lat="Lat",lon="Lon" , hover_data=["Name","Location"],projection="orthographic")
    print("D")
    return fig_Line,figSun,figBubTime,figBubSize,fig_Map


# ------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

    
# https://youtu.be/VZ6IdRMc0RI