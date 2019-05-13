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

#    dcc.Markdown(dedent('''
#    ## app1: R_i vs. xb, zh
#    ''')),
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        '''
        ## app 1:  R<sub>i</sub> vs. x<sub>Bj</sub>, z<sub>h</sub> 
        '''
    )
),    
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        ##### This app plots R<sub>i</sub> for varying x<sub>Bj</sub> and z<sub>h</sub>
        '''
    )
),
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        ###### To discriminate non physical data do not consider data corresponding to x<sub>Bj</sub> > \u03BE
        '''
    )
),


    html.Div('Select quantity to study: '),
    dcc.Dropdown(
        id='app1-quantity',
        options=[{'label': i, 'value': i} for i in ['R1','R2','R3','R1prime']],
        value='R1',
        style=dict(width='38%'),
        ),

    html.Br(),
    html.Div('Choose kinematics and non-perturbative params: '),
    html.Div('Q [GeV] = ', style=style1),

    dcc.Input(  id='app1-Q',type='number'
              ,min=0.5,step=0.1,value=2,style=dict(width='10%')),
    html.Div(['q',html.Sub('T'),' [GeV] = '], style=style1),

    dcc.Input(id='app1-qT',type='number'
      ,min=1e-3,step=0.1,value=0.5,style=dict(width='10%')),
    html.Div([u"\u03BE",' = '], style=style1),

    dcc.Input(id='app1-xi',type='number'
      ,min=1e-3,max=1,step=0.01,value=0.1,style=dict(width='10%')),
    html.Div([u"\u03B6",' = '], style=style1),

    dcc.Input(id='app1-zeta',type='number'
      ,min=1e-3,max=1,step=0.01,value=0.3,style=dict(width='10%')),

    html.Br(),html.Br(),
    html.Div(['M',html.Sub('ki'),' [GeV] = '], style=style1),
    dcc.Input(id='app1-Mki',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div(['M',html.Sub('kf'),' [GeV] = '], style=style1),
    dcc.Input(id='app1-Mkf',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div([u"\u03B4",html.Sub('kT'),' [GeV] = '], style=style1),
    dcc.Input(id='app1-dkT',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div(['k',html.Sub('iT'),' [GeV] = '], style=style1),
    dcc.Input(id='app1-kiT',type='number',step=0.1,value=0.1,style=dict(width='10%')),


    html.Br(),html.Br(),
    html.Div('Choose camera view: '),
    html.Div('angle= ', style=style1),
    dcc.Input(id='app1-angle',type='number',step=5,value=30,style=dict(width='10%')),
    html.Div('height= ', style=style1),
    dcc.Input(id='app1-height',type='number',step=0.1,value=0.5,style=dict(width='10%')),


    dcc.Graph(id='app1-graph'),
    html.Br(),

    dcc.Markdown(dedent('''
    ----
    **Author**: N. Sato (nsato@jlab.org)
    ''')),


   ]) 

@app.callback(
     Output('app1-graph'   , 'figure'),
    [ Input('app1-quantity','value'),
      Input('app1-Q'       , 'value'),
      Input('app1-qT'      , 'value'),
      Input('app1-xi'      , 'value'),
      Input('app1-zeta'    , 'value'),
      Input('app1-Mki'     , 'value'),
      Input('app1-Mkf'     , 'value'),
      Input('app1-dkT'     , 'value'),
      Input('app1-kiT'     , 'value'),
      Input('app1-angle'   , 'value'),
      Input('app1-height'  , 'value')])
def update(Ri,Q,qT,xi,zeta,Mki,Mkf,dkT,kiT,angle,height):

    params=gen_params()
    params['xi']=xi
    params['zeta']=zeta
    params['M_ki']=Mki
    params['M_kf']=Mkf
    params['T_t']=qT
    params['delta_k_t']=dkT
    params['k_i_t']=kiT
    params['Q']=Q
    
    _xb=np.linspace(xi,1,50)
    _zh=np.linspace(zeta,1,50)

    xb,zh=np.meshgrid(_xb, _zh)
    params['x_bj']=xb
    params['z_h']=zh
    
    if Ri=='R1': R=evaluate(rat.get_R1,params)
    if Ri=='R2': R=evaluate(rat.get_R2,params)
    if Ri=='R3': R=evaluate(rat.get_R3,params)
    if Ri=='R1prime': R=evaluate(rat.get_R4,params)    

    R=np.abs(R)

    R[R>1]=1

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=2.5*np.cos(angle*np.pi/180), y=2.5*np.sin(angle*np.pi/180), z=height))

    trace= go.Surface(y=tuple(xb),x=tuple(zh),z=tuple(R),)
    layout = go.Layout(
                title="" ,
                autosize=False,
                width=700,
                height=700,
                scene=dict(
                      aspectmode='cube',
                      camera=camera,
                      yaxis=dict(title='x<sub>Bj</sub>',range=(0,1)),
                      xaxis=dict(title='z<sub>h</sub>',range=(0,1)),
                      zaxis=dict(title=Ri  ,range=(0,1)),))
    data=[trace]
    fig = go.Figure(data=data, layout=layout)
    return fig








