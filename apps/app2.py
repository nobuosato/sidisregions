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
        ## app 2: W<sup>2</sup><sub>SIDIS</sub> vs. x<sub>Bj</sub>, z<sub>h</sub>
        '''
    )
),
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        ###### This app plots W<sup>2</sup><sub>SIDIS</sub> for varying x<sub>Bj</sub>, z<sub>h</sub>
        '''
    )
),    
    
    

    html.Br(),
    html.Div('Choose kinematics and non-perturbative params: '),
    html.Div('Q [GeV] = ', style=style1),
    dcc.Input(id='app2-Q',type='number',min=0,step=0.1,value=2,style=dict(width='10%')),
    html.Div(['q',html.Sub('T'),' [GeV] = '], style=style1),
    dcc.Input(id='app2-qT',type='number',min=0,step=0.1,value=0.5,style=dict(width='10%')),


    html.Br(),html.Br(),
    html.Div('Choose camera view: '),
    html.Div('angle= ', style=style1),
    dcc.Input(id='app2-angle',type='number',step=5,value=30,style=dict(width='10%')),
    html.Div('height= ', style=style1),
    dcc.Input(id='app2-height',type='number',step=0.1,value=0.5,style=dict(width='10%')),


    dcc.Graph(id='app2-graph'),
    html.Br(),

    dcc.Markdown(dedent('''
    ----
    **Author**: N. Sato (nsato@jlab.org)
    ''')),

   ]) 

colorscale=[[0.0 , 'rgb(255,255,255)'],
           [0.1, 'rgb(28,76,96)'],
           [0.2, 'rgb(16,125,121)'],
           [0.3, 'rgb(92,166,133)'],
           [0.4, 'rgb(182,202,175)'],
           [0.5, 'rgb(253,245,243)'],
           [0.6, 'rgb(230,183,162)'],
           [0.7, 'rgb(211,118,105)'],
           [0.8, 'rgb(174,63,95)'],
           [0.9, 'rgb(116,25,93)'],
           [1.0, 'rgb(51,13,53)']]

@app.callback(
     Output('app2-graph'   , 'figure'),
    [ Input('app2-Q'       , 'value'),
      Input('app2-qT'      , 'value'),
      Input('app2-angle'   , 'value'),
      Input('app2-height'  , 'value')])
def update(Q,qT,angle,height):

    params=gen_params()
    params['Q']=Q
    params['T_t']=qT
    
    _zh=np.linspace(0.1,1,50)
    _xb=np.linspace(0.1,1,50)

    xb,zh=np.meshgrid(_xb, _zh)
    params['x_bj']=xb
    params['z_h']=zh
    
    W2=evaluate(rat.get_W2,params)

    W2[W2<0]=np.nan

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=2.5*np.cos(angle*np.pi/180), y=2.5*np.sin(angle*np.pi/180), z=height))

    trace= go.Surface(y=tuple(xb),x=tuple(zh),z=tuple(W2))#,colorscale=colorscale, )
    layout = go.Layout(
                title="" ,
                autosize=False,
                width=700,
                height=700,
                scene=dict(
                      aspectmode='cube',
                      camera=camera,
                      yaxis=dict(title='x<sub>Bj</sub>'),
                      xaxis=dict(title='z<sub>h</sub>'),
                      zaxis=dict(title='W<sup>2</sup> [GeV]'  ),))

    data=[trace]
    fig = go.Figure(data=data, layout=layout)
    return fig




