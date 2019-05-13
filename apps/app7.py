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


style1={'color': 'black', 'fontSize': 14, 'display': 'inline-block','padding': 10 }

    

layout = html.Div([
    dcc.Link('Go back to menu', href='/'),

    
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        '''
        ## app 7:  R<sub>i</sub> vs. x<sub>Bj</sub>, Q 
        '''
    )
),    
        
    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        '''
        ###### This app plots R<sub>i</sub> for varying x<sub>Bj</sub>, Q 
        '''
    )
),
    
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        ###### To discriminate non physical data set x<sub>Bj (max)</sub> = \u03BE
        '''
    )
),       



    html.Div('Select quantity to study: '),
    dcc.Dropdown(
        id='app7-quantity',
        options=[{'label': i, 'value': i} for i in ['R1','R2','R3','R1prime']],
        value='R1',
        style=dict(width='38%'),
        ),

   
    html.Br(),
    html.Div('Choose kinematics and np params: '),

    html.Div(['q',html.Sub('T'),' [GeV] = '], style=style1),
    dcc.Input(id='app7-qT',type='number',min=1e-3,step=0.1,value=0.5,style=dict(width='10%')),

    html.Div(['x',html.Sub('Bj (min)'),' = '], style=style1),
    dcc.Input(id='app7-xbjmin',type='number',min=1e-3,max=1,step=0.01,value=0.1,style=dict(width='10%')),

    html.Div(['x',html.Sub('Bj (max)'),' = '], style=style1),
    dcc.Input(id='app7-xbjmax',type='number',min=1e-3,max=1,step=0.01,value=0.3,style=dict(width='10%')),

    html.Br(),
    html.Div(['z',html.Sub('h'),' = '],style=style1),
    dcc.Input(id='app7-zh',type='number',min=1e-3,max=1,step=0.01,value=0.3,style=dict(width='10%')),

    html.Div([u"\u03BE",' = '], style=style1),
    dcc.Input(id='app7-xi',type='number',min=1e-3,max=1,step=0.01,value=0.3,style=dict(width='10%')),

    html.Div([u"\u03B6",' = '], style=style1),
    dcc.Input(id='app7-zeta',type='number',min=1e-3,max=1,step=0.01,value=0.3,style=dict(width='10%')),

    html.Div('M [GeV] = ', style=style1),
    dcc.Input(id='app7-M',type='number',min=1e-3,step=0.01,value=0.938,style=dict(width='10%')),

    html.Br(),html.Br(),
    html.Div(['M',html.Sub('ki'),' [GeV] = '], style=style1),
    dcc.Input(id='app7-Mki',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div(['M',html.Sub('kf'),' [GeV] = '], style=style1),
    dcc.Input(id='app7-Mkf',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div([u"\u03B4",html.Sub('kT'),' [GeV] = '], style=style1),
    dcc.Input(id='app7-dkT',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div(['k',html.Sub('iT'),' [GeV] = '], style=style1),
    dcc.Input(id='app7-kiT',type='number',step=0.1,value=0.1,style=dict(width='10%')),


    dcc.Graph(id='app7-graph'),
    html.Br(),

   ]) 



@app.callback(
    Output('app7-graph'   , 'figure'),
   [ Input('app7-quantity','value'),
     Input('app7-qT'      , 'value'),
     Input('app7-xbjmin'  , 'value'),
     Input('app7-xbjmax'  , 'value'),
     Input('app7-zh'      , 'value'),
     Input('app7-xi'      , 'value'),
     Input('app7-zeta'    , 'value'),
     Input('app7-M'       , 'value'),
     Input('app7-Mki'     , 'value'),
     Input('app7-Mkf'     , 'value'),
     Input('app7-dkT'     , 'value'),
     Input('app7-kiT'     , 'value')
    ])
def update(Ri,qT,xbjmin,xbjmax,zh,xi,zeta,M,Mki,Mkf,dkT,kiT):

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

    _xb=np.linspace(xbjmin,xbjmax,100)
    _Q =np.linspace(0.8,2.0,100)
    xb,Q=np.meshgrid(_xb,_Q)

    params['Q']=Q
    params['x_bj']=xb

    if Ri=='R1': R=evaluate(rat.get_R1,params)
    if Ri=='R2': R=evaluate(rat.get_R2,params)
    if Ri=='R3': R=evaluate(rat.get_R3,params)
    if Ri=='R1prime': R=evaluate(rat.get_R4,params)
    R=np.abs(R)

    R[R>1]=1


    data = [go.Heatmap(x=_xb,y=_Q,z=R,colorscale='Jet'),]

    layout = go.Layout(
          width = 800,
          height = 500,
          xaxis = dict(
                  #nticks = 10,
                  #domain = [0, 0.45],
                  title = 'x<sub>Bj'
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

 


