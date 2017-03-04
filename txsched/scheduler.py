#!encoding=utf8

__author__ = 'mutalisk'

from twisted.internet.defer import DeferredList, inlineCallbacks


class ScheDuler:
    def __init__(self, **kwargs):
        self.concurrent_max = kwargs['concurrent_max']
        self.task_worker = kwargs['task_worker']
        self.task_params = kwargs['task_params']
        self.retry_times = kwargs['retry_times']
        self.task_number = len(self.task_params)

    @inlineCallbacks
    def task_run(self):
        while True:
            if len(self.task_params) == 0:
                break
            else:
                task_params = self.task_params.pop(0)
                retry_times = self.retry_times
                while retry_times > 0:
                    try:
                        yield self.task_worker.start(task_params)
                        break
                    except Exception, ex:
                        print str(ex)
                        pass
                    retry_times -= 1

    @inlineCallbacks
    def start(self):
        if self.task_number < self.concurrent_max:
            self.concurrent_max = self.task_number
        yield DeferredList([self.task_run() for _ in range(self.concurrent_max)])
