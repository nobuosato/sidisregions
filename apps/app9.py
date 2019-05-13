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
        ## app 9: R<sub>i</sub> vs. q<sub>T</sub>/Q, y<sub>h</sub> 
        '''
    )
),   

    dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        ''' 
        ###### This app plots the R<sub>i</sub> for varying q<sub>T</sub>/Q, y<sub>h</sub> 
        '''
    )
),       
    
    html.Div('Select outgoing hadron: '),
    dcc.Dropdown(
        id='app9-had',
        options=[
            {'label': 'pion' , 'value': 'pion'},
            {'label': 'kaon' , 'value': 'kaon'}
        ],
        value='pion',style=dict(width='40%')
    ),

    html.Div('Select quantity to study: '),
    dcc.Dropdown(
        id='app9-quantity',
        options=[{'label': i, 'value': i} for i in ['R1','R2','R3','R1prime']],
        value='R1',
        style=dict(width='38%'),
        ),


    html.Div('Choose external kinematics: '),

    html.Div('M [GeV]=', style=style1),
    dcc.Input(id='app9-M',type='number',min=0.1,step=0.01,value=0.938,style=dict(width='10%')),

    html.Div(['x',html.Sub('Bj'),' = '], style=style1),
    dcc.Input(id='app9-x_bj',type='number',min=1e-5,max=1,step=0.001,value=0.1,style=dict(width='10%')),

    html.Div('Q [GeV] = ', style=style1),
    dcc.Input(id='app9-Q',type='number',min=1e-5,step=0.1,value=2.0,style=dict(width='10%')),

    html.Div(['y',html.Sub('h (min)'),' = '], style=style1),
    dcc.Input(id='app9-yHmin',type='number',min=-5,step=0.1,value=-4,style=dict(width='10%')),

    html.Div(['y',html.Sub('h (max)'),' = '], style=style1),
    dcc.Input(id='app9-yHmax',type='number',min= 5,step=0.1,value= 0,style=dict(width='10%')),

    html.Br(),
    html.Div('Choose nonperturbative parameters (only relevant for R_123): '),

    html.Div([u"\u03BE",' = '], style=style1),
    dcc.Input(id='app9-xi',type='number',min=1e-3,max=1,step=0.01,value=0.1,style=dict(width='10%')),

    html.Div([u"\u03B6",' = '], style=style1),
    dcc.Input(id='app9-zeta',type='number',min=1e-3,max=1,step=0.01,value=0.4,style=dict(width='10%')),

    html.Br(),#,html.Br(),
    html.Div('Mki[GeV]= ', style=style1),
    dcc.Input(id='app9-Mki',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div('Mkf[GeV]= ', style=style1),
    dcc.Input(id='app9-Mkf',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div('dkT[GeV]= ', style=style1),
    dcc.Input(id='app9-dkT',type='number',step=0.1,value=0.1,style=dict(width='10%')),
    html.Div('kiT[GeV]= ', style=style1),
    dcc.Input(id='app9-kiT',type='number',step=0.1,value=0.1,style=dict(width='10%')),


    dcc.Graph(id='app9-graph'),
    #html.Div(id='app9-log'),

    html.Br(),

   ]) 


@app.callback(
     Output('app9-graph'   , 'figure'),
     #Output('app9-log'   , 'children'),
    [ Input('app9-had'     , 'value'),
      Input('app9-quantity', 'value'),
      Input('app9-M'       , 'value'),
      Input('app9-x_bj'    , 'value'),
      Input('app9-Q'       , 'value'),
      Input('app9-yHmin'   , 'value'),
      Input('app9-yHmax'   , 'value'),
      Input('app9-xi'      , 'value'),
      Input('app9-zeta'    , 'value'),
      Input('app9-Mki'     , 'value'),
      Input('app9-Mkf'     , 'value'),
      Input('app9-dkT'     , 'value'),
      Input('app9-kiT'     , 'value')
    ])
def update(had,qua,M,x,Q,yHmin,yHmax,xi,zeta,Mki,Mkf,dkT,kiT):
    params=gen_params()
    params['M']=M
    params['xi']=xi
    params['zeta']=zeta
    #params['T_t']=qT
    params['delta_k_t']=dkT
    params['M_ki']=Mki
    params['M_kf']=Mkf
    params['k_i_t']=kiT
    params['Q']=Q
    params['x_bj']=x

    if    had=='pion': params['M_h']=0.139
    elif  had=='kaon': params['M_h']=0.497

    Mh=params['M_h']
    xN=evaluate(rat.get_xN,params)

    #etamin=evaluate(rat.get_etamin,params)
    #etamax=evaluate(rat.get_etamax,params)
    #yP=np.log(Q/xN/M)
    #yH=np.linspace(etamin,etamax,100)
    #dy=yP-yH
    #Htmax=[]
    #for eta in yH:
    #    params['eta']=eta
    #    Htmax.append(evaluate(rat.get_Htmax,params))
    #Htmax=np.array(Htmax)
    #zh=(xN*np.sqrt(Mh**2+Htmax**2)*M/(Q**2-xN**2*M**2))*2*np.cosh(dy)
    #qtmax=Htmax/zh

    #line1 = go.Scatter(
    #  x = yH,
    #  y = np.zeros(yH.size),
    #  name = '',
    #  line = dict(
    #      color = ('rgb(22, 96, 167)'),
    #      width = 4,
    #      dash = 'solid'))
    #line2 = go.Scatter(
    #  x = yH,
    #  y = qtmax/Q,
    #  name = 'High Q',
    #  line = dict(
    #      color = ('rgb(22, 96, 167)'),
    #      width = 4,
    #      dash = 'dot'),
    #      fill='tonexty')

    _yH=np.linspace(yHmin,yHmax,50)
    _qT=np.linspace(0,2,50)    
    yH,qT=np.meshgrid(_yH,_qT)
    yP=np.log(Q/xN/M)
    
    pf=xN*M/(Q**2-xN**2*M**2)*2*np.cosh(yP-yH)
    zh=np.sqrt(pf**2*Mh**2/(1-pf**2*qT**2))
    params['z_h']=zh


    if   qua=='R1':    R=np.abs(evaluate(rat.get_R1,params))
    elif qua=='R2':    R=np.abs(evaluate(rat.get_R2,params))
    elif qua=='R3':    R=np.abs(evaluate(rat.get_R3,params))
    elif qua=='R1prime':    R=np.abs(evaluate(rat.get_R4,params))    

    R[R>1]=np.nan

    data = [go.Heatmap(x=_yH,y=_qT,z=R,colorscale='Jet')]#[line1,line2,R1]

    layout = go.Layout(
          width = 800,
          height = 500,
          xaxis = dict(title = "y<sub>h</sub>",range=(None,yP)),
          yaxis = dict(title = "q<sub>T</sub>/Q",range=(0,2)),
          showlegend= True
          )

    fig = go.Figure(data=data, layout=layout)
    return fig











#    params['Q']=Q
#    params['x_bj']=xb
#
#    if   qua=='R1':    R=np.abs(evaluate(rat.get_R1,params))
#    elif qua=='R2':    R=np.abs(evaluate(rat.get_R2,params))
#    elif qua=='R3':    R=np.abs(evaluate(rat.get_R3,params))
#    elif qua=='xN/xb': R=evaluate(rat.get_xN,params)/xb
#    elif qua=='zN/zh': R=evaluate(rat.get_zN,params)/zh
#
#    R[R>1]=np.nan
#    R[Q**2>xb*(s-M)]=np.nan
#    R[W2cut>(M**2+Q**2/xb-Q**2)]=np.nan
#
#    #print(R)
#    data = [go.Heatmap(x=_xb,y=_Q,z=R,colorscale='Jet'),]
#
#    layout = go.Layout(
#          width = 800,
#          height = 500,
#          xaxis = dict(
#                  #nticks = 10,
#                  #domain = [0, 0.45],
#                  title = "x_bj"
#                  ),
#          yaxis = dict(
#                  #scaleanchor = "x",
#                  #domain = [0, 0.45],
#                  title = "Q[GeV]"
#                  ),
#          showlegend= False
#          )
#
#    fig = go.Figure(data=data, layout=layout)
#    return fig
#
#
#
#
#
#
#
#
#
#
#
#    return None
#    #return exp#'%f'%M
#
#
#    Q2min=1.
#    xmin=Q2min/(s-M)
#    _xb=np.linspace(xmin,xmax,50)
#
#    Q2max = xmax*(s-M**2)
#    _Q=np.linspace(Q2min,Q2max,100)**0.5
#    #print(Q2min,Q2max)
#
#    xb,Q=np.meshgrid(_xb,_Q)
#
#    params['Q']=Q
#    params['x_bj']=xb
#
#    if   qua=='R1':    R=np.abs(evaluate(rat.get_R1,params))
#    elif qua=='R2':    R=np.abs(evaluate(rat.get_R2,params))
#    elif qua=='R3':    R=np.abs(evaluate(rat.get_R3,params))
#    elif qua=='xN/xb': R=evaluate(rat.get_xN,params)/xb
#    elif qua=='zN/zh': R=evaluate(rat.get_zN,params)/zh
#
#    R[R>1]=np.nan
#    R[Q**2>xb*(s-M)]=np.nan
#    R[W2cut>(M**2+Q**2/xb-Q**2)]=np.nan
#
#    #print(R)
#    data = [go.Heatmap(x=_xb,y=_Q,z=R,colorscale='Jet'),]
#
#    layout = go.Layout(
#          width = 800,
#          height = 500,
#          xaxis = dict(
#                  #nticks = 10,
#                  #domain = [0, 0.45],
#                  title = "x_bj"
#                  ),
#          yaxis = dict(
#                  #scaleanchor = "x",
#                  #domain = [0, 0.45],
#                  title = "Q[GeV]"
#                  ),
#          showlegend= False
#          )
#
#    fig = go.Figure(data=data, layout=layout)
#    return fig




