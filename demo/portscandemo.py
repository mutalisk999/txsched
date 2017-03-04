#!encoding=utf8

__author__ = 'mutalisk'

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.defer import inlineCallbacks
from txsched.scheduler import ScheDuler


class PortScanProtocol(Protocol):
    def __init__(self, port):
        self.port = port

    def connectionMade(self):
        print 'port', self.port, 'is open'
        self.transport.loseConnection()


class PortScanDemo:
    def __init__(self):
        pass

    @inlineCallbacks
    def start(self, args):
        scan_ip, scan_port = args
        point = TCP4ClientEndpoint(reactor, scan_ip, scan_port)
        yield connectProtocol(point, PortScanProtocol(scan_port))


if __name__ == '__main__':
    portscandemo = PortScanDemo()
    schedualer = ScheDuler(concurrent_max=500, task_worker=portscandemo,
                           task_params=[("127.0.0.1", i + 1) for i in range(10000)], retry_times=1)
    d = schedualer.start()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
