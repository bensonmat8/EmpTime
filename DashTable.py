# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:24:43 2020

@author: piproadm
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
import socket
import plotly.graph_objects as go

conn=sqlite3.connect('employee.db')

app =  dash.Dash()

app.layout =  html.Div([html.H1('AM Schedule'),
                        html.Div([dcc.DatePickerSingle(id='date')]),
                        html.Div([dcc.Graph(id='schedule')],
                                 style=dict(height='450px'))
                        ],style=dict(fontFamily='helvetica',fontSize=18))

@app.callback(Output('schedule','figure'),
              [Input('date','date')])
def table(date):
    conn=sqlite3.connect('employee.db')
    df_ = pd.read_sql('select * from am_schedule', conn)
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_[i] for i in df_.columns],
                   fill_color='lavender',
                   align='left'))
        ])
    return fig

if __name__=='__main__':
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)
    print(f"Goto:\nhttp://{IPAddr}:3152\n")
    app.run_server(host='0.0.0.0',port=3152)
    