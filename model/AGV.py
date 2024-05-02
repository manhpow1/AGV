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
        # Add a tuple (current_node, next_node) to the traces list
        self.traces.append((current_node, next_node))
        print(f"[DEBUG] Trace added to AGV {self.id}: from {current_node} to {next_node}")
        
    def update_cost(self, amount):
        self.cost += amount
        print(f"[DEBUG] Cost updated for AGV {self.id}: {self.cost}")

    def getNextNode(self):
        if self.traces:
            # Check the next node in the trace list without removing it
            current_node, next_node = self.traces[0]
            if current_node == self.current_node:
                return next_node
            else:
                print(f"[ERROR] Trace mismatch for AGV {self.id}: expected {self.current_node}, found {current_node}")
        return None
    
    def process_trace(self):
        # Remove the trace when confirmed and return the next node
        if self.traces and self.getNextNode() is not None:
            self.traces.pop(0)  # Remove the first element
            return self.getNextNode()
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
        
    def __str__(self):
        return f"AGV {self.id}: Current Node {self.current_node}, Cost {self.cost}, Traces {self.traces}"