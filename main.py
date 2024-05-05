import subprocess
from model.Graph import graph
from model.AGV import AGV
from model.Event import Event
from discrevpy import simulator
from model.utility import get_largest_id_from_map, get_pns_seq_path, save_pns_seq_path, getDuration, getForecast, getReal
from model.StartEvent import StartEvent
from model.HoldingEvent import HoldingEvent
from model.MovingEvent import MovingEvent
from model.ReachingTarget import ReachingTarget

AGVS = {}
TASKS = {}
x = {}
y = {}

largest_id = get_largest_id_from_map("map.txt")
print(f"[DEBUG] Largest ID retrieved from map.txt: {largest_id}")
duration = getDuration('TSG_0.txt', largest_id)
forecast = getForecast('TSG_0.txt', largest_id)
print(f"[DEBUG] Duration calculated from TSG_0.txt: {duration}")
print(f"[DEBUG] Forecast calculated from TSG_0.txt: {forecast}")

def getNext(self, graph, file_path, largest_id):
        if self.graph.lastChangedByAGV == self.agv:
            # Nếu đồ thị trước đó bị thay đổi bởi chính AGV này
            next_vertex = self.agv.getNextNode()  # Giả định phương thức này tồn tại
        else:
            # Nếu đồ thị bị thay đổi bởi AGV khác, cần tìm lại đường đi
            self.updateGraph(graph)
            filename = self.saveGraph(graph)
            lenh = f"./pns-seq -f {filename} > seq-f.txt"
            subprocess.run(lenh, shell=True)
            lenh = "py filter.py > traces.txt"
            subprocess.run(lenh, shell=True)
            self.agv.traces = self.getTraces("traces.txt")
            next_vertex = self.agv.getNextNode()
            
        real_duration = getReal()  # Retrieve the real duration from an external function
        hold_duration = getDuration(file_path, largest_id)
        # Xác định kiểu sự kiện tiếp theo
        if next_vertex == self.agv.current_node:
        # If the next vertex is the current one, initiate a holding event
            new_event = HoldingEvent(self.endTime, self.endTime + hold_duration, self.agv, graph, hold_duration)
        elif next_vertex == self.agv.target_node:
            # If the next vertex is the target node, initiate a reaching target event
            new_event = ReachingTarget(self.endTime, self.endTime + hold_duration, self.agv, graph, next_vertex)
        else:
            # Otherwise, initiate a moving event
            new_event = MovingEvent(self.endTime, self.endTime + real_duration, self.agv, graph, self.agv.current_node, next_vertex)
        # Schedule the new event
        simulator.schedule(new_event.startTime, new_event.process)
        
def load_traces_into_agvs():
    print("[DEBUG] Loading traces into AGVs")
    with open('traces.txt', 'r') as f:
        traces = f.readlines()

    for line in traces:
        if line.startswith('a'):
            parts = line.split()
            current_id = int(parts[1])
            current_node = int(parts[2])
            next_id = int(parts[3])
            next_node = int(parts[4])
            agv_id = f"AGV{current_id}"  # Assuming the AGV ID is somehow related or needs adjusting

            if agv_id in AGVS:
                AGVS[agv_id].add_trace(current_id, current_node, next_id, next_node)
            else:
                print(f"[DEBUG] No AGV found for ID {agv_id}")

    print(f"[DEBUG] Final AGV states after loading traces: {[(agv.id, agv.traces) for agv in AGVS.values()]}")

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
                if agv_flag == 1:  # This means the node is a starting point for an AGV
                    startTime = round(node_id / largest_id)  # Use rounding for startTime
                    agv_id = "AGV" + parts[1]
                    current_id = node_id  # Assuming current_id is the same as node_id if not specified otherwise
                    if agv_id not in AGVS:
                        agv = AGV(agv_id, node_id, current_id)  # Now providing current_id
                        AGVS[agv_id] = agv  # Add to AGVS set or dictionary
                        print(f"[DEBUG] AGV {agv_id} initialized at node {node_id} with ID {current_id}")
                    event = StartEvent(startTime=startTime, endTime=startTime, agv=AGVS[agv_id], graph=graph)
                    original_events.append(event)
                    print(f"[DEBUG] StartEvent created for AGV {agv_id} at node {node_id} with startTime {startTime}")
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
    load_traces_into_agvs()
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