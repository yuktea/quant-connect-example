# region imports
from AlgorithmImports import *
from collections import deque

# endregion

class DefineSimpleMovingAverage(PythonIndicator):
    
    def __init__(self, name, period):
        self.Name = name
        self.Time = datetime.min
        self.Value = 0
        self.queue = deque(maxlen=period)

    def Update(self, input):
        self.queue.appendleft(input.Close)
        self.Time = input.EndTime
        count = len(self.queue)
        self.Value = sum(self.queue) / count
        
        return (count == self.queue.maxlen)