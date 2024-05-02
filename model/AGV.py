class AGV:
    def __init__(self, id, current_node, cost=0):
        self.id = id
        self.current_node = current_node
        self.previous_node = None
        self.state = 'idle'
        self.cost = cost
        self.traces = []  # Tracks the upcoming nodes for the AGV to visit
        self.visited_ids = []  # List to store visited IDs from the TSG

    def add_trace(self, current_node, next_node):
        # Adding the trace as a tuple to maintain the relationship between nodes
        self.traces.append((current_node, next_node))
        self.current_node = next_node  # Optionally update current node
        
    def update_cost(self, amount):
        self.cost += amount
        print(f"Cost updated for AGV {self.id}: {self.cost}.")

    def getNextNode(self):
        if self.traces:
            next_trace = self.traces[0]  # Peek at the first trace without removing it
            current_node, next_node = next_trace
            if current_node == self.current_node:  # Verify that it matches the AGV's current state
                return next_node
            else:
                print(f"Trace mismatch: Expected current node {current_node}, but AGV is at {self.current_node}")
        return None
    
    def process_trace(self):
        if self.traces and self.getNextNode() is not None:
            _, next_node = self.traces.pop(0)  # Pop the first trace when processing
            return next_node
        return None
    
    def confirmNodeVisit(self):
        # Remove the confirmed node from traces after processing
        if self.traces:
            visited_trace = self.traces.pop(0)
            self.visited_ids.append(visited_trace[0])  # Store the visited node ID
            print(f"AGV {self.id} confirmed visit to node {visited_trace[0]}.")

    def move_to(self, next_node):
        if next_node is not None:
            self.previous_node = self.current_node
            self.current_node = next_node
            print(f"AGV {self.id} moved from {self.previous_node} to {self.current_node}.")
            self.confirmNodeVisit()  # Confirm the node visit after moving

    def wait(self, duration):
        print(f"AGV {self.id} is waiting at node {self.current_node} for {duration} seconds.")
        self.state = 'waiting'
        self.confirmNodeVisit()  # Confirm the node visit after waiting
        print(f"AGV {self.id} finished waiting at node {self.current_node}. State updated to 'idle'.")
        self.state = 'idle'

    def print_status(self):
        """ Utility method to print current status of the AGV """
        print(f"AGV {self.id}: Current Node: {self.current_node}, Previous Node: {self.previous_node}, State: {self.state}, Cost: {self.cost}, Upcoming Path: {self.traces}, Visited IDs: {self.visited_ids}")