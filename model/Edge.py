class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        
    def __repr__(self):
        return f"Edge({self.start_node}, {self.end_node}, weight={self.weight})"
class HoldingEdge(Edge):
    def __init__(self, start_node, end_node, weight, min_hold_time):
        super().__init__(start_node, end_node, weight)
        self.min_hold_time = min_hold_time  # Minimum time an AGV has to hold on this edge

    def __repr__(self):
        return f"HoldingEdge({self.start_node}, {self.end_node}, weight={self.weight}, hold_time={self.min_hold_time})"

class MovingEdge(Edge):
    pass

class ArtificialEdge(Edge):
    pass