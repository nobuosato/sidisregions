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
        ## app 4: W<sup>2</sup><sub>SIDIS</sub> vs. x<sub>Bj</sub>, Q
        '''
    )
),
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        ##### This app plots W<sup>2</sup><sub>SIDIS</sub> for varying x<sub>Bj</sub>, Q
        '''
    )
),    

    html.Br(),
    html.Div('Choose kinematics: '),
    html.Div(['z',html.Sub('h'),' = '], style=style1),
    dcc.Input(id='app4-zh',type='number',min=0,max=1,step=0.01,value=0.25,style=dict(width='10%')),
    html.Div(['q',html.Sub('T'),' [GeV] = '], style=style1),
    dcc.Input(id='app4-qT',type='number',min=0,step=0.1,value=0,style=dict(width='10%')),
    html.Div(['W',html.Sup('2'),html.Sub('(max)'),' = '], style=style1),
    dcc.Input(id='app4-W2max',type='number',min=1,step=1,value=12,style=dict(width='10%')),

    dcc.Graph(id='app4-graph'),
    html.Br(),

   ]) 



@app.callback(
     Output('app4-graph'   , 'figure'),
    [ Input('app4-zh'      , 'value'),
      Input('app4-qT'      , 'value'),
      Input('app4-W2max'   , 'value')
    ])
def update(zh,qT,W2max):

    params=gen_params()
    params['T_t']=qT
    params['z_h']=zh
    


    _Q =np.linspace(0.5,2.5,100)
    _xb=np.linspace(0.1,0.8,100)
    xb,Q=np.meshgrid(_xb, _Q)

    params['Q']=Q
    params['x_bj']=xb
    
    W2=evaluate(rat.get_W2,params)
    W2[W2<0]=np.nan
    W2[W2>W2max]=np.nan


    data = [go.Heatmap(x=_xb,y=_Q,z=W2,colorscale='Jet'),]

    layout = go.Layout(
          width = 800,
          height = 500,
          xaxis = dict(
                  #nticks = 10,
                  #domain = [0, 0.45],
                  title = "x<sub>Bj"
                  ),
          yaxis = dict(
                  #scaleanchor = "x",
                  #domain = [0, 0.45],
                  title = "Q [GeV]"
                  ),
          showlegend= False
          )

    fig = go.Figure(data=data, layout=layout)
    return fig




