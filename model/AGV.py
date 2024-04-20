import time

class AGV:
    def __init__(self, id, current_node, cost = 0):
        self.id = id
        self.current_node = current_node
        self.state = 'waiting'  # Default state
        self.cost = cost

    def move_to(self, graph, target_node):
        # Assuming the graph instance is passed to this method
        edge = graph.get_edge(self.current_node, target_node)
        if edge and edge.weight == 17:
            # Move is only made if the edge exists and the weight is exactly 17
            self.current_node = target_node
            self.state = 'moving'
            print(f"AGV {self.id} moved from {edge.start_node} to {edge.end_node}")
            # After move is complete, update state back to idle or any other necessary state
            self.state = 'idle'
        else:
            print(f"No valid move found from {self.current_node} to {target_node} with weight 17")

    def wait(self, graph, duration, target_node=None, required_weight=10):
        # Check if an edge with the required weight exists from the current node
        if target_node is not None:
            edges = graph.find_edge_by_weight(self.current_node, required_weight)
            valid_edges = [edge for edge in edges if edge.end_node == target_node and edge.weight == required_weight]

            if valid_edges:
                print(f"AGV {self.id} is waiting for {duration} seconds at node {self.current_node}")
                self.state = 'waiting'
                time.sleep(duration)  # Simulates waiting
                self.state = 'idle'
                print(f"AGV {self.id} finished waiting at node {self.current_node}")
            else:
                print(f"No valid edge found for waiting at node {self.current_node} with weight {required_weight}")
        else:
            print("No target node specified for waiting.")
            
    def updateCost(self, amount):
        self.cost += amount
