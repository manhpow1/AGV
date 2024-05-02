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
        next_node = self.agv.getNextNode()  # Check next node but don't move yet

        if next_node == self.agv.current_node:
            # Continue holding if the next node is the same
            print(f"AGV {self.agv.id} continues to hold at node {self.agv.current_node}.")
            self.schedule_next_holding()
        elif next_node is not None:
            # Move if the next node is different
            self.agv.process_trace()  # Confirm and process the trace to actually move
            print(f"AGV {self.agv.id} moves from {self.agv.current_node} to {next_node}.")
            # Here, move to a moving event or process the movement
        else:
            print(f"No further moves possible for AGV {self.agv.id} from node {self.agv.current_node}")

    def schedule_next_holding(self):
        # Schedule next holding event if conditions still match
        next_start_time = self.endTime
        next_end_time = self.endTime + self.duration
        simulator.schedule(next_start_time, HoldingEvent(next_start_time, next_end_time, self.agv, self.graph, self.duration).process)
        
    def calculateCost(self):
        cost_increase = self.endTime - self.startTime
        self.agv.cost += cost_increase  # Update the cost of the specific AGV instance
        return cost_increase

    def getNextNode(self):
        # This method directly calls the AGV's getNextNode to get the next target node
        return self.agv.getNextNode()