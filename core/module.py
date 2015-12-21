import random
import string

random.seed()


class Module(object):
    grade = {
        1: 2,  # white
        2: 3,  # green
        3: 3,  # blue
        4: 3  # violette
    }

    def __init__(self, level, config):
        self.production = 0
        self.failure = 0
        self.fuel = 0
        self.max_prod = 0
        self.all_perks = config['module']['all_perks']
        self.__production_bonus = config['module']['production_bonus']
        self.__fuel_bonus = config['module']['fuel_bonus']
        self.__fail_bonus = config['module']['fail_bonus']

        self.perks = []
        self.level = level
        self.connections = 0
        self.__generate()
        self.__update_stats()
        self.id = self.__id_gen()

    def __generate(self):
        for _ in range(0, self.grade.get(int(self.level), 2)):
            kk = random.choice(self.all_perks)
            if kk == 'conn':
                if 'conn' not in self.perks:
                    self.perks.append(kk)
                else:
                    self.perks.append('prod')
            else:
                self.perks.append(kk)

    def __update_stats(self):
        self.connections = 0
        self.failure = int(self.level) / 4
        self.fuel = self.level
        if self.level == 3:
            if 'conn' not in self.perks:
                self.perks.append('conn')
            else:
                self.perks.append('prod')

        if self.level == 4:
            if 'conn' not in self.perks:
                self.perks.append('conn')
            else:
                self.perks.append('prod')
            self.perks.append('prod')

        for _ in self.perks:
            if _ == 'prod':
                self.production += self.__production_bonus
            elif _ == 'batt':
                self.fuel -= self.__fuel_bonus
            elif _ == 'fail':
                self.failure -= self.__fail_bonus
            elif _ == 'conn':
                self.connections += 1
            else:
                print('error in parsing perks')
                exit(1)

    def stats(self):
        return 'Level: {level} prod {prod} fail {fail} conn {conn}\nperks {perks} '.format(level=self.level,
                                                                                           prod=self.production,
                                                                                           fail=self.failure,
                                                                                           conn=self.connections,
                                                                                           perks=', '.join(self.perks))

    def __id_gen(self):
        return '{l}{perks}#{hash}'.format(perks=''.join([_[0] for _ in self.perks]),
                                          hash=''.join(
                                              random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
                                          l=str(self.level))

    def __repr__(self):
        return self.id