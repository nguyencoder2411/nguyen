import cv2
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pickle

road_network = pickle.load(open('road_network.sav', 'rb'))
nx.draw(road_network, with_labels=True, node_color='lightblue', font_weight='bold')
plt.show()