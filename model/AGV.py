class AGV:
    def __init__(self, id, current_node):
        self.id = id
        self.current_node = current_node
        self.state = 'idle'  # Default state

    def move_to(self, target_node):
        # Logic to move to another node
        pass

    def wait(self, time):
        # Logic to simulate waiting
        pass