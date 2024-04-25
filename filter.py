from model.utility import get_largest_id_from_map 

M = get_largest_id_from_map("map.txt")

# Open the file for reading
with open("seq-f.txt", "r") as file:
    # Read each line in the file
    for line in file:
        # Strip whitespace and split the line into elements
        parts = line.strip().split()
        if parts[0] == 'f' and int(parts[3]) == 1:
            
        # Check if the last element is '1'
            print(f"a {int(parts[1])} {int(parts[1])%M} {int(parts[2])} {int(parts[2])%M}")
