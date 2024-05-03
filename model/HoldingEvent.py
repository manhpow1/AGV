from .Event import Event
from model.utility import get_largest_id_from_map
from discrevpy import simulator
class HoldingEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, duration):
        super().__init__(startTime, endTime, agv, graph)
        self.duration = duration
        self.largest_id = get_largest_id_from_map("map.txt")
        self.type = 'HoldingEvent'

    def updateGraph(self):
        current_node = self.agv.current_node
        next_node = current_node + (self.duration * self.largest_id) + 1

        # Prepare properties as a dictionary
        properties = {'next_node': next_node}  # Assuming 'next_node' is a property you want to set

        # Check if this node exists in the graph and update accordingly
        if next_node in self.graph.nodes:
            self.graph.update_node(current_node, properties)
        else:
            print("Calculated next node does not exist in the graph.")
        # Update the AGV's current node to the new node
        self.agv.current_node = next_node

    def process(self):
        added_cost = self.calculateCost()
        print(f"Processed HoldingEvent for AGV {self.agv.id}, added cost: {added_cost}, at node {self.agv.current_node}")

        # Decide next event based on AGV's traces or planned path
        next_node = self.agv.getNextNode()
        if next_node is None:
            print(f"AGV {self.agv.id} has no further nodes to move to.")
            return

        if next_node == self.agv.current_node:
            # If next node is the same, schedule another holding event
            print(f"AGV {self.agv.id} continues to hold at node {self.agv.current_node}.")
            self.schedule_next_holding()
        else:
            # Move to the next node and possibly switch to a MovingEvent
            print(f"AGV {self.agv.id} prepares to move from {self.agv.current_node} to {next_node}.")
            self.agv.move_to(next_node)  # Ensure this method updates the AGV's current node

    def schedule_next_holding(self):
        next_start_time = self.endTime
        next_end_time = self.endTime + self.duration
        new_holding_event = HoldingEvent(next_start_time, next_end_time, self.agv, self.graph, self.duration)
        simulator.schedule(next_start_time, new_holding_event.process)
        
    def calculateCost(self):
        cost_increase = self.endTime - self.startTime
        self.agv.cost += cost_increase  # Update the cost of the specific AGV instance
        return cost_increase

    def getNextNode(self):
        # This method directly calls the AGV's getNextNode to get the next target node
        return self.agv.getNextNode()