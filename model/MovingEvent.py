from .Event import Event
from model.AGV import AGV

class MovingEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, start_node, end_node):
        super().__init__(startTime, endTime, agv, graph)
        self.start_node = start_node
        self.end_node = end_node
        self.type = 'MovingEvent'

    def updateGraph(self):
        actual_time = self.endTime - self.startTime
        edge = self.graph.get_edge(self.start_node, self.end_node)  # This now returns an Edge object
        predicted_time = edge.weight if edge else None

        if actual_time != predicted_time:
            self.graph.update_edge(self.start_node, self.end_node, actual_time, self.agv)
            self.graph.handle_edge_modifications(self.start_node, self.end_node, self.agv)

    def calculateCost(self):
        # Tính chi phí dựa trên thời gian di chuyển thực tế
        cost_increase = self.endTime - self.startTime
        AGV.cost += cost_increase  # Cập nhật chi phí của AGV
        return cost_increase

    def process(self):
        # Thực hiện cập nhật đồ thị khi xử lý sự kiện di chuyển
        self.updateGraph()
        print(
            f"AGV {self.agv.id} moves from {self.start_node} to {self.end_node} taking actual time {self.endTime - self.startTime}"
        )