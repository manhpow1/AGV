# -*- coding: utf-8 -*-
from model.Graph import Graph
from model.AGV import AGV
from model.Event import MovingEvent, HoldingEvent, Event
from discrevpy import simulator

def getReal():
    return 15

def getForecast():
    
    return 17

AGV = set()
TASKS = set()

x = {}
y = {}

graph = Graph()  # Assuming a Graph class has appropriate methods to handle updates

# Mở file để đọc
with open('TSG_0.txt', 'r') as f:
	# Đọc từng dòng của file
	for line in f:
    	# Phân tích dòng thành các phần tử, phân tách bởi khoảng trắng
            parts = line.split()
    	# Kiểm tra loại dữ liệu của dòng
            if parts[0] == 'n':  # Nếu là dòng chứa thông tin về AGV hoặc công việc
                if int(parts[2]) == 1:
                    AGV.add(parts[1])  # Thêm vào tập hợp AGV
                elif int(parts[2]) == -1:
                    TASKS.add(parts[1])  # Thêm vào tập hợp TASKS
            elif parts[0] == 'a':  # Nếu là dòng chứa thông tin về mối quan hệ
                    i, j, c_i_j = int(parts[1]), int(parts[2]), int(parts[5])
                    x[i, j] = c_i_j  # Lưu thông tin về mối quan hệ vào từ điển x
            graph.insertEdgesAndNodes(i, j, c_i_j)
        
def parse_tsg_file(filename):
    OriginalEvents = []

    event_type_mapping = {'M': MovingEvent, 'H': HoldingEvent}  # Example mapping
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts[0] == 'n' and int(parts[2]) == 1:
                node_id = int(parts[1])
                time_event = node_id  # Assuming node ID encodes the time
                event_type = parts[2] if len(parts) > 2 else 'H'  # Default to 'H' if not specified
                agv_id = "AGV" + parts[1]  # Constructing AGV ID for uniqueness
                event_class = event_type_mapping.get(event_type, HoldingEvent)  # Default to HoldingEvent
                if event_type == 'M':
                    # Assuming defaults for start_node and end_node if not specified
                    event = event_class(time=time_event, agv=agv_id, graph=graph, start_node=node_id, end_node=node_id+1)
                else:
                    event = event_class(time=time_event, agv=agv_id, graph=graph, duration=10)
                OriginalEvents.append(event)
    return sorted(OriginalEvents, key=lambda x: x.time)

def schedule_events(events):
    for event in events:
        simulator.schedule(event.time, event.process)

# Main execution
if __name__ == "__main__":
    simulator.ready()
    events = parse_tsg_file('TSG_0.txt')
    schedule_events(events)
    simulator.run()
