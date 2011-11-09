from panda3d.direct.task import Task
from panda3d.pandac import NodePath

import __builtin__
if __builtin__.__dict__.has_key("scheduler"):
  raise Exception("Circular reference to scheduling module")

#-------------------------------------------------------------------------------

class Scheduler(object):
  '''Simulation scheduler.
  This class handles the simulation clock and task scheduling. Every simulation
  time task in the should use this class methods instead of the standard taskMgr
  ones, which should still be used for system related tasks (gui, event
  handling, etc.)
  '''
  def __init__(self):
    object.__init__(self)

    self.realTime    = True
    self.skipFrames  = True
    self.pause       = False
    self._time       = 0
    self.lastTime    = -1
    self.times       = []
    self.tasks       = {}
    self.schedule    = {}
    self.renderTasks = []
    taskMgr.add(self.dispatcher, "morselDispatcher", -20)

#-------------------------------------------------------------------------------

  def togglePause(self):
    ''' Pause/unpause the simulation.
    This toggles the pause state for the simulation, it should be noted that
    system tasks are still handled by the engine.
    '''
    self.pause = not self.pause

#-------------------------------------------------------------------------------

  def setRealTime(self, value):
    ''' Chooses between real/virtual simulation time.
    On real time, one simulation second corresponds to one real second. Virtual
    time, on the other hand does not have any exact correspondance to real time,
    but is able to simulate arbitrary high frequency events.
    '''
    self.realTime = value

#-------------------------------------------------------------------------------

  def setSkipFrames(self, value):
    ''' Allows for skipping multiple scheduled tasks.
    When this flag is set to true, the simulator will only schedule each task
    once per render cycle.
    '''
    self.skipFrames = value

#-------------------------------------------------------------------------------

  def dispatcher(self, task):
    if self.lastTime == -1:
      self.lastTime = task.time
    if not self.pause:
      deltaTime = task.time - self.lastTime
      self._time += deltaTime
      self.dispatch()
      self.lastTime = task.time
    else:
      self.lastTime = -1
    return Task.cont

#-------------------------------------------------------------------------------

  def time(self):
    ''' Returns the simulator's time.'''
    if self.realTime:
      return self._time
    elif len(self.times) > 0:
      return self.times[0]
    else:
      return 0

#-------------------------------------------------------------------------------

  def dispatch(self):
    currentTime = self.time()
    processed = {}

    while len(self.times) > 0 and self.times[0] <= currentTime:
      t = self.times.pop(0)
      taskList = self.schedule.pop(t)

      for task in taskList:
        period = task["period"]
        if not self.skipFrames or not processed.has_key(task["name"]) or \
            period == 0:
          result = task["function"](t)
        else:
          result = True

        if result:
          if period > 0:
            self.scheduleTask(t + period, task)
          elif period == 0:
            self.scheduleTask(t + result, task)
        else:
          self.removeTask(task["name"])
        processed[task["name"]] = True
    for task in self.renderTasks:
      result = task["function"](currentTime)
      if not result:
        self.removeTask(task["name"])

#-------------------------------------------------------------------------------

  def scheduleTask(self, time, task):
    if self.schedule.has_key(time):
      self.schedule[time].append(task)
      self.schedule[time].sort(lambda x, y: x["priority"] - y["priority"]  )
    else:
      self.schedule[time] = [ task ]
      self.times.append(time)
      self.times.sort()

#-------------------------------------------------------------------------------

  def containsTask(self, name):
    return self.tasks.has_key(name)

#-------------------------------------------------------------------------------

  def addTask(self, name, function, period = None, priority = 0):
    ''' Adds a periodic task to the scheduler.
    The name for the task should be unique. If 'period == 0' then the value
    returned by 'function' will be used to reschedule the task.
    If 'period' is not given then the task will be executed once per rendering
    cycle.
    '''
    if self.tasks.has_key(name):
      return False
    else:
      self.tasks[name]     = {
        "name"      : name,
        "function"  : function,
        "period"    : period,
        "priority"  : priority
      }
      if period != None:
        self.scheduleTask(self.time() + period, self.tasks[name])
      else:
        self.renderTasks.append(self.tasks[name])
        self.renderTasks.sort(lambda x, y: x["priority"] - y ["priority"])

#-------------------------------------------------------------------------------

  def removeTask(self, name):
    task = self.tasks[name]
    del self.tasks[name]
    if task in self.renderTasks:
      self.renderTasks.remove(task)
  