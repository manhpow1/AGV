from model.utility import utility
from model.Graph import Graph
from connect import run_command,extract_time_values,wsl_command
class Event:
    def __init__(self,currentpos,x):
        self.pos = currentpos
        self.x = x
        self.time = 0
    def getwait(self,waittime):
        obj = utility()
        graph = Graph(self.x)
        self.pos =  self.pos + waittime*obj.M
        self.time = self.time + waittime
        graph.writefile(self.pos,1)

    def getreal(self,currentpos,nextpos,realtime):
        obj = utility()
        graph = Graph(self.x)
        nextpos = obj.M*(int(self.pos/obj.M)+obj.matrix[currentpos,nextpos]) + obj.getid(nextpos)
        graph.update(self.pos,nextpos,realtime)
        self.x  = graph.matrix
        self.time = self.time+realtime
        self.pos = obj.M*(int(self.pos/obj.M)+realtime) + obj.getid(nextpos)
        graph.writefile(self.pos,1)

    def getforecast(self,nextpos,forecastime):
        obj = utility()
        self.pos = obj.M*(int(self.pos/obj.M)+forecastime) + obj.getid(nextpos)
        self.time = self.time + forecastime
        graph = Graph(self.x)
        graph.writefile(self.pos,1)
        
class ReachingTarget(Event):
    pass

class HoldingEvent(Event):
    pass

class MovingEvent(Event):
    pass