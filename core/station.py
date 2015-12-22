import random

from core.base import Base


class Station(object):
    def __init__(self, name, config):
        self.config = config
        self.base = Base(name, config)
        self.name = name
        self.power = 0  # abstract res for find modules
        self.resources = 0
        self.fuel_sources = config['station']['fuel_sources']
        self.events = []

    def tick(self):
        self.events.clear()
        self.power += random.randint(1, 2)
        self.res_is_full()
        self.base_status()
        self.get_res()

    def base_status(self):
        if not self.base.state:
            self.base.repair()
            self.events.append(' repair self base')
        if self.base.fuel < 1:
            if self.fuel_sources > 0:
                self.fuel_sources -= 1
                self.base.fuel_recharge()
                self.events.append(' refill their base')

    def aquire_modules(self, module):
        self.power = 0
        self.base.add_module(module)
        self.events.append(' aquired module {}'.format(str(module)))

    def aquire_fuel(self):
        self.power = 0
        self.fuel_sources += 1

    def res_is_full(self):
        if self.base.producted > self.base.max_prod / 2:
            decision = random.randint(0, 100) < (self.base.producted / self.base.max_prod) * 100
            if decision:
                self.events.append(' is full {}/{}, emptyng'.format(self.base.producted, self.base.max_prod))
                self.resources += self.base.producted
                self.base.producted = 0

    def get_res(self):
        self.base.tick()
        self.events.extend(self.base.events)

    def __repr__(self):
        stat = 'Station: {name} modules:{mod} active:{am} producted: {prod} fail: {fail}% fuel cons: {fuel}' \
            .format(mod=len(self.base.modules),
                    name=self.name,
                    am=len(self.base.connected_modules),
                    prod=self.resources,
                    fail=self.base.get_fail(),
                    fuel=self.base.fuel_consumption())
        return stat + '\n' + str(self.base)

    def sell_module(self):
        return self.base.sell_module()

    def get_fuel(self):
        return self.base.fuel + self.fuel_sources * self.base.fuel_refill

    def stats(self):
        res = dict(mod=len(self.base.modules),
                   name=self.name,
                   am=len(self.base.connected_modules),
                   producted=self.resources,
                   fail=self.base.get_fail(),
                   fuel_cons=self.base.fuel_consumption(),
                   production=self.base.total_production(),
                   fuel_storage=self.base.fuel,
                   module_levels=self.base.modules_sum())
        return res

    def disables_count(self):
        return self.base.disables

    def used_fuel(self):
        return self.base.fuel_used