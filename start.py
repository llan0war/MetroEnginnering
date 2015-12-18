from flask import Flask, render_template, redirect, Response
from core.main import Simulation, default_config
import datetime
import os

app = Flask(__name__)

config = default_config()
sim = Simulation(config)


@app.route('/')
def control():
    return render_template('index.html', cfg_st=True)


@app.route('/simulate/')
def simulate():
    pass


@app.route('/config/')
def show_config():
    return render_template('config', config)


@app.route('/config/apply/')
def update_config():
    return

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