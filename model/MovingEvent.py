from .Event import Event

class MovingEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, start_node, end_node, start_id, end_id):
        super().__init__(startTime, endTime, agv, graph)
        self.start_node = start_node
        self.end_node = end_node
        self.start_id = start_id
        self.end_id = end_id
        self.type = 'MovingEvent'

    def updateGraph(self):
        actual_time = self.endTime - self.startTime
        edge = self.graph.get_edge(self.start_node, self.end_node)
        predicted_time = edge.weight if edge else None

        if actual_time != predicted_time:
            self.graph.update_edge(self.start_node, self.end_node, actual_time, self.agv)
            self.graph.handle_edge_modifications(self.start_node, self.end_node, self.agv)

    def calculateCost(self):
        # Calculate cost based on the actual movement time
        cost_increase = self.endTime - self.startTime
        self.agv.update_cost(cost_increase)  # Update the cost of the AGV instance, not the class
        return cost_increase

    def process(self):
        # Perform graph update when processing the movement event
        self.updateGraph()
        print(f"AGV {self.agv.id} moves from {self.start_node} (ID: {self.start_id}) to {self.end_node} (ID: {self.end_id}) taking actual time {self.endTime - self.startTime}")
        
        # Optionally, handle reaching the new node
        self.agv.current_node = self.end_node
        self.agv.current_id = self.end_id  # Update AGV's current ID to the new node's ID
        print(f"AGV {self.agv.id} is now at node {self.end_node} with ID {self.end_id}.")