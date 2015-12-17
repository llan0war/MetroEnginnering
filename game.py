from station import Station
from module import Module
import random


GL_EVENTS = {  # number its level of module, range 1-4
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
}

MODULES_POOL = []
FUEL_POOL = 1
NO_EVENT_TRESHOLD = 45


class Game(object):
    def __init__(self):
        self.stations = [Station('Ganza'), Station('Lubanka'), Station('Nazi'), Station('Polis'), Station('Dirty')]
        self.empty_rounds = 0
        self.events = {}

    def tick(self, time):
        self.events.clear()
        self.events['global'] = [' fuel_sources: {} modules {}'.format(FUEL_POOL, len(MODULES_POOL))]
        time = int(time.total_seconds() / 60)
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
            global FUEL_POOL
            if winner.fuel_sources == 0 and FUEL_POOL > 0:
                winner.aquire_fuel()
                FUEL_POOL -= 1
            elif len(MODULES_POOL) > 0:
                winner.aquire_modules(MODULES_POOL.pop(0))

    def do_events(self, mins):
        if mins in GL_EVENTS.keys():
            self.empty_rounds = 0
            if not self.events.get('global', False):
                self.events['global'] = []
            event = GL_EVENTS.get(mins)
            for _ in event:
                if _ in [1, 2, 3, 4]:
                    MODULES_POOL.append(Module(_))
                    self.events['global'].append('Event - spawned module')
                elif _ == 5:
                    global FUEL_POOL
                    FUEL_POOL += 1
                    self.events['global'].append('Added new fuel source')

    def generate_events(self, mins):
        self.empty_rounds += 1
        if self.empty_rounds > NO_EVENT_TRESHOLD:
            self.empty_rounds = 0
            if mins + 1 not in GL_EVENTS.keys():
                if not self.events.get('global', False):
                    self.events['global'] = []
                event = [random.randint(1, 2) for _ in range(0, random.randint(1, 4))]
                if random.randint(0, 3) > 0:
                    event.extend([5, 5])
                self.events['global'].append('New event generated {}'.format(event))
                GL_EVENTS[mins + 1] = event

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
            MODULES_POOL.append(deal)
            if not self.events.get('global', False):
                self.events['global'] = []
            self.events['global'].append('{name} sells module {mod}'.format(name=station.name, mod=str(deal)))