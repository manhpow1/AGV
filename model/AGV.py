class AGV:
    def __init__(self, id, current_node, current_id, cost=0):
        self.id = id
        self.current_node = current_node
        self.previous_node = None
        self.state = 'idle'
        self.current_id = current_id
        self.cost = cost
        self.traces = []  # Tracks the upcoming nodes for the AGV to visit
        self.visited_ids = []  # List to store visited IDs from the TSG

    def add_trace(self, current_id, current_node, next_id, next_node):
        # Add full trace information
        self.traces.append((current_id, current_node, next_id, next_node))
        print(f"[DEBUG] Trace added to AGV {self.id}: from {current_id} at node {current_node} to {next_id} at node {next_node}")
        
    def update_cost(self, amount):
        self.cost += amount
        print(f"[DEBUG] Cost updated for AGV {self.id}: {self.cost}")

    def getNextNode(self):
        # Adjust to check based on IDs and nodes
        if self.traces:
            first_trace = self.traces[0]
            if first_trace[0] == self.current_id and first_trace[1] == self.current_node:
                return first_trace[2], first_trace[3]  # Return next_id and next_node
        return None, None  # If no valid trace or mismatch, return None
    
    def process_trace(self):
        # Confirm and move to the next node if it's consistent with the current position
        if self.traces:
            current_node, next_node = self.traces.pop(0)  # Pop the first trace
            if current_node == self.current_node:
                self.move_to(next_node)  # Move to the next node
                self.visited_ids.append(current_node)  # Log the visited node
                return next_node
            else:
                print(f"[ERROR] Trace mismatch for AGV {self.id}: expected {self.current_node}, found {current_node}")
        return None
    
    def confirmNodeVisit(self):
        # Remove the confirmed node from traces after processing
        if self.traces:
            visited_trace = self.traces.pop(0)
            self.visited_ids.append(visited_trace[0])  # Store the visited node ID
            print(f"AGV {self.id} confirmed visit to node {visited_trace[0]}.")

    def move_to(self, next_id, next_node):
        if next_node is not None:
            self.previous_node = self.current_node
            self.current_id = self.current_id  # Update ID when moving
            self.current_node = next_node
            print(f"AGV {self.id} moved from {self.previous_node} to {self.current_node} with ID {self.current_id} to {next_id}.")

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