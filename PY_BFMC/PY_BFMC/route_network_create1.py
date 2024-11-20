import cv2
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pickle
import os  # For checking file existence

crossroad_counter = 0

# Initialize graph
road_network = nx.Graph()  # Use nx.DiGraph() for directed roads

# Data structures
crossroads = []  # All crossroads
selected_nodes = []  # Nodes selected for route creation
edges = []
node_radius = 30  # Radius to detect nearby nodes for selection

# Mode tracking
mode = "select_nodes"  # Modes: 'select_nodes' or 'add_routes'

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_nearest_node(x, y):
    """Find the nearest node within a given radius, or return None."""
    for node in crossroads:
        if distance((x, y), node) <= node_radius:
            return node
    return None

def onclick(event):
    """Handle mouse clicks based on the current mode."""
    global mode
    global crossroad_counter

    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        if mode == "select_nodes":
            nearest_node = find_nearest_node(x, y)
            if nearest_node:
                print(f"Node is already added")
                ax.plot(nearest_node[0], nearest_node[1], 'yo')  # Highlight selected node
            else:
                crossroads.append((x, y))
                road_network.add_node((x, y))
                print(f"'{crossroad_counter}': ({x}, {y}),")
                crossroad_counter += 1
                ax.plot(x, y, 'go')  # Green dot for new node

                # Display the node number with white color
                ax.text(x + 5, y + 5, str(crossroad_counter), color='white', fontsize=12, ha='center', va='center')
                
            fig.canvas.draw()
        
        elif mode == "add_routes":
            nearest_node = find_nearest_node(x, y)
            if nearest_node:
                print(f"Selected node for route creation: {nearest_node}")
                selected_nodes.append(nearest_node)
                ax.plot(nearest_node[0], nearest_node[1], 'yo')  # Highlight selected node
                fig.canvas.draw()

                # If two nodes are selected, create a route
                if len(selected_nodes) == 2:
                    p1, p2 = selected_nodes
                    cost = distance(p1, p2)
                    edges.append((p1, p2))
                    road_network.add_edge(p1, p2, weight=cost)  # Add edge to the graph
                    print(f"Road added between: {p1} and {p2}")
                    
                    # Draw the road
                    x_vals, y_vals = zip(*[p1, p2])
                    ax.plot(x_vals, y_vals, 'r-')  # Red line for the road
                    fig.canvas.draw()
                    selected_nodes.clear()  # Clear selection for next route

def on_key(event):
    """Handle Enter key to switch modes."""
    global mode

    if event.key == "enter":
        if mode == "select_nodes":
            mode = "add_routes"
            print("Switched to route creation mode. Select two nodes to connect them.")
            ax.set_title("Route Creation Mode: Click two nodes to create a route.")
        elif mode == "add_routes":
            print("Already in route creation mode. Continue selecting nodes.")
        fig.canvas.draw()

# Load the map
image_path = "Track2025_2.png"  # Replace with the path to your map image
image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

# Check if the file exists and load the road network
if os.path.exists('road_network_1.sav'):
    road_network = pickle.load(open('road_network_1.sav', 'rb'))  # Load the existing network
    crossroads = list(road_network.nodes)  # Get nodes from the loaded graph
    print("Loaded existing road network.")
    crossroad_counter = len(crossroads)  # Set the counter based on loaded nodes
else:
    print("No existing road network found. Starting fresh.")

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(image)
ax.set_title("Node Selection Mode: Click to add/select nodes. Press Enter to switch modes.")

# Plot the existing nodes from the loaded network
for node in crossroads:
    ax.plot(node[0], node[1], 'go')  # Plot nodes as green dots
    ax.text(node[0] + 5, node[1] + 5, str(crossroad_counter), color='white', fontsize=12, ha='center', va='center')
    crossroad_counter += 1

# Connect mouse and keyboard events
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', on_key)

# Show the plot
plt.show()

# Print the road network
print("Crossroads (nodes):", crossroads)
print("Roads (edges):", edges)

# Visualize the network
nx.draw(road_network, with_labels=True, node_color='lightblue', font_weight='bold')
plt.show()

# Save the updated network to file
pickle.dump(road_network, open('road_network_1.sav', 'wb'))  



# Cho chat GPt chay doan nay cong len 1 
# '0': (206, 3495),
# '1': (472, 3242),
# '2': (992, 3228),
# '3': (1483, 3265),
# '4': (2002, 3306),
# '5': (2356, 3334),
# '6': (2889, 3026),
# '7': (3316, 2686),
# '8': (2825, 2374),
# '9': (2921, 1979),
# '10': (3165, 1528),
# '11': (2815, 1083),
# '12': (3091, 913),
# '13': (3367, 632),
# '14': (3045, 164),
# '15': (2632, 357),
# '16': (2094, 389),
# '17': (1649, 389),
# '18': (863, 384),
# '19': (188, 453),
# '20': (105, 1345),
# '21': (110, 2250),
# '22': (105, 2755),
# '23': (110, 3439),
# '24': (2650, 835),
# '25': (2347, 729),
# '26': (1768, 830),
# '27': (1263, 885),
# '28': (1162, 1377),
# '29': (1157, 2268),
# '30': (1157, 2929),
# '31': (904, 3150),
# '32': (358, 3141),
# '33': (188, 2971),
# '34': (197, 2700),
# '35': (468, 2553),
# '36': (629, 2966),
# '37': (973, 2548),
# '38': (914, 2456),
# '39': (399, 2475),
# '40': (201, 1813),
# '41': (440, 1639),
# '42': (996, 1643),
# '43': (1235, 1184),
# '44': (1525, 926),
# '45': (2016, 917),
# '46': (2338, 1014),
# '47': (2696, 926),
# '48': (2241, 1243),
# '49': (2191, 1634),
# '50': (2232, 1937),
# '51': (2351, 2534),
# '52': (2094, 2980),
# '53': (1414, 3054),
# '54': (2296, 1767),
# '55': (2374, 2176),
# '56': (2365, 2810),
# '57': (1433, 3159),
# '58': (1244, 2714),
# '59': (1244, 1813),
# '60': (909, 1556),
# '61': (385, 1560),
# '62': (192, 917),
# '63': (780, 490),
# '64': (1391, 476),
# '65': (2094, 481),
# '66': (2724, 403),
# '67': (3215, 361),
# '68': (3132, 812),
# '69': (716, 1836),
# '70': (629, 2126),
# '71': (2370, 3109),
# '72': (2590, 2732),
# '73': (2577, 2190),
# '74': (2453, 1680),
# '75': (2379, 1188),
# '76': (2191, 3136),
# '77': (2544, 2507),
# '78': (2402, 1928),