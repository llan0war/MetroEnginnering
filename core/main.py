import datetime

from core.game import Game


class Simulation(object):
    def __init__(self, config):
        self.config = config
        self.start = config['simulation']['start']
        self.end = config['simulation']['end']
        self.tdelta = datetime.timedelta(minutes=config['simulation']['tdelta'])
        self.polygon = Game(config)
        self.history = {}
        self.now = config['simulation']['start']
        self.simulated = False

    def events_printer(self, events):
        res = '\n'.join(
            ['\n'.join(['{} {}'.format(station, _) for _ in events.get(station)]) for station in events.keys() if
             len(events.get(station)) > 0])
        # for station in events.keys():
        # res += '\n'.join(['{} {}'.format(station, _) for _ in events.get(station)])
        return res

    def simulate(self):
        while self.now < self.end:
            self.now += self.tdelta
            rand = int((self.now - self.start).total_seconds() / 60)
            print('Starting round {}[{}]'.format(self.now.strftime('%H-%M-%d'), rand))
            self.polygon.tick(self.now - self.start)
            if rand in self.history.keys():
                exit(1)
            else:
                self.history[rand] = self.station_stats()
            self.history[rand]['events'] = self.polygon.events

            print(self.events_printer(self.polygon.events))
        self.endgame()
        self.simulated = True

    def endgame(self):
        print(self.polygon.endgame())
        print('All modules({}):'.format(len(self.polygon.all_modules())))
        print('\n'.join(self.polygon.all_modules()))

    def station_stats(self):
        res = {}
        for station in self.polygon.stations:
            res[station.name] = station.stats()
        return res


def default_config():
    globs = {
        'simulation': {
            'start': datetime.datetime(year=2016, month=1, day=10, hour=22, minute=0),
            'end': datetime.datetime(year=2016, month=1, day=11, hour=1, minute=0),
            'tdelta': 1
        },
        'game': {
            'gl_events': {  # number its level of module, range 1-4
                            # 5 is one fuel source
                            5: [1, 1, 1, 1, 1, 1, 1, 5],
                            67: [2, 2, 2, 2, 5],
                            127: [2, 2, 2, 5],
                            187: [3, 3, 5],
                            217: [3, 3, 5],
                            407: [4, 5],
                            507: [4],
                            607: [4, 4],
                            707: [4]
                            },
            'fuel_pool': 1,
            'no_event_treshold': 45,
            'random_events': True
        },
        'station': {
            'fuel_sources': 1
        },
        'base': {
            'prod': 2,
            'prod_max': 500,
            'base_fail': 0,
            'max_modules': 9,
            'fuel_refill': 1000,
            'fuel_base_cons': 3,
            'no_fail_treshold': 30,
            'connections': 3,
            'start_fuel': 1000,
            'fail_penalty': 20
        },
        'module': {
            'all_perks': ['prod',  # +1 production
                          'batt',  # -1 fuel cost
                          'fail',  # -0.5 fail chance
                          'conn'],  # +1 connection
            'production_bonus': 1,
            'fail_bonus': 0.5,
            'fuel_bonus': 1
        }
    }
    return globs


if __name__ == '__main__':
    sim = Simulation(default_config())
    sim.simulate()

