import os
import json

class utility:
    def __init__(self):
        x = {}
        max_value = 0
        with open('map.txt', 'r') as f:
            for line in f:
                parts = line.split()
                if parts[0] == 'a':
                    max_value = max(max_value, int(parts[1]), int(parts[2]))
                    i, j, c_i_j = int(parts[1]), int(parts[2]), int(parts[5])
                    x[i,j] = c_i_j
        self.matrix = x
        self.M = max_value
        self.H = 3600

    def getid(self,pos):
        if pos % self.M != 0:
            return pos%23 
        else: 
            return self.M
    
    def findid(self, pos):
        my_list = set()  # Tạo một set mới
        i = self.getid(pos)
        for j in range(1, 24):
            if (i,j) in self.matrix:
                id1 = self.M * (int(pos / self.M) + self.matrix[i, j]) + j
                id2 = self.M * 10 + pos 
                my_list.add(id1)
                my_list.add(id2)
        return my_list
    
def get_largest_id_from_map(filename):
    largest_id = 0
    with open('map.txt', 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'a':  # Assuming arcs start with 'a'
                id1, id2 = int(parts[1]), int(parts[2])
                largest_id = max(largest_id, id1, id2)
    return largest_id

def get_pns_seq_path():
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config.get('pns_seq_path', '')
    return ''

def save_pns_seq_path(path):
    config = {"pns_seq_path": path}
    try:
        with open("config.json", "w") as file:
            json.dump(config, file)
        print("The path to pns-seq.exe has been saved successfully.")
    except IOError as e:
        print(f"Failed to save the path: {e}")
        
def getDuration(file_path, largest_id):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return None
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('a'):
                parts = line.split()
                id1 = int(parts[1])
                id2 = int(parts[2])
                cost = int(parts[5])

                # Calculate the expected ID2 based on the formula
                expected_id2 = id1 + largest_id * cost

                # Check if the calculated ID2 matches the actual ID2
                if id2 == expected_id2:
                    return cost  # Return the cost if the condition is satisfied

    return None  # Return None if no matching condition is found

def getReal():
    return 15

def getForecast(file_path, largest_id):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return None
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('a'):
                parts = line.split()
                id1 = int(parts[1])
                id2 = int(parts[2])
                cost = int(parts[5])

                # Calculate the expected ID2 based on the adjusted formula
                expected_id2 = id1 + largest_id * cost + 1

                # Check if the calculated ID2 matches the actual ID2
                if id2 == expected_id2:
                    return cost  # Return the cost if the condition is satisfied

    return None  # Return None if no matching condition is found