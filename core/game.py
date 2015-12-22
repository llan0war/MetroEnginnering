import random

from core.station import Station
from core.module import Module


class Game(object):
    def __init__(self, config):
        self.config = config
        self.stations = [Station('Ganza', config),
                         Station('Lubanka', config),
                         Station('Nazi', config),
                         Station('Polis', config),
                         Station('Dirty', config)]
        self.gl_events = config['game']['gl_events']
        self.modules_pool = []
        self.fuel_pool = config['game']['fuel_pool']
        self.no_event_treshold = config['game']['no_event_treshold']
        self.random_events = config['game']['random_events']
        self.empty_rounds = 0
        self.events = {}

    def tick(self, time):
        self.events.clear()
        self.events['global'] = [' fuel_sources: {} modules {}'.format(self.fuel_pool, len(self.modules_pool))]
        time = int(time.total_seconds() / 60)
        if self.random_events:
            self.generate_events(time)
        self.do_events(time)
        self.aquire_items()
        for _ in self.stations:
            self.move_module(_)
            _.tick()
            self.events[_.name] = _.events

    def aquire_items(self):
        challengers = [_ for _ in self.stations if _.power > 30]
        if len(challengers) > 0:
            winner = random.choice(challengers)
            if winner.fuel_sources == 0 and self.fuel_pool > 0:
                winner.aquire_fuel()
                self.fuel_pool -= 1
            elif len(self.modules_pool) > 0:
                winner.aquire_modules(self.modules_pool.pop(0))

    def do_events(self, mins):
        if mins in self.gl_events.keys():
            self.empty_rounds = 0
            if not self.events.get('global', False):
                self.events['global'] = []
            event = self.gl_events.get(mins)
            for _ in event:
                if _ in [1, 2, 3, 4]:
                    self.modules_pool.append(Module(_, self.config))
                    self.events['global'].append('Event - spawned module')
                elif _ == 5:
                    self.fuel_pool += 1
                    self.events['global'].append('Added new fuel source')

    def generate_events(self, mins):
        self.empty_rounds += 1
        if self.empty_rounds > self.no_event_treshold:
            self.empty_rounds = 0
            if mins + 1 not in self.gl_events.keys():
                if not self.events.get('global', False):
                    self.events['global'] = []
                event = [random.randint(1, 2) for _ in range(0, random.randint(1, 4))]
                if random.randint(0, 3) > 0:
                    event.extend([5, 5])
                self.events['global'].append('New event generated {}'.format(event))
                self.gl_events[mins + 1] = event

    def endgame(self):
        res = '\n'.join([str(_) for _ in self.stations])
        return res

    def all_modules(self):
        mods = []
        for _ in self.stations:
            mods.extend([str(i) for i in _.base.modules])
        return mods

    def move_module(self, station):
        if len(station.base.modules) > 9:
            deal = station.sell_module()
            self.modules_pool.append(deal)
            if not self.events.get('global', False):
                self.events['global'] = []
            self.events['global'].append('{name} sells module {mod}'.format(name=station.name, mod=str(deal)))

    def disables_count(self):
        return {_.name: _.disables_count() for _ in self.stations}

    def fuel_used(self):
        return {_.name: _.used_fuel() for _ in self.stations}