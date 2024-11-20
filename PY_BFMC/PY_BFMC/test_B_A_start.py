import matplotlib.pyplot as plt
import math
import cv2
from heapq import heappop, heappush
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
# Tọa độ các node
# Đọc nodes và edges từ file .sav
with open("graph_data.sav", "rb") as file:
    data = pickle.load(file)

nodes = data["nodes"]
edges = data["edges"]

# Tính chi phí của một đường nối dựa trên các điểm gãy
def calculate_cost(points):
    cost = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        cost += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return cost

# Tạo bản đồ chi phí
cost_map = {}
for (start, end), points in edges.items():
    cost = calculate_cost(points)
    cost_map[(start, end)] = cost
    cost_map[(end, start)] = cost  # Đường 2 chiều

# Tìm đường đi ngắn nhất bằng thuật toán A*
def a_star(start, goal, nodes, cost_map):
    # Hàm heuristic: tính khoảng cách Euclidean
    def heuristic(n1, n2):
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            break

        for neighbor in nodes:
            if (current, neighbor) in cost_map:
                new_cost = cost_so_far[current] + cost_map[(current, neighbor)]
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

    # Truy vết lại đường đi
    path = []
    current = goal
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# Vẽ đồ thị và đường đi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def draw_graph_with_map(nodes, edges, path=None, map_image_path="image.png"):
    # Đọc hình ảnh bản đồ
    image_path = "Track2025_2.png"
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    # Lấy tỷ lệ thực tế của hình ảnh (dựa trên chiều rộng và chiều cao gốc)
    # Hiển thị hình ảnh bản đồ làm nền với đúng tỷ lệ
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(image)

    # Vẽ các node
    for node, (x, y) in nodes.items():
        plt.scatter(x, y, color='blue')  # Node màu xanh
        plt.text(x + 20, y + 20, f"{node}", fontsize=9, color="white")  # Hiển thị tên node

    # Vẽ các đường nối
    for (start, end), points in edges.items():
        x, y = zip(*points)
        plt.plot(x, y, color='orange')  # Edge màu cam

    # Vẽ đường đi tìm được
    if path:
        path_points = []
        for i in range(len(path) - 1):
            if (path[i], path[i+1]) in edges:
                path_points += edges[(path[i], path[i+1])]
            elif (path[i+1], path[i]) in edges:
                path_points += edges[(path[i+1], path[i])]
            else:
                path_points += [nodes[path[i]], nodes[path[i+1]]]
        
        px, py = zip(*path_points)
        plt.plot(px, py, color='white', linewidth=3, label="Found Path")  # Đường đi màu đỏ



    # Hiển thị đồ thị
    plt.show()


# Nhập điểm bắt đầu và kết thúc từ người dùng
def main():
    print("Các node có sẵn:", list(nodes.keys()))
    start = input("Nhập điểm bắt đầu: ").strip()
    goal = input("Nhập điểm kết thúc: ").strip()

    if start not in nodes or goal not in nodes:
        print("Lỗi: Điểm bắt đầu hoặc kết thúc không tồn tại.")
        return

    # Tìm đường đi từ start đến goal
    path = a_star(start, goal, nodes, cost_map)
    print("Đường đi tìm được:", " -> ".join(path))

    # Vẽ đồ thị và đường đi với bản đồ nền
    draw_graph_with_map(nodes, edges, path, map_image_path="Track2025_2.png")


# Chạy chương trình
if __name__ == "__main__":
    main()
