from flask import Flask, render_template, redirect, Response
from core.main import Simulation, default_config
import datetime
import os

app = Flask(__name__)

start = datetime.datetime(year=2016, month=1, day=10, hour=22, minute=0)
end = datetime.datetime(year=2016, month=1, day=11, hour=12, minute=0)
tdelta = datetime.timedelta(minutes=1)
config = default_config()
sim = Simulation(config)

@app.route('/')
def control():
    return render_template('index.html', cfg_st=True)

@app.route('/simulate/')
def simulate():
    pass

@app.route('/bootstrap/css/<path>')
def load_css(path):
    fullpath = os.getcwd() + '/templates/bootstrap/css/' + path
    if os.path.exists(fullpath):
        with open(fullpath) as f:
            data = f.read()
        return Response(response=data, mimetype='text/css')
    return 'Fail!'

if __name__ == '__main__':
    app.run()