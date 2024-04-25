import os
from collections import deque, defaultdict
from .utility import utility

class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(list)
        self.enter_node = set()
        self.target_node = set()
        self.nodes = set()
        self.lastChangedByAGV = -1
        self.edges = {}
        
    def insertEdgesAndNodes(self, start, end, weight):
        self.adjacency_list[start].append((end, weight))
        self.nodes.update([start, end])

    def insertEnterAndTarget(self,node,flow):
        if flow > 0 :
            self.enter_node[node] = flow
        else:
            self.target_node[node] = flow

    def find_unique_nodes(self, file_path):
        """ Find nodes that are only listed as starting nodes in edges. """
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist.")
            return []
        
        target_ids = set()
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('a'):
                    parts = line.split()
                    target_ids.add(int(parts[3]))

        unique_ids = set()
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('a'):
                    parts = line.split()
                    node_id = int(parts[1])
                    if node_id not in target_ids:
                        unique_ids.add(node_id)

        return list(unique_ids)
    
    def build_path_tree(self, file_path):
        """ Build a tree from edges listed in a file for path finding. """
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('a'):
                    parts = line.split()
                    id1, id3 = int(parts[1]), int(parts[3])
                    id2, id4 = int(parts[2].strip('()')), int(parts[4].strip('()'))
                    self.insertEdgesAndNodes(id1, id3, id2)
                    self.insertEdgesAndNodes(id3, id1, id4)

    def dfs(self, start_node, visited=None):
        """ Depth First Search to explore paths from a given node. """
        if visited is None:
            visited = set()
        visited.add(start_node)
        paths = [start_node]
        for (neighbor, weight) in self.adjacency_list[start_node]:
            if neighbor not in visited:
                paths.extend(self.dfs(neighbor, visited))
        return paths
    
    def has_initial_movement(self, node):
        # Check if there are any outgoing edges from 'node'
        return node in self.edges and len(self.edges[node]) > 0
    
    def update(self,currentpos,nextpos,realtime):
        list = utility()
        del self.matrix[currentpos,nextpos]
        Q = deque()
        Q.append(nextpos)
        while Q:
            pos = Q[0]
            Q.pop()
            for i in list.findid(pos):
                if (pos,i) in self.matrix:
                    del self.matrix[pos,i]
                    Q.append(i)
        nextpos = list.M*(int(currentpos/list.M)+ realtime) + list.getid(nextpos)
        self.matrix[currentpos,nextpos] = realtime
        Q.append(nextpos)
        while Q:
            pos = Q[0]
            Q.pop()
            for i in list.findid(pos):
                if (pos,i) not in self.matrix:
                    self.matrix[pos,i] = int((pos-i)/list.M)
                    Q.append(i)      
              
    def add_node(self, node, properties=None):
        if properties is None:
            properties = {}
        self.nodes[node] = properties

    def update_node(self, node, **properties):
        if node in self.nodes:
            self.nodes[node].update(properties)
        else:
            self.nodes[node] = properties
            
    def add_edge(self, from_node, to_node):
        self.adjacency_list[from_node].append(to_node)
        self.nodes.update([from_node, to_node])

    def display_graph(self):
        for start_node in self.adjacency_list:
            print(f"{start_node} -> {self.adjacency_list[start_node]}")
            
    def get_edge(self, start_node, end_node):
        return self.adjacency_list.get(start_node, {}).get(end_node, None)
    
    def find_edge_by_weight(self, start_node, weight):
        # Find all edges from a node with a specific weight
        return [edge for edge in self.edges if edge.start_node == start_node and edge.weight == weight]
    
    def find_path(self, start_node, end_node):
        # Placeholder for a pathfinding algorithm like Dijkstra's
        queue = deque([start_node])
        visited = set()
        path = []
        
        while queue:
            node = queue.popleft()
            if node == end_node:
                break
            visited.add(node)
            for neighbor, weight in self.adjacency_list[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    path.append((node, neighbor, weight))
        return path
    
    def update_graph(self, currentpos, nextpos, realtime):
        # Update the graph with new edge information
        self.add_edge(currentpos, nextpos, realtime)
        
    def write_to_file(self, filename="TSG.txt"):
        with open(filename, "w") as file:
            file.write(f"p min {len(self.nodes)} {len(self.adjacency_list)}\n")
            for node in self.enter_node:
                file.write(f"n {node} {self.enter_node[node]}")
            for node in self.target_node:
                file.write(f"n {node} {self.target_node[node]}")
            for start_node in self.adjacency_list:
                for end_node, weight in self.adjacency_list[start_node]:
                    file.write(f"a {start_node} {end_node} 0 1 {weight}\n")
                    
    def update_edge(self, start_node, end_node, new_weight, agv):
        if start_node in self.adjacency_list and end_node in self.adjacency_list[start_node]:
            self.adjacency_list[start_node][end_node] = new_weight
            # Update the last AGV to change this edge
            self.lastChangedByAGV[(start_node, end_node)] = agv.id
            print(f"Edge weight from {start_node} to {end_node} updated to {new_weight} by AGV {agv.id}.")
        else:
            print("Edge does not exist to update.")

    def remove_node(self, node):
            if node in self.nodes:
                del self.nodes[node]
                self.edges.pop(node, None)
                for edges in self.edges.values():
                    edges[:] = [(n, w) for n, w in edges if n != node]

    def remove_edge(self, start_node, end_node, agv_id):
        if (start_node, end_node) in self.edges:
            del self.edges[(start_node, end_node)]
            self.lastChangedByAGV = agv_id  # Update the last modified by AGV

    def handle_edge_modifications(self, start_node, end_node, agv):
        # Example logic to adjust the weights of adjacent edges
        print(f"Handling modifications for edges connected to {start_node} and {end_node}.")
        # Check adjacent nodes and update as necessary
        for adj_node, weight in self.adjacency_list.get(end_node, {}).items():
            if (end_node, adj_node) not in self.lastChangedByAGV or self.lastChangedByAGV[(end_node, adj_node)] != agv.id:
                # For example, increase weight by 10% as a traffic delay simulation
                new_weight = int(weight * 1.1)
                self.adjacency_list[end_node][adj_node] = new_weight
                print(f"Updated weight of edge {end_node} to {adj_node} to {new_weight} due to changes at {start_node}.")
    
    def __str__(self):
        return "\n".join(f"{start} -> {end} (Weight: {edge.weight})" for (start, end), edge in self.edges.items())
    
graph = Graph()

def initialize_graph():
    # Function to populate the graph if needed
    return graph