class AGV:
    def __init__(self, id, current_node, cost=0):
        self.id = id
        self.current_node = current_node
        self.previous_node = None
        self.state = 'idle'
        self.cost = cost
        self.traces = []  # Tracks the upcoming nodes for the AGV to visit

    def update_cost(self, amount):
        self.cost += amount
        print(f"Cost updated for AGV {self.id}: {self.cost}.")

    def getNextNode(self):
        if self.traces:
            next_node = self.traces.pop(0)
            print(f"AGV {self.id} is moving to next node: {next_node} from current node: {self.current_node}.")
            return next_node
        else:
            print(f"AGV {self.id} has no more nodes in the trace. Remaining at node: {self.current_node}.")
            return None

    def move_to(self, next_node):
        if next_node is not None:
            self.previous_node = self.current_node
            self.current_node = next_node
            self.state = 'moving'
            print(f"AGV {self.id} moved from {self.previous_node} to {self.current_node}. State updated to 'idle'.")
            self.state = 'idle'
        else:
            print(f"AGV {self.id} has no further destinations to move to.")

    def wait(self, duration):
        print(f"AGV {self.id} is waiting at node {self.current_node} for {duration} seconds.")
        self.state = 'waiting'
        # Simulating the wait time (Here you could implement a real wait using sleep if it fits the use case)
        print(f"AGV {self.id} finished waiting at node {self.current_node}. State updated to 'idle'.")
        self.state = 'idle'

    def add_trace(self, node):
        self.traces.append(node)
        print(f"Node {node} added to AGV {self.id}'s trace. Current trace path: {self.traces}")

    def print_status(self):
        """ Utility method to print current status of the AGV """
        print(f"AGV {self.id}: Current Node: {self.current_node}, Previous Node: {self.previous_node}, State: {self.state}, Cost: {self.cost}, Upcoming Path: {self.traces}")