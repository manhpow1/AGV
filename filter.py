from model.utility import get_largest_id_from_map

# Get the largest ID from the map file
M = get_largest_id_from_map("map.txt")

# Prepare a dictionary to hold the cost information from TSG_0.txt
cost_data = {}

# Read the TSG_0.txt file to populate the cost dictionary
with open("TSG_0.txt", "r") as tsg_file:
    for line in tsg_file:
        if line.startswith('a'):
            parts = line.strip().split()
            key = (int(parts[1]), int(parts[2]))  # Create a tuple key from parts 1 and 2
            cost_data[key] = parts[-1]  # Take the last element as cost

# Open the sequence file and process each line
with open("seq-f.txt", "r") as file:
    for line in file:
        parts = line.strip().split()
        if parts[0] == 'f' and int(parts[3]) == 1:
            # Get the cost associated with the tuple (parts[1], parts[2])
            cost = cost_data.get((int(parts[1]), int(parts[2])), '0')  # Default to '0' if not found
            print(f"a {int(parts[1])} {int(parts[1])%M} {int(parts[2])} {int(parts[2])%M} {cost}")
