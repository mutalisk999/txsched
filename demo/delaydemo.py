#!encoding=utf8

__author__ = 'mutalisk'

from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from txsched.scheduler import ScheDuler


def f1():
    import time
    return 'f1', time.time()


def f2():
    import time
    return 'f2', time.time()


class DelayDemo:
    def __init__(self):
        pass

    @inlineCallbacks
    def start(self, delay):
        result = yield task.deferLater(reactor, delay, f1)
        print result

        result = yield task.deferLater(reactor, delay, f2)
        print result

if __name__ == '__main__':
    delaydemo = DelayDemo()
    schedualer = ScheDuler(concurrent_max=3, task_worker=delaydemo, task_params=[1]*10, retry_times=1)
    d = schedualer.start()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
