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
        ## app 3: y<sub>h</sub> vs. x<sub>Bj</sub>, z<sub>h</sub>
        '''
    )
),    
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        ##### This app plots y<sub>h</sub> for varying x<sub>Bj</sub> and z<sub>h</sub>
        '''
    )
),

    html.Br(),
    html.Div('Choose kinematics and non-perturbative params: '),
    html.Div('Q [GeV] = ', style=style1),
    dcc.Input(id='app3-Q',type='number',min=0,step=0.1,value=2,style=dict(width='10%')),
    html.Div(['q',html.Sub('T'),' [GeV] = '], style=style1),
    dcc.Input(id='app3-qT',type='number',min=0,step=0.1,value=0.5,style=dict(width='10%')),


    html.Br(),html.Br(),
    html.Div('Choose camera view: '),
    html.Div('angle= ', style=style1),
    dcc.Input(id='app3-angle',type='number',step=5,value=30,style=dict(width='10%')),
    html.Div('height= ', style=style1),
    dcc.Input(id='app3-height',type='number',step=0.1,value=0.5,style=dict(width='10%')),


    dcc.Graph(id='app3-graph'),
    html.Br(),

    dcc.Markdown(dedent('''
    ----
    **Author**: N. Sato (nsato@jlab.org)
    ''')),

   ]) 


@app.callback(
     Output('app3-graph'   , 'figure'),
    [ Input('app3-Q'       , 'value'),
      Input('app3-qT'      , 'value'),
      Input('app3-angle'   , 'value'),
      Input('app3-height'  , 'value')])
def update(Q,qT,angle,height):

    params=gen_params()
    params['T_t']=qT
    params['Q']=Q
    
    _zh=np.linspace(0.1,1,50)
    _xb=np.linspace(0.1,1,50)

    xb,zh=np.meshgrid(_xb, _zh)
    params['x_bj']=xb
    params['z_h']=zh
    
    yh=evaluate(rat.get_yh,params)

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=2.5*np.cos(angle*np.pi/180), y=2.5*np.sin(angle*np.pi/180), z=height))

    trace= go.Surface(y=tuple(xb),x=tuple(zh),z=tuple(yh),)
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
                      zaxis=dict(title='y<sub>h</sub>'  ),))
    data=[trace]
    fig = go.Figure(data=data, layout=layout)
    return fig


