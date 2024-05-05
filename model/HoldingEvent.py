from model.Event import Event
from model.utility import get_largest_id_from_map
from discrevpy import simulator
from .MovingEvent import MovingEvent

class HoldingEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, duration):
        super().__init__(startTime, endTime, agv, graph)
        self.duration = duration
        self.largest_id = get_largest_id_from_map("map.txt")
        self.type = 'HoldingEvent'

    def updateGraph(self, next_node):
        if next_node in self.graph.nodes:
            self.graph.update_node(self.agv.current_node, {'next_node': next_node})
            print(f"Graph updated for AGV {self.agv.id}, moving to node {next_node}.")
        else:
            print("Calculated next node does not exist in the graph.")

    def process(self):
        added_cost = self.calculateCost()
        print(f"Processed HoldingEvent for AGV {self.agv.id}, added cost: {added_cost}, at node {self.agv.current_node}")

        next_node, next_id = self.agv.getNextNode()  # Updated to get both node and ID
        if next_node is None:
            print(f"AGV {self.agv.id} has no further nodes to move to.")
            return

        if next_node == self.agv.current_node:
            if self.agv.current_id not in self.agv.visited_ids:  # Check based on ID now
                print(f"AGV {self.agv.id} continues to hold at node {self.agv.current_node}.")
                self.schedule_next_holding()
            else:
                print(f"AGV {self.agv.id} stays at node {self.agv.current_node} but already visited, no new holding scheduled.")
        else:
            print(f"AGV {self.agv.id} prepares to move from {self.agv.current_node} (ID {self.agv.current_id}) to {next_node} (ID {next_id}).")
            self.updateGraph(next_node)
            self.schedule_movement(next_node, next_id)

    def schedule_next_holding(self):
        next_start_time = self.endTime
        next_end_time = self.endTime + self.duration
        new_holding_event = HoldingEvent(next_start_time, next_end_time, self.agv, self.graph, self.duration)
        simulator.schedule(next_start_time, new_holding_event.process)

    def schedule_movement(self, next_node, next_id):
        move_time = self.endTime
        move_duration = self.graph.get_edge(self.agv.current_node, next_node).weight if self.graph.get_edge(self.agv.current_node, next_node) else 10
        new_moving_event = MovingEvent(move_time, move_time + move_duration, self.agv, self.graph, self.agv.current_node, self.agv.current_id, next_node, next_id)
        simulator.schedule(move_time, new_moving_event.process)

    def calculateCost(self):
        cost_increase = self.endTime - self.startTime
        self.agv.update_cost(cost_increase)
        return cost_increase
