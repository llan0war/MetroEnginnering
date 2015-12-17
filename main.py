import csv
from game import Game
import datetime

history = {}


def do_history(polygon, num):
    history[rand] = {

    }


def write_history(num, data):
    with open('{num}.csv'.format(num=str(num)), 'w') as f:
        print('Writing to file ' + str(f.name))
        wrt = csv.writer(f, delimiter=';')
        wrt.writerow(['timestamp', 'ccu'])
        for time in sorted(data.keys()):
            print('ready to write %s' % ([time, data.get(time)]))
            wrt.writerow([time, data.get(time)])


def events_printer(events):
    for station in events.keys():
        for _ in events.get(station):
            print('{} {}'.format(station, _))

if __name__ == '__main__':
    start = datetime.datetime(year=2016, month=1, day=10, hour=22, minute=0)
    end = datetime.datetime(year=2016, month=1, day=11, hour=12, minute=0)
    tdelta = datetime.timedelta(minutes=1)
    now = start
    polygon = Game()

    while now < end:
        now += tdelta
        rand = int((now - start).total_seconds() / 60)
        print('Starting round {}[{}]'.format(now.strftime('%H-%M-%d'), rand))
        polygon.tick(now - start)
        events_printer(polygon.events)
        do_history(polygon, rand)

    print(polygon.endgame())
    print('All modules({}):'.format(len(polygon.all_modules())))
    print('\n'.join(polygon.all_modules()))