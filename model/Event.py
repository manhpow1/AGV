from model.utility import utility
from model.Graph import Graph
from connect import run_command,extract_time_values,wsl_command
import subprocess
class Event:
    def __init__(self, time, agv):
        self.time = int(time)  # Ensure time is always an integer
        self.agv = agv

    def process(self):
        print(f"Event at {self.time} for AGV {self.agv}")
    
    def __repr__(self):
        return f"Event(time={self.time}, agv={self.agv})"
    
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

def run_pns_command(input_file):
    """ Runs the PNS command and returns its output. """
    try:
        result = subprocess.run(["./pns-seq.exe", "-f", input_file], capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Failed to run PNS command:", e)
        return None
class ReachingTarget(Event):
    def __init__(self, time, agv, target_node):
        super().__init__(time, agv, "ReachingTarget")
        self.target_node = target_node

    def __repr__(self):
        return f"ReachingTarget(time={self.time}, agv={self.agv.id}, target_node={self.target_node.id})"
    
    def handle_reaching_target(self, event):
    # Update AGV state and position
        event.agv.current_node = event.target_node
        event.agv.state = 'waiting'  # Assume the AGV goes idle after reaching the target

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
        super().__init__(time, agv)
        self.duration = duration

    def process(self):
        self.agv.hold(self.duration)
        output = run_pns_command("AGV_0.txt")  # Assuming AGV_0.txt is prepared for each decision point
        print("PNS Command Output:", output)
        # You would parse the output here and decide what to do next
        # For example:
        if "continue" in output:
            self.agv.move_to(self.agv.current_node + 1)  # Example of deciding the next node based on output
    
class MovingEvent(Event):
    def __init__(self, time, agv, start_node, end_node):
        super().__init__(time, agv)
        self.start_node = start_node
        self.end_node = end_node

    def process(self):
        print(f"Moving AGV {self.agv} from {self.start_node} to {self.end_node} at {self.time}")
        # Actual moving logic here