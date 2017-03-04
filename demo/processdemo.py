#!encoding=utf8

__author__ = 'mutalisk'

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from txsched.scheduler import ScheDuler
from twisted.internet.utils import getProcessOutput


class ProcessDemo:
    def __init__(self):
        pass

    @inlineCallbacks
    def start(self, args):
        result = yield getProcessOutput('df')
        print result

        yield getProcessOutput('sleep', ['1'])
        print 'sleep 1'


if __name__ == '__main__':
    processdemo = ProcessDemo()
    schedualer = ScheDuler(concurrent_max=3, task_worker=processdemo,
                           task_params=[None]*10, retry_times=1)
    d = schedualer.start()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()