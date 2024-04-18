import tkinter as tk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import hypernetx as hnx
import ast
import warnings

warnings.simplefilter(action='ignore')

def algorithm(H):
    colors = {}
    vertices = list(H.nodes)
    degrees = {v: H.degree(v) for v in vertices}
    sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    print(sorted_degrees)
    for vertex, degree in sorted_degrees:
        if vertex not in colors:
            used_colors = set(colors[neighbor] for neighbor in H.neighbors(vertex) if neighbor in colors)
            available_colors = set(range(1, len(vertices) + 1)) - used_colors
            if available_colors:
                colors[vertex] = min(available_colors)
            else:
                colors[vertex] = max(colors.values()) + 1
    return [colors.get(k) for k in sorted(colors)]

def color_and_print_hypergraph(H):
    colors = algorithm(H)
    rgba_colors = []
    for color in colors:
        random.seed(color)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgba_colors.append((r, g, b, 1))
        random.seed(None)
    fig = Figure(figsize=(6,5))
    ax = fig.add_subplot(111)

    hnx.drawing.draw(
        H,
        with_edge_labels=False,
        nodes_kwargs={
            'facecolors': rgba_colors
        },
        ax=ax
    )
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=4, column=0,columnspan = 5)
    label = tk.Label(root, text="Использованные цвета: " + str(len(set(colors))))
    label.grid(row=3, column=0, columnspan=2)

def color_given_hypergraph(string):
    H = hnx.Hypergraph(dict(enumerate(ast.literal_eval(string))))
    color_and_print_hypergraph(H)

def color_random_hypergraph(n, m):
    n = int(n)
    m = int(m)
    vertices = list(range(n))
    edges = []
    while (vertices):
        if (m >= len(vertices)):
            edges.append(list(vertices))
            vertices.clear()
        else:
            size = random.randint(2, m)
            edge = random.sample(vertices, size)
            vertices = [item for item in vertices if item not in edge]
            if (len(vertices) == 1):
                edges.append(vertices + random.sample(list(set(list(range(n))) - set(vertices)),1))
                vertices.clear()
            edges.append(edge)
    vertices = list(range(n))
    b = len(edges) - 1
    for i in range(b):
        size = random.randint(0, max(m - 2, 0))
        edge = list(set(random.sample(vertices, size) + [edges[i][0], edges[i+1][0]]))
        edges.append(edge)
    H = hnx.Hypergraph(dict(enumerate(edges)))
    color_and_print_hypergraph(H)

    
if __name__ == "__main__": 
    root = tk.Tk()
    root.title("Раскрашивание гиперграфа")  
    root.geometry("600x600")
    root.grid_columnconfigure((0,1,2,3,4), weight=1)
    root.wm_resizable(width=False, height=False)

    label = tk.Label(text="Введите рёбра гиперграфа\n(Например: [[0, 1, 2],[1, 2, 3],[3, 4]])")
    entry = tk.Entry(root)
    button = tk.Button(root, text="Покрасить вершины", command=lambda: color_given_hypergraph(entry.get()))
    label2 = tk.Label(text="Введите количество вершин и\n максимальное количество вершин в узле")
    entry2 = tk.Entry(root)
    entry3 = tk.Entry(root)
    button2 = tk.Button(root, text="Покрасить вершины", command=lambda: color_random_hypergraph(entry2.get(),entry3.get()))

    label2.grid(row=0, column=3, columnspan = 2,sticky="we",padx=4, pady=4)
    entry2.grid(row=1, column=3, sticky="we",padx=4, pady=4)
    entry3.grid(row=1, column=4, sticky="we",padx=4, pady=4)
    button2.grid(row=2, column=4, sticky="we",padx=4, pady=4)
    label.grid(row=0, column=0, columnspan = 2, sticky="ew",padx=4, pady=4)
    entry.grid(row=1, column=0, sticky="we",padx=4, pady=4)
    button.grid(row=2, column=0, sticky="we",padx=4, pady=4)
    fig = Figure(figsize=(6,5))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=4, column=0,columnspan = 5)
    
    root.mainloop()
