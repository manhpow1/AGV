from model.Graph import Graph
from model.AGV import AGV
from model.Event import StartEvent
from discrevpy import simulator

def getReal():
    return 15

def getForecast():
    return 17

graph = Graph()

AGVS = set()
TASKS = set()

x = {}
y = {}

# Read and parse the TSG_0.txt file
def parse_tsg_file(filename):
    original_events = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'n' and int(parts[2]) == 1:
                agv_id = parts[1]
                AGVS.add(agv_id)  # Assuming AGV is properly defined elsewhere
                e = StartEvent(startTime=0, endTime=0, agv=AGV(agv_id, int(parts[1])), graph=graph)
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
