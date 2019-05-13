# sidis

## getting started. 

- create a python eviroment:  $ conda create --name snakes python=3.6

- acticate the envirment:     $ conda activate snakes

- intall the following packegs via pip

    pip install dash
    pip install dash-core-components
    pip install dash-daq
    pip install dash-html-components
    pip install dash-renderer
    pip install dash-table
    pip install plotly

- run the program:            $ ./index.py

- use your browser and got to http://127.0.0.1:8050/


## code organization

- index.py is the entry of the prgram. Here we specify the layout 
  of the homepage and the available apps.  

- the apps are located inside the folder apps/appsX.py. 

- code_gen.py generates the ratlib.py which contains all the functions 
  to compute the ratios.  

- aux.py contans helpers to for numerical evaluation

## warm up tutorial to get started

- First revise the code_gen.py and see if you understand the logic.

- Create your own script to load ratlib and evalute the ratio functions 
  using the helpers at aux.py. See the function test as code_gen.py

- Not that you know how the ratlib works, go to the apps and pick up 
  an app and revise its code. 

- We use dash, which is the magic behind the scenes. The basic ingridients 
  are layouts and call backs. Refer to dash tutorial for more info. 

- Try to create your own app. 




