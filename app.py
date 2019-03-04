#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as py


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
from plotly.tools import mpl_to_plotly
import dash
#from apps import ri_zn
#from apps import example1 
from textwrap import dedent

import ratlib as rat

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.config.requests_pathname_prefix = ""

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

######################################################
index_page = html.Div([
    dcc.Markdown(dedent('''

    # SIDIS regions analysis tools
    
    This site is currently under development. 
    
    ''')),

    html.Br(),
    html.Br(),
    dcc.Link('example 1', href='/ri-vs-zh'),
    html.Br(),
    dcc.Link('example 2', href='/example1'),
    html.Br(),
    html.Br(),
    dcc.Markdown(dedent('''
    ## Authors:
    
       - N. Sato
    
    ''')),
])



######################################################
def gen_slider(label,min,max,step,value):
    #return daq.Slider(
    #  id=label,
    #  min=min,
    #  max=max,
    #  step=step,
    #  value=value,
    #  marks={_ : '%0.1f'%_ for _ in np.linspace(min, max, 10)},
    #  #updatemode='drag',
    #  handleLabel={"showCurrentValue": True,"label": "VALUE"},
    #  size=400)

    return dcc.Slider(
      id=label,
      min=min,
      max=max,
      step=step,
      value=value)


style={'height': '50px', 'width': '40%','display': 'inline-block','position':'relative'}
######################################################

p1layout = html.Div([

    dcc.Link('Go back to home', href='/'),
    html.Br(),

    html.H1('R_i vs z_h'),

    dcc.Graph(id='ri_zh'),
    html.Br(),

    html.Div(children='xb' ) , html.Div(gen_slider('xb' , 0.0,  1.0,  0.1, 0.5),style=style),
    html.Div(children='Q'  ) , html.Div(gen_slider('Q'  , 0.5, 10.0,  0.1, 2.0),style=style),
    html.Div(children='qT' ) , html.Div(gen_slider('qT' , 0.0, 10.0,  0.1, 2.0),style=style),
    html.Div(children='Mki' ), html.Div(gen_slider('Mki', 0.0,  1.0,  0.1, 0.1),style=style),
    html.Div(children='Mkf' ), html.Div(gen_slider('Mkf', 0.0,  1.0,  0.1, 0.1),style=style),
    html.Div(children='dkT' ), html.Div(gen_slider('dkT', 0.0,  1.0,  0.1, 0.1),style=style),
    html.Div(children='kiT' ), html.Div(gen_slider('kiT', 0.0,  1.0,  0.1, 0.1),style=style),


])

def gen_params():
    params={}

    params['M']   = 0.938
    params['M_h'] = 0.139

    params['x_bj']= 0.1
    params['z_h'] = 0.1
    params['Q']   = 10.0
    params['T_t'] = 0.1

    params['xi']  = 0.3
    params['zeta']= 0.3
    params['delta_k_t']=0.1
    params['k_i_t']=0.01
    params['M_ki']=0.1
    params['M_kf']=0.1
    return params

def evaluate(func,params=None,verb=False):
    if params==None: params=gen_params()
    keys=['M','M_h','x_bj','z_h','Q','T_t','xi','zeta','delta_k_t','k_i_t','M_ki','M_kf']
    args=[params[_] for _ in keys]
    return func(*args)

@app.callback(
     Output('ri_zh', 'figure'),
    [Input('xb' , 'value'),
     Input('Q'  , 'value'),
     Input('qT' , 'value'),
     Input('Mki', 'value'),
     Input('Mkf', 'value'),
     Input('dkT', 'value'),
     Input('kiT', 'value')
    ])
def update_output1(xb,Q,qT,Mki,Mkf,dkT,kiT):
    params=gen_params()
    params['M_ki']=Mki
    params['M_kf']=Mkf
    params['T_t']=qT
    params['delta_k_t']=dkT
    params['k_i_t']=kiT
    params['xi']=xb
    params['x_bj']=xb
    params['Q']=Q
    
    zh=np.linspace(0.1,1,100)
    params['z_h']=zh
    params['zeta']=zh
    
    R={}
    R[1]=evaluate(rat.get_R1,params)
    R[2]=evaluate(rat.get_R2,params)
    R[3]=evaluate(rat.get_R3,params)
    for _ in R: R[_]=np.abs(R[_])

    nrows,ncols=1,3
    fig = py.figure(figsize=(ncols*3,nrows*3))
    AX={}
    AX[1]=py.subplot(nrows,ncols,1)
    AX[2]=py.subplot(nrows,ncols,2)
    AX[3]=py.subplot(nrows,ncols,3)
    
    for i in [1,2,3]:
        AX[i].plot(zh,R[i])
        AX[i].set_ylim(0,1)
        AX[i].set_xlim(0,1)
        AX[i].set_xlabel('z_h')
        AX[i].set_ylabel('R_%d'%i)
        #AX[i].tick_params(axis='both', which='major',labelsize=13)

    return mpl_to_plotly(fig)


#######################################################
p2layout = html.Div([
    dcc.Link('Go back to home', href='/'),
    html.Br(),
    html.H1('Example 1'),

    dcc.Graph(id='ex1'),

    html.Div(children='a' ) , html.Div(gen_slider('a' , -0.9,  1.0,  0.1, 0.5),style=style),
    html.Div(children='b' ) , html.Div(gen_slider('b' ,  0.0, 10.0,  0.1, 5.0),style=style),

])


@app.callback(
     Output('ex1', 'figure'),
    [Input('a', 'value'),
     Input('b', 'value')
    ])
def update_output2(a,b):
    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*4,nrows*4))
    ax=py.subplot(nrows,ncols,1)
    X=np.linspace(0,1,100)
    Y=X**a*(1-X)**b
    ax.plot(X,Y)
    #ax.set_ylim(0,.05)
    ax.set_xlim(0,1)
    return mpl_to_plotly(fig)


#######################################################
# Update the index
@app.callback(Output('page-content', 'children'),
             [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/ri-vs-zh':
        return p1layout
    elif pathname == '/example1':
        return p2layout
    else:
        return index_page


if __name__ == '__main__':

    app.run_server(debug=True)


