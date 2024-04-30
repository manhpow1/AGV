from model.Event import Event
from model.AGV import AGV
from model.Graph import Graph

class RestrictionEvent(Event):
    def __init__(self, startTime, endTime, agv, graph, start_node, end_node):
        super().__init__(startTime, endTime, agv, graph)
        self.start_node = start_node
        self.end_node = end_node

    def updateGraph(self):
        # Giả định thời gian di chuyển thực tế khác với dự đoán do các ràng buộc đặc biệt
        actual_time = self.endTime - self.startTime
        predicted_time = Graph.get_edge(self.start_node, self.end_node).weight

        if actual_time != predicted_time:
            # Cập nhật trọng số của cung trên đồ thị để phản ánh thời gian thực tế
            Graph.update_edge(self.start_node, self.end_node, actual_time)

            # Đánh dấu AGV cuối cùng thay đổi đồ thị
            Graph.lastChangedByAGV = AGV.id

    def calculateCost(self):
        # Chi phí của AGV sẽ được tăng thêm một lượng bằng trọng số của cung mà AGV đi trên đồ thị TSG
        edge = Graph.get_edge(self.start_node, self.end_node)
        if edge:
            cost_increase = edge.weight
            AGV.cost += cost_increase
            print(
                f"Cost increased by {cost_increase} for AGV {AGV.id} due to RestrictionEvent from {self.start_node} to {self.end_node}"
            )
        else:
            print("No edge found or incorrect edge weight.")

    def process(self):
        # Xử lý khi sự kiện được gọi
        print(
            f"AGV {AGV.id} moves from {self.start_node} to {self.end_node} under restrictions, taking {self.endTime - self.startTime} seconds"
        )
        self.updateGraph(self.graph)
        self.calculateCost()