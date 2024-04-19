from model.utility import utility
from model.Graph import Graph
from connect import run_command,extract_time_values,wsl_command
import subprocess
from discrevpy import simulator
class Event:
    def __init__(self, time, agv, graph):
        self.time = int(time)  # Ensure time is always an integer
        self.agv = agv
        self.graph = graph

    def process(self):
        print(f"Event at {self.time} for AGV {self.agv}")
        # To be overridden in subclasses
    
    def __repr__(self):
        return f"{self.type}(time={self.time}, agv_id={self.agv.id})"
 
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
        
    def getNext(self, graph):
        if graph.lastChangedByAGV == self.agv.id:
            next_node = self.agv.getNextNode()  # Assuming this method exists
        else:
            self.updateGraph(graph)
            filename = self.saveGraphToFile(graph)
            self.run_pns_sequence(filename)
            self.agv.traces = self.getTraces('traces.txt')
            next_node = self.agv.getNextNode()

        # Determine the type of the next event based on the next node and current node
        if next_node == self.agv.current_node:
            event = HoldingEvent(self.time + 10, self.agv, graph, duration=10)
        elif next_node is self.agv.target_node:
            event = ReachingTarget(self.time + 10, self.agv, graph, next_node)
        else:
            event = MovingEvent(self.time + 10, self.agv, graph, self.agv.current_node, next_node)

        # Schedule the next event
        simulator.schedule(event.time, event.process, event)

    def updateGraph(self, graph):
        # Implement logic to update graph
        pass

    def saveGraphToFile(self, graph):
        # Implement logic to save graph to a DIMACS file
        return "graph.dimacs"

    def run_pns_sequence(self, filename):
        command = f"./pns-seq -f {filename} > seq-f.txt"
        subprocess.run(command, shell=True)
        command = "python3 filter.py > traces.txt"
        subprocess.run(command, shell=True)

    def getTraces(self, filename):
        # Read and parse the Traces file to identify traces
        with open(filename, 'r') as file:
            return file.read().split()  # Simplified parsing logic

class HoldingEvent(Event):
    def __init__(self, time, agv, graph, duration):
        super().__init__(time, agv, graph)
        self.duration = duration

    def process(self):
        print(f"AGV {self.agv.id} holds at node {self.agv.current_node} for {self.duration} seconds")

class MovingEvent(Event):
    def __init__(self, time, agv, graph, start_node, end_node):
        super().__init__(time, agv, graph)
        self.start_node = start_node
        self.end_node = end_node

    def process(self):
        print(f"AGV {self.agv.id} moves from {self.start_node} to {self.end_node}")

class ReachingTarget(Event):
    def __init__(self, time, agv, graph, target_node):
        super().__init__(time, agv, graph)
        self.target_node = target_node

    def process(self):
        print(f"AGV {self.agv.id} reaches its target at node {self.target_node}")