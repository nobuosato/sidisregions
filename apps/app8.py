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
        ## app 8:  Ratios vs. x<sub>Bj</sub>, Q 
        '''
    )
),   
    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        '''
        ###### This app plots Ratios vs. x<sub>Bj</sub>, Q For JLab, HERMES and COMPASS
        '''
    )
),       
    

    html.Div('Choose experiment: '),
    dcc.Dropdown(
        id='app8-exp',
        options=[
            {'label': 'JLab'   , 'value': 'JLab'},
            {'label': 'HERMES' , 'value': 'HERMES'},
            {'label': 'COMPASS', 'value': 'COMPASS'}
        ],
        value='JLab',style=dict(width='40%')
    ),

    html.Div('Select outgoing hadron: '),
    dcc.Dropdown(
        id='app8-had',
        options=[
            {'label': 'pion' , 'value': 'pion'},
            {'label': 'kaon' , 'value': 'kaon'}
        ],
        value='pion',style=dict(width='40%')
    ),

    html.Div('Select quantity to study: '),
    dcc.Dropdown(
        id='app8-quantity',
        options=[{'label': i, 'value': i} for i in ['R1','R2','R3','R1prime','xN/xb','zN/zh']],
        value='R1',
        style=dict(width='38%'),
        ),


    html.Div('Choose external kinematics: '),

    html.Div('M [GeV] = ', style=style1),
    dcc.Input(id='app8-M',type='number',min=0.1,step=0.01,value=0.938,style=dict(width='10%')),

    html.Div(['W',html.Sup('2'),html.Sub('cut'), ' [Gev]',html.Sup('2'), ' = '], style=style1),
    dcc.Input(id='app8-W2_cut',type='number',min=4,step=0.1,value=4,style=dict(width='10%')),

    html.Div(['x',html.Sub('Bj (max)'),' = '], style=style1),
    dcc.Input(id='app8-x_bjmax',type='number',min=1e-5,max=1,step=0.01,value=0.8,style=dict(width='10%')),

    html.Br(),
    html.Div(['q',html.Sub('T'),' [GeV] = '], style=style1),
    dcc.Input(id='app8-qT',type='number',min=1e-3,step=0.1,value=0.5,style=dict(width='10%')),

    html.Div(['z',html.Sub('h'),' = '], style=style1),
    dcc.Input(id='app8-zh',type='number',min=1e-3,max=1,step=0.01,value=0.4,style=dict(width='10%')),

    html.Br(),
    html.Div('Choose nonperturbative parameters (only relevant for R_123): '),

    html.Div([u"\u03BE",' = '], style=style1),
    dcc.Input(id='app8-xi',type='number',min=1e-3,max=1,step=0.01,value=0.1,style=dict(width='10%')),

    html.Div([u"\u03B6",' = '], style=style1),
    dcc.Input(id='app8-zeta',type='number',min=1e-3,max=1,step=0.01,value=0.4,style=dict(width='10%')),

    html.Br(),#,html.Br(),
    html.Div(['M',html.Sub('ki'),' [GeV] = '], style=style1),
    dcc.Input(id='app8-Mki',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div(['M',html.Sub('kf'),' [GeV] = '], style=style1),
    dcc.Input(id='app8-Mkf',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div([u"\u03B4",html.Sub('kT'),' [GeV] = '], style=style1),
    dcc.Input(id='app8-dkT',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div(['k',html.Sub('iT'),' [GeV] = '], style=style1),
    dcc.Input(id='app8-kiT',type='number',step=0.1,value=0.1,style=dict(width='10%')),


    dcc.Graph(id='app8-graph'),
    #html.Div(id='app8-log'),

    html.Br(),

   ]) 


@app.callback(
     Output('app8-graph'   , 'figure'),
     #Output('app8-log'   , 'children'),
    [ Input('app8-exp'     , 'value'),
      Input('app8-had'     , 'value'),
      Input('app8-quantity', 'value'),
      Input('app8-M'       , 'value'),
      Input('app8-W2_cut'  , 'value'),
      Input('app8-x_bjmax' , 'value'),
      Input('app8-qT'      , 'value'),
      Input('app8-zh'      , 'value'),
      Input('app8-xi'      , 'value'),
      Input('app8-zeta'    , 'value'),
      Input('app8-Mki'     , 'value'),
      Input('app8-Mkf'     , 'value'),
      Input('app8-dkT'     , 'value'),
      Input('app8-kiT'     , 'value')
    ])
def update(exp,had,qua,M,W2cut,xmax,qT,zh,xi,zeta,Mki,Mkf,dkT,kiT):
    #return exp#'%f'%M

    params=gen_params()
    params['M']=M
    params['z_h']=zh
    params['xi']=xi
    params['zeta']=zeta
    params['T_t']=qT
    params['delta_k_t']=dkT
    params['M_ki']=Mki
    params['M_kf']=Mkf
    params['k_i_t']=kiT

    if   exp=='JLab':    s = M**2 + 2*11*M
    elif exp=='HERMES':  s = M**2 + 2*27.6*M
    elif exp=='COMPASS': s = M**2 + 2*160*M

    if    had=='pion': params['M_h']=0.139
    elif  had=='kaon': params['M_h']=0.497

    Q2min=1.
    xmin=Q2min/(s-M)
    _xb=np.linspace(xmin,xmax,50)

    Q2max = xmax*(s-M**2)
    _Q=np.linspace(Q2min,Q2max,100)**0.5
    #print(Q2min,Q2max)

    xb,Q=np.meshgrid(_xb,_Q)

    params['Q']=Q
    params['x_bj']=xb

    if   qua=='R1':    R=np.abs(evaluate(rat.get_R1,params))
    elif qua=='R2':    R=np.abs(evaluate(rat.get_R2,params))
    elif qua=='R3':    R=np.abs(evaluate(rat.get_R3,params))
    elif qua=='R1prime':    R=np.abs(evaluate(rat.get_R4,params))    
    elif qua=='xN/xb': R=evaluate(rat.get_xN,params)/xb
    elif qua=='zN/zh': R=evaluate(rat.get_zN,params)/zh

    R[R>1]=np.nan
    R[Q**2>xb*(s-M)]=np.nan
    R[W2cut>(M**2+Q**2/xb-Q**2)]=np.nan

    #print(R)
    data = [go.Heatmap(x=_xb,y=_Q,z=R,colorscale='Jet'),]

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




