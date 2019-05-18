#!/usr/bin/env python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent
from app import app
from apps import app1,app2,app3,app4,app5,app6,app7,app8,app9


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

server = app.server

index = html.Div([
    #dcc.Link('Go back to home', href='/'),

    dcc.Markdown(dedent('''
    # SIDIS regions analysis tool

    **About**: Numerical evaluation of ratios based on arXiv:1904.12882 

    Select available apps below:

    ---- 
    ''')),
    
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 1: R<sub>i</sub> vs. x<sub>Bj</sub>, z<sub>h</sub> : Makes heat map of R<sub>i</sub> in the plane of x<sub>Bj</sub>, z<sub>h</sub>
        '''
    )
),

    
    dcc.Link('app1(3D): R_i vs. (x_b, z_h) '        , href='/apps/app1'),html.Br(),html.Br(),
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 2: W<sup>2</sup><sub>SIDIS</sub> vs. x<sub>Bj</sub>, z<sub>h</sub> : Makes heat map of W<sup>2</sup><sub>SIDIS</sub> in the plane of x<sub>Bj</sub>, z<sub>h</sub>
        '''
    )
),    
    dcc.Link('app2(3D): W2_(SIDIS) vs. (x_b, z_h)'  , href='/apps/app2'),html.Br(),html.Br(),
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 3: y<sub>h</sub> vs. x<sub>Bj</sub>, z<sub>h</sub> : Makes heat map of y<sub>h</sub> in the plane of x<sub>Bj</sub>, z<sub>h</sub>
        '''
    )
),    
    
    dcc.Link('app3(3D): y_h vs. (xb, zh)'           , href='/apps/app3'),html.Br(),html.Br(),
    
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 4: W<sup>2</sup><sub>SIDIS</sub> vs. x<sub>Bj</sub>, Q : Makes heat map of W<sup>2</sup><sub>SIDIS</sub> in the plane of x<sub>Bj</sub>, Q
        '''
    )
),    
    dcc.Link('app4(2D): W2_SIDIS vs. (x_b, Q)'      , href='/apps/app4'),html.Br(),html.Br(),
    
    
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 5: x<sub>N</sub>/x<sub>Bj</sub> vs x<sub>Bj</sub> : Makes plot of x<sub>N</sub>/x<sub>Bj</sub> vs x<sub>Bj</sub> for JLab, HERMES and COMPASS
        '''
    )
),      
    dcc.Link('app5(2D): x_N/x_bj vs. x_b'           , href='/apps/app5'),html.Br(),html.Br(),
    
    
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 6: z<sub>N</sub>/z<sub>h</sub> vs. z<sub>h</sub> : Makes plot of <sub>N</sub>/z<sub>h</sub> vs z<sub>h</sub> for JLab, HERMES, and COMPASS
        '''
    )
),      
    dcc.Link('app6(2D): z_N/z_h vs. z_h'            , href='/apps/app6'),html.Br(),html.Br(),
    
        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 7: R<sub>i</sub> vs. x<sub>Bj</sub>, Q : Makes heat map of R<sub>i</sub> in the plane of x<sub>Bj</sub>, Q
        '''
    )
),      
    dcc.Link('app7(2D): R_i vs. (x_b, Q)'           , href='/apps/app7'),html.Br(),html.Br(),
    

        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 8: Ratios vs. x<sub>Bj</sub>, Q : Makes heat map of R<sub>i</sub>, x<sub>N</sub>/x<sub>Bj</sub> and z<sub>N</sub>/z<sub>h</sub> in the plane of x<sub>Bj</sub>, Q
        '''
    )
),      
    dcc.Link('app8(2D): rat_exp vs. (x_b, Q)'       , href='/apps/app8'),html.Br(),html.Br(),
    

        dcc.Markdown(
    dangerously_allow_html=True,
    children=dedent(
        u'''
        #### app 9: R<sub>i</sub> vs. q<sub>T</sub>/Q, y<sub>h</sub> : Makes heat map of R<sub>i</sub> in the plane of q<sub>T</sub>/Q, y<sub>h</sub>
        '''
    )
),      
    dcc.Link('app9(2D): qT/Q vs. rap'               , href='/apps/app9'),html.Br(),html.Br(),


    dcc.Markdown(dedent('''
    ----
    **Authors**:
 
        - N. Sato   (ODU/JLab)  (nsato@jlab.org)
        - S. Gordon (ODU) 
        - T. Rogers (ODU)
    ----
    **Acknowledgements**:

    The creation of this web app was supported by the U.S. Department of
    Energy, Office of Science, Office of Nuclear Physics, under Award Number
    DE-SC0018106.
    ''')),


   ]) 


@app.callback(Output('page-content', 'children'),[ Input('url', 'pathname')])
def update(url):
    if    url=='/apps/app1': return app1.layout
    elif  url=='/apps/app2': return app2.layout
    elif  url=='/apps/app3': return app3.layout
    elif  url=='/apps/app4': return app4.layout
    elif  url=='/apps/app5': return app5.layout
    elif  url=='/apps/app6': return app6.layout
    elif  url=='/apps/app7': return app7.layout
    elif  url=='/apps/app8': return app8.layout
    elif  url=='/apps/app9': return app9.layout
    else: return index 

if __name__ == '__main__':
    app.run_server(debug=True)



