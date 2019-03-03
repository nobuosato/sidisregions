pip install dash
pip install dash-renderer
pip install dash-core-components
pip install dash-html-components
pip install plotly
pip install gunicorn
pip freeze > requirements.txt

#heroku create toy # change my-dash-app to a unique name
#git add . # add all files to git
#git commit -m 'Initial app boilerplate'
#git push #heroku master # deploy code to heroku
#heroku ps:scale web=1  # run the app with a 1 heroku "dyno"
