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
        u'''
        ## app 6: z<sub>N</sub>/z<sub>h</sub> vs. z<sub>h</sub>
        '''
    )
),     

    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        ###### This is a plot of z<sub>N</sub>/z<sub>h</sub> vs. z<sub>h</sub> for JLab, HERMES, and COMPASS
        '''
    )
),       

    html.Div('Choose experiment: '),
    dcc.Dropdown(
        id='app6-exp',
        options=[
            {'label': 'JLab'   , 'value': 'JLab'},
            {'label': 'HERMES' , 'value': 'HERMES'},
            {'label': 'COMPASS', 'value': 'COMPASS'}
        ],
        value='JLab',style=dict(width='40%')
    ),
    dcc.Dropdown(
        id='app6-had',
        options=[
            {'label': 'pion' , 'value': 'pion'},
            {'label': 'kaon' , 'value': 'kaon'}
        ],
        value='pion',style=dict(width='40%')
    ),

    html.Br(),
    html.Div('Additional parameters: '),
    html.Div(['q',html.Sub('T'),' [GeV] = '], style=style1),
    dcc.Input(id='app6-q_T',type='number',min=1e-10,
              step=0.01,value=0.5,style=dict(width='10%')),

    html.Div(['W',html.Sup('2'),html.Sub('cut'), ' [Gev]',html.Sup('2'), ' = '], style=style1),
    dcc.Input(id='app6-W2_cut',type='number',min=4,
              step=0.01,value=4,style=dict(width='10%')),

    html.Div('x_bj(max)=', style=style1),
    dcc.Input(id='app6-x_bjmax',type='number',min=1e-5,max=1,
              step=0.01,value=0.8,style=dict(width='10%')),

    html.Div('x_bj=', style=style1),
    dcc.Input(id='app6-x_bj',type='number',min=1e-5,max=1,
              step=0.01,value=0.1,style=dict(width='10%')),

    html.Div('Q [GeV] = ', style=style1),
    dcc.Input(id='app6-Q',type='number',min=1,
              step=0.05,value=2.0,style=dict(width='10%')),

    dcc.Graph(id='app6-graph'),

   ]) 



@app.callback(
     Output('app6-graph'   , 'figure'),
    [ Input('app6-exp'     , 'value'),
      Input('app6-had'     , 'value'),
      Input('app6-q_T'      , 'value'),
      Input('app6-W2_cut'  , 'value'),
      Input('app6-x_bjmax' , 'value'),
      Input('app6-x_bj'    , 'value'),
      Input('app6-Q'       , 'value')
    ])
def update(exp,had,qT,W2cut,xmax,x,Q):

    params=gen_params()
    M=0.938

    if   exp=='JLab':    s = M**2 + 2*11*M
    elif exp=='HERMES':  s = M**2 + 2*27.6*M
    elif exp=='COMPASS': s = M**2 + 2*160*M

    if    had=='pion': params['M_h']=0.139
    elif  had=='kaon': params['M_h']=0.497

    params['T_t']=qT
    zh=np.linspace(0.1,0.8,50)
    

    Q2min=1.
    xmin=Q2min/(s-M)
    xb=np.linspace(xmin,xmax,50)
    Q2_low  = xb/(1-xb)*(W2cut-M**2)
    Q2_high = xb*(s-M**2)
    params['x_bj']=xb

    zN_up=[]
    zN_do=[]
    for _zh in zh:
        params['z_h']=_zh
        params['Q']=Q2_low**0.5
        zN_vals=evaluate(rat.get_zN,params)
        params['Q']=Q2_high**0.5
        zN_vals=np.append(zN_vals,evaluate(rat.get_zN,params))
        zN_do.append(np.amin(zN_vals))
        zN_up.append(np.amax(zN_vals))
    zN_up=np.array(zN_up)
    zN_do=np.array(zN_do)

    line1 = go.Scatter(
      x = zh,
      y = zN_do/zh,
      name = 'Low Q',
      line = dict(
          color = ('rgb(22, 96, 167)'),
          width = 4,
          dash = 'solid'))

    line2 = go.Scatter(
      x = zh,
      y = zN_up/zh,
      name = 'High Q',
      line = dict(
          color = ('rgb(22, 96, 167)'),
          width = 4,
          dash = 'dot'),
          fill='tonexty')

    params['z_h']=zh
    params['Q']=Q
    zN=evaluate(rat.get_zN,params)

    line3 = go.Scatter(
      x = zh,
      y = zN/zh,
      name = 'Q',
      line = dict(
          color = ('rgb(205, 12, 24)'),
          width = 4,))

    data = [line1,line2,line3]

    layout = go.Layout(
          width = 800,
          height = 500,
          xaxis = dict(title = "z<sub>h"),
          yaxis = dict(title = "z<sub>N</sub>/z<sub>h</sub>",range=(0.8,1)),
          showlegend= True
          )

    fig = go.Figure(data=data, layout=layout)
    return fig




