from model.utility import get_largest_id_from_map 
from collections import deque, defaultdict
t = 0
M = get_largest_id_from_map("map.txt")

def findpath(elements_only_in_id1,edge):
    path1 = []
    path2 = []
    Q = deque()
    Q.append(elements_only_in_id1)
    path1.append(elements_only_in_id1)
    path2.append(elements_only_in_id1%M)
    while Q:
        current_id = Q.popleft()
        for pair in edge:
            if pair[0] == current_id:
                Q.append(pair[1])
                path1.append(pair[1])
                path2.append(pair[1]%M)
    print(f"{path1} # {path2}")
    

# Open the file for reading
with open("traces.txt", "r") as file:
    # Read each line in the file
    id1 = []
    id3 = []
    edge = []
    for line in file:
        # Split the line into parts
        parts = line.strip().split()
        # Check if the first part is 'f'
        if parts[0] == 'a':
            # Convert the IDs to integers and append to lists
            id1.append(int(parts[1]))
            id3.append(int(parts[3]))
            edge.append((int(parts[1]), int(parts[3])))
    # Convert lists to sets
    id1_set = set(id1)
    id3_set = set(id3)

    # Find elements only in id1
    elements_only_in_id1 = id1_set.difference(id3_set)
    print("Các số nguyên mà không bao giờ xuất hiện ở ID3, chỉ xuất hiện ở ID1:")
    print(elements_only_in_id1)
    
    #print 2 ways
    print("In ra danh sách các con số nguyên tiếp nối nhau theo hai kiểu:")
    for element in elements_only_in_id1:
        findpath(element,edge)
    
    
