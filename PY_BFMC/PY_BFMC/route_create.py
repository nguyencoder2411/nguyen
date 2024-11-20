import cv2
import matplotlib.pyplot as plt
import matplotlib
import pickle
import networkx as nx  # Import networkx if using NetworkX graph

# Sử dụng Qt5 để mở cửa sổ riêng
matplotlib.use('Qt5Agg')

# Function to handle mouse clicks
def onclick(event):
    global current_node, edge_in_progress
    # Check if the click is inside the image axes
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        
        # Check if we're in the mode to select node for edge creation
        if current_node is not None:
            # Add the node to the edge and draw it
            edge_in_progress.append((x, y))
            print(f"({x}, {y})")
            ax.plot(x, y, 'ro')  # Mark the point
            if len(edge_in_progress) > 1:
                # Draw a line between the last two points
                x_vals, y_vals = zip(*edge_in_progress)
                ax.plot(x_vals, y_vals, 'b-')  # Route in blue line
            fig.canvas.draw()
        else:
            # Check if clicked on a main node
            nearest_node = find_nearest_node(x, y)
            if nearest_node:
                current_node = nearest_node  # Set the current node as the starting point for edge creation
                edge_in_progress = [nearest_node]
                print(f"Start new edge from node: {nearest_node}")
                ax.plot(nearest_node[0], nearest_node[1], 'yo')  # Highlight main node in yellow
                fig.canvas.draw()

# Function to find the nearest node to a clicked position
def find_nearest_node(x, y):
    """Find the nearest node within a given radius, or return None."""
    for node in nodes:
        if distance((x, y), node) <= node_radius:
            return node
    return None

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# Function to save points to a .sav file using pickle
def save_to_sav(route_points, filename="route_points.sav"):
    with open(filename, 'wb') as file:
        pickle.dump(route_points, file)  # Save the list of points to a binary file
    print(f"Route points saved to {filename}")

# Function to load the road network data from a .sav file
def load_road_network(filename="route_points.sav"):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

# Load the image
image_path = "Track2025_2.png"  # Replace with the path to your image
image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

# Load the road network data (nodes and edges)
network_data = load_road_network("road_network_1.sav")

# Check the type of network_data
if isinstance(network_data, nx.Graph):
    # If network_data is a NetworkX graph, extract the nodes from the graph
    nodes = list(network_data.nodes)  # This returns a list of nodes
    print(f"Nodes in the network: {nodes}")  # Print the nodes to verify
else:
    # If the data isn't a NetworkX graph, try to access the nodes differently
    try:
        nodes = network_data["nodes"]
    except KeyError:
        print("Error: No 'nodes' key found in the data. Please check the structure of the .sav file.")
        exit()

# Initialize variables for edge creation
current_node = None
edge_in_progress = []
node_radius = 30  # Radius to detect nearby nodes for selection

# Display the image
fig, ax = plt.subplots(figsize=(16, 10))  # Adjust figsize as needed
ax.imshow(image)
ax.set_title("Click to create a route. Close the window to finish.")

# Plot the nodes on the image
for i, node in enumerate(nodes):
    x, y = node  # Unpack the tuple to get the x and y coordinates
    ax.plot(x, y, 'go')  # Plot nodes as green circles
    
    # Display the node number with white color (numbering starts from 1)
    ax.text(x + 5, y + 5, str(i + 1), color='white', fontsize=12, ha='center', va='center')

# Connect the mouse event
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# Show the plot
plt.show()

# Save the route points to a .sav file when the window is closed
save_to_sav(edge_in_progress)
