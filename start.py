from flask import Flask, render_template, redirect, request

from core.main import Simulation, default_config

# from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import BooleanField, IntegerField, FloatField, DateTimeField

app = Flask(__name__)
app.config.from_object('config')

config = default_config()
sim = Simulation(config)
simulated = False


class ConfigForm(Form):
    global config
    # Module
    production_bonus = FloatField('production_bonus', default=config.get('module').get('production_bonus'),
                                  description='MODULE: production bonus per perk')
    fail_bonus = FloatField('fail_bonus', default=config.get('module').get('fail_bonus'),
                            description='MODULE: value to substract from fail per perk')
    fuel_bonus = FloatField('fuel_bonus', default=config.get('module').get('fuel_bonus'),
                            description='MODULE: value to substract from fuel usage per perk')
    # Base
    prod = FloatField('prod', default=config.get('base').get('prod'), description='BASE: default production value')
    prod_max = FloatField('prod_max', default=config.get('base').get('prod_max'),
                          description='BASE: max storage capacity')
    base_fail = FloatField('base_fail', default=config.get('base').get('base_fail'),
                           description='BASE: default fail chance')
    max_modules = FloatField('max_modules', default=config.get('base').get('max_modules'),
                             description='BASE: max connected modules')
    fuel_refill = FloatField('fuel_refill', default=config.get('base').get('fuel_refill'), description='BASE: ')
    fuel_base_cons = FloatField('fuel_base_cons', default=config.get('base').get('fuel_base_cons'),
                                description='BASE: default fuel consumption')
    connections = FloatField('connections', default=config.get('base').get('connections'),
                             description='BASE: default number of connections')
    start_fuel = FloatField('start_fuel', default=config.get('base').get('start_fuel'),
                            description='BASE: starting fuel count')
    # Station
    fuel_sources = FloatField('fuel_sources', default=config.get('station').get('fuel_sources'),
                              description='STATION: default fuel sources count')
    # Game
    fuel_pool = FloatField('fuel_pool', default=config.get('game').get('fuel_pool'),
                           description='GAME: starting fuel sources in game')
    no_event_treshold = FloatField('no_event_treshold', default=config.get('game').get('no_event_treshold'),
                                   description='GAME: time without events before new event generated')
    random_events = BooleanField('random_events', default=config.get('game').get('random_events'),
                                 description='GAME: set checked to generate random events')
    # Simulation
    start = DateTimeField('start', default=config.get('simulation').get('start'),
                          description='SIMULATION: start date and time')
    end = DateTimeField('end', default=config.get('simulation').get('end'), description='SIMULATION: end date and time')
    tdelta = IntegerField('tdelta', default=config.get('simulation').get('tdelta'),
                          description='SIMULATION: time for one internal cycle')


@app.route('/')
def control():
    global sim, simulated
    return render_template('index.html', polygon=sim.polygon.endgame(), simulated=simulated)


@app.route('/simulate/')
def simulate():
    global config, sim, simulated
    sim = Simulation(config)
    sim.simulate()
    simulated = True
    return redirect('/')


@app.route('/config/', methods=['GET', 'POST'])
def config_module():
    form = ConfigForm()
    if request.method == 'POST':
        global simulated
        simulated = False
        for _ in form.data.keys():
            update_config(_, form.data.get(_))
        return redirect('/config/')
    return render_template('editor.html', form=form)


def update_config(key, val):
    global config
    for _ in config.keys():
        for __ in config.get(_).keys():
            if __ == key:
                config[_][__] = val
                break


@app.route('/charts/')
def charts(chartID='chart_ID', chart_type='line', chart_height=350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    series = [{"name": 'Label1', "data": [1, 2, 3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    charts = chart_builder(history_parser())
    return render_template('charts.html', charts=charts, prod=charts['total_energy_producted'],
                           fail=charts['disable_chance'])


def chart_builder(data):
    res = {}
    for type_desc in data.keys():
        res[type_desc] = {}
        res[type_desc]['chartID'] = type_desc
        res[type_desc]['chart'] = {"renderTo": type_desc, "type": 'line', "height": '350'}
        res[type_desc]['title'] = {'text': type_desc}
        res[type_desc]['xAxis'] = {"categories": [_ for _ in range(0, len(next(iter(data.get(type_desc).values()))))]}
        res[type_desc]['yAxis'] = {'title': 'what?'}
        res[type_desc]['series'] = [{'name': name, 'data': val} for name, val in data.get(type_desc).items()]
    return res


def history_parser():
    stations = [_ for _ in sim.history[1].keys() if _ != 'events']
    types = {'production': 'total_production',
             'producted': 'total_energy_producted',
             'fail': 'disable_chance',
             'fuel_cons': 'fuel_consumation',
             'fuel_storage': 'remainig_fuel',
             'am': 'attached_modules'}
    res = {_: {__: [] for __ in stations} for _ in types.values()}  # {type: {station: []}}

    for type, desc in types.items():
        for station in stations:
            for round in sim.history.keys():
                res[desc][station].append(sim.history[round][station][type])
    return res


if __name__ == '__main__':
    app.run(debug=True)