import multiprocessing, multiprocessing.dummy
from logging import getLogger
from time import sleep, time
__all__ = ["MPQRunner", "ThreadRunner", "DummyRunner", "TaskRunner"]

class MPQRunner:
	def get_pool_class(self):
		return multiprocessing.Pool
	def __init__(self, process, **opts):
		self._pool = self.get_pool_class()(opts['processCnt'] if "processCnt" in opts else 4)
		self._process = process
		self._res = []
		self._ready = {}
	def add_task(self, task):
		thread = self._pool.apply_async(self._process, [task])
		thread.start = time()
		self._res.append(thread)
	def wait_task(self):
		while len(self._ready) < len(self._res):
			for ind, thread in enumerate(self._res):
				if ind in self._ready and self._ready[ind]:
					continue
				try:
					thread.get(0)
					self._ready[ind] = True
					getLogger("Task-%s"%(ind+1)).info("Task completed in %s. %d tasks completed", time() - thread.start, len(self._ready))
				except multiprocessing.TimeoutError:
					pass
			sleep(0.01)
	def results(self):
		return [item.get() for item in self._res]

class ThreadRunner(MPQRunner):
	def get_pool_class(self):
		return multiprocessing.dummy.Pool

class DummyRunner:
	def __init__(self, process):
		self._process = process
		self._res = []
	def add_task(self, task):
		self._res.append(self._process(task))
		getLogger("DummyRunner").info("Task %d completed", len(self._res))
	def wait_task(self):
		pass
	def results(self):
		return self._res

class TaskRunner:
	total_task = 0
	def __init__(self, process, engine=ThreadRunner, **engineopt):
		self._engine = engine(process, **engineopt)
	def add(self, task):
		self._engine.add_task(task)
		self.total_task += 1
	def run(self, printCase=False):
		getLogger("TaskRunner").info("%d task assigned", self.total_task)
		self._engine.wait_task()
		if printCase:
			print "\n".join(["Case #%d: %s"%(ind+1, x) for ind,x in enumerate(self._engine.results())])
		else:
			print "\n".join([str(x) for x in self._engine.results()])