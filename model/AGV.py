from model.utility import get_largest_id_from_map
class AGV:
    def __init__(self, id, current_node, cost=0):
        self.id = id
        self.current_node = current_node
        self.previous_node = None
        self.state = 'idle'
        self.cost = cost
        self.path = []
        
    def update_cost(self, amount):
        self.cost += amount
        print(f"Cost updated for AGV {self.id}: {self.cost}.")

    def getNextNode(self):
        # Assumes that the current node and the graph are correctly assigned and managed
        index = self.path.index(self.current_node)
        if index < len(self.path) - 1:
            next_node = self.path[index+1]
            return next_node
        return None  # Return None if no edges are available
    
    def move_to(self, graph, target_node):
        edge = graph.get_edge(self.current_node, target_node)
        if edge:
            self.previous_node = self.current_node  # Update previous node before moving
            self.current_node = target_node
            self.state = 'moving'
            print(f"AGV {self.id} moved from {self.previous_node} to {self.current_node}.")
            self.state = 'idle'
        else:
            print(f"No valid path from {self.current_node} to {target_node}.")

    def wait(self, duration):
        print(f"AGV {self.id} is waiting at node {self.current_node} for {duration} seconds.")
        self.state = 'waiting'
        # Simulate waiting
        self.state = 'idle'
        print(f"AGV {self.id} finished waiting at node {self.current_node}.")