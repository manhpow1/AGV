from model.Graph import Graph
from model.AGV import AGV
from model.Event import StartEvent
from discrevpy import simulator

graph = Graph()

AGVS = set()
TASKS = set()

x = {}
y = {}

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
                    # Determine startTime based on node ID and largest ID from map.txt
                    startTime = node_id / largest_id  # This is a simplified assumption
                    agv_id = "AGV" + parts[1]
                    agv = AGV(agv_id, node_id)
                    e = StartEvent(startTime=startTime, endTime=startTime, agv=agv, graph=graph)
                    original_events.append(e)
            elif parts[0] == 'a':
                i, j, c_i_j = int(parts[1]), int(parts[2]), int(parts[5])
                graph.insertEdgesAndNodes(i, j, c_i_j)
    return sorted(original_events, key=lambda x: x.startTime)
def schedule_events(events):
    for e in events:
        simulator.schedule(e.startTime, e.process)
        
# Main execution
if __name__ == "__main__":
    simulator.ready()
    events = parse_tsg_file('TSG_0.txt')
    schedule_events(events)
    simulator.run()
