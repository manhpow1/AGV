from .utility import get_largest_id_from_map, getDuration, getReal
from discrevpy import simulator
from .events import MovingEvent, HoldingEvent, Event

class StartEvent(Event):
    def __init__(self, startTime, endTime, agv, graph):
        super().__init__(startTime, endTime, agv, graph)
        print(f"StartEvent initialized for AGV {agv.id} at node {agv.current_node} with start time {startTime}.")

    def process(self, file_path=None, largest_id=None):
        if file_path is None or largest_id is None:
            file_path = 'TSG_0.txt'
            largest_id = get_largest_id_from_map(file_path)
        print(f"Processing StartEvent for AGV {self.agv.id} at time {self.startTime}. Checking initial movements from node {self.agv.current_node}.")
        self.determine_next_event(file_path, largest_id)

    def determine_next_event(self, file_path, largest_id):
        has_movement = self.graph.has_initial_movement(self.agv.current_node)
        print(f"Initial movement check for node {self.agv.current_node}: {'found' if has_movement else 'not found'}.")

        if has_movement:
            next_node = self.agv.current_node + 1  # Assuming the next node is simply the next sequential node
            movement_time = getReal()  # Get the real movement time from an external source or function
            print(f"Moving AGV {self.agv.id} from {self.agv.current_node} to {next_node} over {movement_time} seconds.")
            next_event = MovingEvent(
                startTime=self.endTime,
                endTime=self.endTime + movement_time,
                agv=self.agv,
                graph=self.graph,
                start_node=self.agv.current_node,
                end_node=next_node,
            )
        else:
            holding_time = getDuration(file_path, largest_id)
            print(f"No initial movement found. Holding AGV {self.agv.id} at node {self.agv.current_node} for {holding_time} seconds.")
            next_event = HoldingEvent(
                startTime=self.endTime,
                endTime=self.endTime + holding_time,
                agv=self.agv,
                graph=self.graph,
                duration=holding_time,
            )

        simulator.schedule(next_event.startTime, next_event.process)
        print(f"Scheduled {'Moving' if has_movement else 'Holding'} Event for AGV {self.agv.id} at time {next_event.startTime}.")