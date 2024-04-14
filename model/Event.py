from model.utility import utility
from model.Graph import Graph
from connect import run_command,extract_time_values,wsl_command
class Event:
    def __init__(self,currentpos,x):
        self.pos = currentpos
        self.x = x
        self.time = 0
        
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
        
class ReachingTarget(Event):
    def __init__(self, time, agv, target_node):
        super().__init__(time, agv, "ReachingTarget")
        self.target_node = target_node

    def __repr__(self):
        return f"ReachingTarget(time={self.time}, agv={self.agv.id}, target_node={self.target_node.id})"
    
    def handle_reaching_target(self, event):
    # Update AGV state and position
        event.agv.current_node = event.target_node
        event.agv.state = 'idle'  # Assume the AGV goes idle after reaching the target

    # Log the event
        print(f"AGV {event.agv.id} has reached the target node {event.target_node.id} at time {event.time}")

    # Trigger next actions, such as scheduling a new task
        self.post_reach_actions(event.agv)

    def post_reach_actions(self, agv):
    # Determine the next task for the AGV
        next_node = self.find_next_task_for_agv(agv)  # You would implement this method
        if next_node:
            self.schedule_event(agv.current_time + 10, self.simulator.move_to, agv, next_node)  # Example scheduling
    pass

class HoldingEvent(Event):
    def __init__(self, time, agv, duration):
        super().__init__(time, agv, "HoldingEvent")
        self.duration = duration  # Duration for which the AGV must hold

    def __repr__(self):
        return f"HoldingEvent(time={self.time}, agv_id={self.agv.id}, duration={self.duration})"
    

class MovingEvent(Event):
    pass