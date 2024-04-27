from model.Graph import graph
from model.AGV import AGV
from model.Event import StartEvent, getDuration,getForecast, Event
from discrevpy import simulator
from model.utility import get_largest_id_from_map, get_pns_seq_path, save_pns_seq_path

AGVS = set()
TASKS = set()
x = {}
y = {}

largest_id = get_largest_id_from_map("map.txt")
print(f"[DEBUG] Largest ID retrieved from map.txt: {largest_id}")
duration = getDuration('TSG_0.txt', largest_id)
forecast = getForecast('TSG_0.txt', largest_id)
print(f"[DEBUG] Duration calculated from TSG_0.txt: {duration}")
print(f"[DEBUG] Forecast calculated from TSG_0.txt: {forecast}")

def initialize_graph_from_file(file_path):
    print(f"[DEBUG] Initializing graph from file: {file_path}")
    graph.build_path_tree(file_path)
    unique_start_nodes = graph.find_unique_nodes(file_path)
    print(f"[DEBUG] Graph initialization complete: Unique start nodes found: {unique_start_nodes}")

def parse_tsg_file(filename, largest_id):
    print(f"[DEBUG] Parsing TSG file: {filename}")
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
                    print(f"[DEBUG] StartEvent created for AGV {agv_id} at node {node_id} with startTime {startTime}")
            elif parts[0] == 'a':
                i, j, c_i_j = int(parts[1]), int(parts[2]), int(parts[5])
                graph.insertEdgesAndNodes(i, j, c_i_j)
    return sorted(original_events, key=lambda event: event.startTime)

def schedule_events(events):
    print(f"[DEBUG] Scheduling events for simulator")
    for event in events:
        simulator.schedule(event.startTime, event.process)
        print(f"[DEBUG] Event scheduled: {event}")

def setup_simulation(filename, traces_file):
    print(f"[DEBUG] Setup simulation with filename: {filename} and traces file: {traces_file}")
    if not Event.run_pns_sequence(filename):
        print("[ERROR] Failed to run pns-seq sequence. Simulation aborted.")
        return
    simulator.ready()
    initialize_graph_from_file(traces_file)
    events = parse_tsg_file(filename, largest_id)
    schedule_events(events)
    print(f"[DEBUG] Starting simulator")
    simulator.run()

def main():
    if not get_pns_seq_path():
        print("Path to pns-seq.exe is not set.")
        new_path = input("Please enter the full path to pns-seq.exe: ")
        save_pns_seq_path(new_path)
    else:
        print("Path to pns-seq.exe is already configured.")
        
    # Continue with setup and execution
    setup_simulation('TSG_0.txt', 'traces.txt')

# Main execution
if __name__ == "__main__":
    main()