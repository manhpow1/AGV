from .utility import utility,get_pns_seq_path, getDuration, getReal
from .Graph import Graph
import subprocess
from discrevpy import simulator
from .events import MovingEvent, HoldingEvent, ReachingTarget

class Event:
    def __init__(self, startTime, endTime, agv, graph):
        self.startTime = int(startTime)
        self.endTime = int(endTime)
        self.agv = agv
        self.graph = graph
        self.type = 'GenericEvent'

    def process(self):
        edge = self.graph.get_edge(self.start_node, self.end_node)
        if edge is not None:
            print(f"Edge found from {self.start_node} to {self.end_node} with weight {edge}")
        else:
            print(f"No edge found from {self.start_node} to {self.end_node}")
    def __repr__(self):
        # Safely get the type attribute if it exists, else default to 'Unknown'
        event_type = getattr(self, 'type', 'UnknownEvent')
        return f"{event_type}(startTime={self.startTime}, endTime={self.endTime}, agv_id={self.agv.id})"

    def getWait(self, waittime):
        obj = utility()
        graph = Graph(self.x)
        self.pos = self.pos + waittime * obj.M
        self.time = self.time + waittime
        graph.writefile(self.pos, 1)

    def getReal(self, currentpos, nextpos, realtime):
        obj = utility()
        graph = Graph(self.x)
        nextpos = obj.M * (
            int(self.pos / obj.M) + obj.matrix[currentpos, nextpos]
        ) + obj.getid(nextpos)
        graph.update(self.pos, nextpos, realtime)
        self.x = graph.matrix
        self.time = self.time + realtime
        self.pos = obj.M * (int(self.pos / obj.M) + realtime) + obj.getid(nextpos)
        graph.writefile(self.pos, 1)

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

    def updateGraph(self):
        """
        # Assuming that `self.graph` is an instance of `Graph`
        edge = Graph.get_edge(self.start_node, self.end_node)
        if edge:
            # Proceed with your logic
            print("Edge found:", edge)
        else:
            print("No edge found between", self.start_node, "and", self.end_node)"""
        pass
    
    def saveGraph(self):
        # Lưu đồ thị vào file DIMACS và trả về tên file
        filename = "current_graph.dimacs"
        # Code để lưu đồ thị vào file
        return filename

    def calculateCost(self):
        # Increase cost by the actual time spent in holding
        cost_increase = self.endTime - self.startTime
        self.agv.cost += cost_increase
        return cost_increase

    def run_pns_sequence(input_file):
        pns_seq_path = get_pns_seq_path()
        if not pns_seq_path:
            print("Path to pns-seq.exe is not set. Please configure it first.")
            return None

        try:
            output_file = "seq-f.txt"
            command = f"'{pns_seq_path}' -f '{input_file}' > '{output_file}'"
            subprocess.run(command, shell=True, check=True)
            print(f"pns-seq executed successfully, output in {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Failed to run pns-seq: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return None

    def getTraces(self):
    # Đọc và xử lý file traces để lấy các đỉnh tiếp theo
        path = []
        with open('traces.txt', "r") as file:
            for line in file:
                parts = line.strip().split()
                if parts[0] == 'f':  # Filter lines that describe the path
                    from_node = int(parts[1])
                    to_node = int(parts[2])
                    # Add the start node to the path list if the path is empty or continue the path
                    if not path:
                        path.append(from_node)
                    path.append(to_node)
        return path