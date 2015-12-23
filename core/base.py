import random


class Base(object):
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.modules = []
        self.connected_modules = []
        self.production = config['base']['prod']
        self.producted = 0
        self.fail = config['base']['base_fail']
        self.state = True
        self.max_prod = config['base']['prod_max']
        self.disables = 0
        self.connections = config['base']['connections']
        self.max_modules = config['base']['max_modules']
        self.no_fails = 0
        self.fuel_refill = config['base']['fuel_refill']
        self.fuel = config['base']['start_fuel']
        self.events = []
        self.fuel_cons = config['base']['fuel_base_cons']
        self.no_fail_treshold = config['base']['no_fail_treshold']
        self.fail_penalty = config['base']['fail_penalty']
        self.fuel_used = 0

    def tick(self):
        self.events.clear()
        if self.state:
            if not self.check_fail():
                self.producted = int(self.producted * (100 - self.fail_penalty) / 100)
                self.events.append(' Base broken')
                return 0
            if self.fuel_state():
                prod = self.production
                for _ in self.connected_modules:
                    prod += _.production
                self.producted += prod if self.producted < self.max_prod else self.max_prod
                return prod
            else:
                self.events.append(' out of fuel')
        return 0

    def check_fail(self):
        self.no_fails += 1
        if self.no_fails > self.no_fail_treshold:
            fail = self.fail + sum([_.failure for _ in self.connected_modules])
            self.state = random.randint(0, 100) > fail
            if not self.state:
                self.disables += 1
                self.no_fails = 0
        return self.state

    def fuel_state(self):
        self.fuel -= self.fuel_consumption()
        if self.fuel > 0:
            self.fuel_used += self.fuel_consumption()
            return True
        self.fuel = 0
        return False

    def fuel_consumption(self):
        res = self.fuel_cons
        for _ in self.connected_modules:
            res += _.fuel
        return res

    def total_production(self):
        res = self.production
        for _ in self.connected_modules:
            res += _.production
        return res

    def get_fail(self):
        return self.fail + sum([_.failure for _ in self.connected_modules])

    def repair(self):
        if not self.state:
            self.state = True

    def add_module(self, module):
        self.modules.append(module)
        self.composite_modules()

    def composite_modules(self):
        self.connected_modules.clear()
        done = False
        while not done:
            if (len(self.connected_modules) < self.max_modules) and (len(self.connected_modules) < len(self.modules)):
                if self._free_connections() > 0:
                    curr = self._find_top_level()
                    self.connected_modules.append(curr)
                else:
                    if not self._add_another_modules():
                        done = True
            else:
                done = True

    def _find_top_level(self):
        possibilities = [_ for _ in self.modules if _ not in self.connected_modules]
        res = possibilities[0]
        for _ in possibilities:
            if _.level > res.level:
                res = _
        return res

    def _find_low_level(self):
        possibilities = [_ for _ in self.modules if _ not in self.connected_modules]
        res = possibilities[0]
        for _ in possibilities:
            if _.level < res.level:
                res = _
        return res

    def _add_another_modules(self):
        if len(self.connected_modules) < self.max_modules:
            possibilities = [_ for _ in self.modules if _ not in self.connected_modules]
            for module in possibilities:
                if module.connections > 0:
                    self.connected_modules.append(module)
                    return True
        return False

    def sell_module(self):
        target = self._find_low_level()
        self.modules.remove(target)
        return target

    def _free_connections(self):
        res = 0
        for _ in self.connected_modules:
            res += _.connections
        return res + self.connections - len(self.connected_modules)

    def __repr__(self):
        # return '  Modules: {m:5}\n  Connected: {cn:5}'.format(m='\n'.join([str(_) for _ in self.modules]),
        # cn='\n'.join([str(_) for _ in self.connected_modules]))
        return '{name} base, fails: {f}\n  modules: {mods}\n  connected: {cm}' \
            .format(name=self.name,
                    f=self.disables,
                    mods=','.join([str(_) for _ in self.modules]),
                    cm=','.join([str(_) for _ in self.connected_modules]))

    def fuel_recharge(self):
        self.fuel = self.fuel_refill

    def modules_sum(self):
        if len(self.connected_modules) > 0:
            return sum([_.level for _ in self.connected_modules])
        return 0