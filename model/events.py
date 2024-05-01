from.utility import get_largest_id_from_map

class Event:
    def __init__(self, startTime, endTime, agv, graph):
        self.startTime = int(startTime)
        self.endTime = int(endTime)
        self.agv = agv
        self.graph = graph
        self.type = 'GenericEvent'
        
class HoldingEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, duration):
        super().__init__(startTime, endTime, agv, graph)
        self.duration = duration
        self.largest_id = get_largest_id_from_map("map.txt")
        self.type = 'HoldingEvent'

class MovingEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, start_node, end_node):
        super().__init__(startTime, endTime, agv, graph)
        self.start_node = start_node
        self.end_node = end_node
        self.type = 'MovingEvent'

class ReachingTarget(Event):
    def __init__(self, startTime, endTime, agv, graph, target_node):
        super().__init__(startTime, endTime, agv, graph)
        self.target_node = target_node
        self.type = 'ReachingTarget'
        
class RestrictionEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, start_node, end_node):
        super().__init__(startTime, endTime, agv, graph)
        self.start_node = start_node
        self.end_node = end_node
        
class StartEvent(Event):
    def __init__(self, startTime, endTime, agv, graph):
        super().__init__(startTime, endTime, agv, graph)
        print(f"StartEvent initialized for AGV {agv.id} at node {agv.current_node} with start time {startTime}.")
        
class TimeWindowsEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, target_node):
        super().__init__(startTime, endTime, agv, graph)
        self.target_node = target_node  # Mục tiêu mà AGV phải đạt đến trong một khoảng thời gian nhất định
