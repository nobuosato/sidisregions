import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent
import matplotlib
#matplotlib.use('Agg')
import pylab as py
from plotly.tools import mpl_to_plotly
import numpy as np
import ratlib as rat
from plotly import tools
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from plotly import tools
from app import app
from aux import gen_params, evaluate

style1={'color': 'black', 'fontSize': 14, 'display': 'inline-block','padding': 10}

layout = html.Div([
    dcc.Link('Go back to menu', href='/'),

    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        '''
        ## app 5:  x<sub>N</sub>/x<sub>Bj</sub> vs. x<sub>Bj</sub> 
        '''
    )
),   
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        '''
        ###### This app plots the ratio x<sub>N</sub>/x<sub>Bj</sub> vs. x<sub>Bj</sub> 
        '''
    )
),      

    html.Div('Choose experiment: '),
    dcc.Dropdown(
        id='app5-exp',
        options=[
            {'label': 'JLab'   , 'value': 'JLab'},
            {'label': 'HERMES' , 'value': 'HERMES'},
            {'label': 'COMPASS', 'value': 'COMPASS'}
        ],
        value='JLab',style=dict(width='40%')
    ),

    html.Br(),
    html.Div('Additional parameters: '),
    html.Div('M [GeV] = ', style=style1),
    dcc.Input(id='app5-M',type='number',min=0.1,
              step=0.01,value=0.938,style=dict(width='10%')),

    html.Div(['W',html.Sup('2'),html.Sub('cut'), ' [Gev]',html.Sup('2'), ' = '], style=style1),
    dcc.Input(id='app5-W2_cut',type='number',min=4,
              step=0.01,value=4,style=dict(width='10%')),

    html.Div(['x',html.Sub('Bj (max)'),' = '], style=style1),
    dcc.Input(id='app5-x_bjmax',type='number',min=1e-5,max=1,
              step=0.01,value=0.8,style=dict(width='10%')),

    html.Div('Q [GeV] = ', style=style1),
    dcc.Input(id='app5-Q',type='number',min=1,
              step=0.05,value=2.0,style=dict(width='10%')),

    dcc.Graph(id='app5-graph'),

   ]) 



@app.callback(
     Output('app5-graph'   , 'figure'),
    [ Input('app5-exp'     , 'value'),
      Input('app5-M'       , 'value'),
      Input('app5-W2_cut'  , 'value'),
      Input('app5-x_bjmax' , 'value'),
      Input('app5-Q'       , 'value')
    ])
def update(exp,M,W2cut,xmax,Q):

    params=gen_params()
    params['M']=M

    if   exp=='JLab':    s = M**2 + 2*11*M
    elif exp=='HERMES':  s = M**2 + 2*27.6*M
    elif exp=='COMPASS': s = M**2 + 2*160*M

    Q2min=1.
    xmin=Q2min/(s-M)
    xb=np.linspace(xmin,xmax,50)
    Q2_low  = xb/(1-xb)*(W2cut-M**2)
    Q2_high = xb*(s-M**2)
    params['x_bj']=xb

    params['Q']=Q2_low**0.5
    xN_low=evaluate(rat.get_xN,params)
    params['Q']=Q2_high**0.5
    xN_high=evaluate(rat.get_xN,params)


    line1 = go.Scatter(
      x = xb,
      y = xN_low/xb,
      name = 'Low Q',
      line = dict(
          color = ('rgb(22, 96, 167)'),
          width = 4,
          dash = 'solid'))

    line2 = go.Scatter(
      x = xb,
      y = xN_high/xb,
      name = 'High Q',
      line = dict(
          color = ('rgb(22, 96, 167)'),
          width = 4,
          dash = 'dot'),
          fill='tonexty')

    xmin=Q**2/(s-M)
    _xmax=Q**2/(W2cut-M**2+Q**2)

    xb=np.linspace(xmin,min(_xmax,xmax),50)
    params['x_bj']=xb
    params['Q']=Q
    xN=evaluate(rat.get_xN,params)


    line3 = go.Scatter(
      x = xb,
      y = xN/xb,
      name = 'Q',
      line = dict(
          color = ('rgb(205, 12, 24)'),
          width = 4,))

    data = [line1,line2,line3]

    layout = go.Layout(
          width = 800,
          height = 500,
          xaxis = dict(title = "x<sub>Bj"),
          yaxis = dict(title = "x<sub>N</sub>/x<sub>Bj</sub>",range=(0.9,1)),
          showlegend= True
          )

    fig = go.Figure(data=data, layout=layout)
    return fig




