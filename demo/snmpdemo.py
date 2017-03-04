#!encoding=utf8

__author__ = 'mutalisk'

from twisted.internet import reactor
from twistedsnmp import snmpprotocol, agentproxy
from twisted.internet.defer import inlineCallbacks
from txsched.scheduler import ScheDuler
import time


def nm_snmpbulk(ip, port, comm_ro, snmp_version, oids, timeout, retry_times):
    proxy = agentproxy.AgentProxy(ip, port, comm_ro, snmp_version, SNMPPORT.get_proto())
    return proxy.get(oids, timeout, retry_times)


def nm_snmpwalk(ip, port, comm_ro, snmp_version, oids, timeout, retry_times):
    proxy = agentproxy.AgentProxy(ip, port, comm_ro, snmp_version, SNMPPORT.get_proto())
    return proxy.getTable(oids, timeout, retry_times)


class SNMPConf(object):
    port = 161
    timeout = 0.5
    retry_times = 1
    snmp_version = "v2"

    def __init__(self):
        pass


class SNMPPORT(object):
    proto = None

    def __init__(self):
        pass

    @staticmethod
    def get_proto():
        if SNMPPORT.proto is None:
            SNMPPORT.proto = snmpprotocol.port().protocol
        return SNMPPORT.proto


class SNMPDemo:
    def __init__(self):
        pass

    @inlineCallbacks
    def start(self, param):
        ip, comm_ro = param[0], param[1]
        port, snmp_version = SNMPConf.port, SNMPConf.snmp_version
        timeout, retry_times = SNMPConf.timeout, SNMPConf.retry_times

        result = yield nm_snmpbulk(ip, port, comm_ro, snmp_version,
                                   ['.1.3.6.1.2.1.1.1.0',  '.1.3.6.1.2.1.1.2.0',
                                    '.1.3.6.1.2.1.1.3.0', '1.3.6.1.2.1.25.1.5.0',
                                    '1.3.6.1.2.1.25.1.6.0', '1.3.6.1.2.1.25.2.2.0'],
                                   timeout, retry_times)
        print result

        result = yield nm_snmpwalk(ip, port, comm_ro, snmp_version,
                                   ['1.3.6.1.2.1.25.4.2.1.2'],
                                   timeout, retry_times)
        print result

        result = yield nm_snmpwalk(ip, port, comm_ro, snmp_version,
                                   ['1.3.6.1.2.1.2.2.1.2'],
                                   timeout, retry_times)
        print result


if __name__ == '__main__':
    print time.asctime()
    snmpdemo = SNMPDemo()
    schedualer = ScheDuler(concurrent_max=100, task_worker=snmpdemo,
                           task_params=[("127.0.0.1", "public") for _ in range(1000)], retry_times=1)
    d = schedualer.start()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    print time.asctime()
