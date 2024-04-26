from model.Graph import graph
from model.AGV import AGV
from model.Event import StartEvent, getDuration, getReal, getForecast
from discrevpy import simulator
from model.utility import get_largest_id_from_map

AGVS = set()
TASKS = set()
x = {}
y = {}
 
largest_id = get_largest_id_from_map("map.txt")
duration = getDuration('TSG_0.txt', largest_id)
forecast = getForecast('TSG_0.txt', largest_id)

def initialize_graph_from_file(file_path):
    graph.build_path_tree(file_path)
    unique_start_nodes = graph.find_unique_nodes(file_path)
    print(f"[DEBUG] Graph initialization: Unique start nodes found: {unique_start_nodes}")

# Read and parse the TSG_0.txt file
def parse_tsg_file(filename, largest_id):
    original_events = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'n':
                node_id = int(parts[1])
                agv_flag = int(parts[2])
                if agv_flag == 1:
                    startTime = node_id / largest_id
                    agv_id = "AGV" + parts[1]
                    agv = AGV(agv_id, node_id)
                    event = StartEvent(startTime=startTime, endTime=startTime, agv=agv, graph=graph)
                    original_events.append(event)
            elif parts[0] == 'a':
                i, j, c_i_j = int(parts[1]), int(parts[2]), int(parts[5])
                graph.insertEdgesAndNodes(i, j, c_i_j)
    return sorted(original_events, key=lambda event: event.startTime)

def schedule_events(events):
    """Schedules events for processing by the simulator."""
    for event in events:
        simulator.schedule(event.startTime, event.process)

def setup_simulation(filename, traces_file):
    simulator.ready()
    initialize_graph_from_file(traces_file)
    events = parse_tsg_file(filename, largest_id)
    schedule_events(events)
    simulator.run()
     
# Main execution
if __name__ == "__main__":
    setup_simulation('TSG_0.txt', 'traces.txt')
