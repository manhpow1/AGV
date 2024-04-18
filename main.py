# -*- coding: utf-8 -*-
from model.Graph import Graph
from model.AGV import AGV
from model.Event import MovingEvent, HoldingEvent
from discrevpy import simulator
from connect import run_command, extract_time_values, wsl_command

def getreal():
    return 15

def getforecast():
    
    return 17

AGV = set()
TASKS = set()

x = {}
y = {}

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
  
class OriginalEvent:
    def __init__(self, startTime, agvID, nodeID, action):
        self.startTime = startTime
        self.agvID = agvID
        self.nodeID = nodeID
        self.action = action  # This could be a method or function pointer

    def getNext(self):
        # Implement logic to decide the next step for the AGV based on current node or state
        print(f"Executing event for AGV {self.agvID} at Node {self.nodeID} at t={self.startTime}")
        # Placeholder for real action, e.g., moving to next node or processing a task
      
def parse_tsg_file(filename):
    original_events = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts[0] == 'n' and int(parts[2]) == 1:
                node_id = int(parts[1])
                time_event = node_id  # Assuming node ID encodes the time
                agv_id = "AGV" + parts[1]  # Constructing AGV ID for uniqueness
                # Create an event, here using HoldingEvent as a placeholder
                event = HoldingEvent(time=time_event, agv=agv_id, duration=10)
                original_events.append(event)
    return sorted(original_events, key=lambda x: x.time)

def schedule_events(events):
    for event in events:
        # Schedule each event based on its start time
        simulator.schedule(event.time, event.process)

# Main execution setup
if __name__ == "__main__":
    simulator.ready()
    events = parse_tsg_file('TSG_0.txt')
    schedule_events(events)
    simulator.run()
