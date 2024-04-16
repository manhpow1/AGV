import time

class AGV:
    def __init__(self, id, current_node):
        self.id = id
        self.current_node = current_node
        self.state = 'waiting'  # Default state
        self.cost = 0

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
            
    def run_pns(input_file):
    # Path to the pns-seq executable and the input file
        cmd = ["wsl", "/mnt/d/MinGW64/lab2/pns/pns-seq", f"/mnt/d/python/simulation/TSG.txt"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print("Error running pns-seq:")
            print(result.stderr)
            return None

    def process_event(agv, event_info, t):
        if event_info['type'] == 'move':
            agv.move_to(event_info['new_position'], event_info['travel_time'])
        elif event_info['type'] == 'wait':
            agv.wait(event_info['wait_time'])
        # Possible re-evaluation of path after each move or wait
        new_path = run_pns("new_TSG.txt")
        print(f"New path at t={t}: {new_path}")

    # Example Usage:
    agv = AGV(position=2)
    events = [
        {'type': 'wait', 'wait_time': 10},
        {'type': 'move', 'new_position': 3, 'travel_time': 15},
        {'type': 'wait', 'wait_time': 10}
    ]

    current_time = 0
    for event in events:
        process_event(agv, event, current_time)
        current_time += event.get('wait_time', 0) + event.get('travel_time', 0)