# -*- coding: utf-8 -*-
from model.Graph import Graph
from model.AGV import AGV
from model.Event import Event
from discrevpy import simulator
from connect import run_command,extract_time_values,wsl_command

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
  

# Example command to run in WSL 2

# Run command in WSL 2
# Example usage:

event = Event(2,x)
#event.getwait(10)
#print(event.pos)
#event.getreal(2,3,15)
#print(event.pos)
#event.getwait(10)
#print(event.pos)
simulator.ready()
simulator.schedule(0, event.getwait,10)
simulator.schedule(10,event.getreal,2,3,getreal())
simulator.schedule(10,event.getwait,10)
simulator.run()