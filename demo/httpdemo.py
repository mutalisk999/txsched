#!encoding=utf8

__author__ = 'mutalisk'

from twisted.internet import reactor
from twisted.web.client import Agent, readBody
from twisted.internet.defer import inlineCallbacks
from twisted.web.http_headers import Headers
from txsched.scheduler import ScheDuler
from zope.interface import implements
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer


class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class HttpGetDemo:
    def __init__(self):
        pass

    @inlineCallbacks
    def start(self, url):
        agent = Agent(reactor)
        response = yield agent.request(
            'GET', url,
            Headers({'User-Agent': ['Twisted Web Client Example']}),
            None)

        body = yield readBody(response)
        print len(body)


class HttpPostDemo:
    def __init__(self):
        pass

    @inlineCallbacks
    def start(self, url):
        agent = Agent(reactor)
        response = yield agent.request(
            'POST', url,
            Headers({'User-Agent': ['Twisted Web Client Example']}),
            StringProducer('test'))

        body = yield readBody(response)
        print len(body)


if __name__ == '__main__':
    httpgetdemo = HttpGetDemo()
    schedualer = ScheDuler(concurrent_max=3, task_worker=httpgetdemo,
                           task_params=['http://www.baidu.com']*100, retry_times=1)
    d = schedualer.start()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
