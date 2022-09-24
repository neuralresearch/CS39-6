# Graph pair generator

import networkx as nx
import os
import matplotlib.pyplot as plt
import random
import itertools

os.chdir('/Users/ruby/Desktop/Development/DATA5703/Graph Pair Generator')
G = nx.read_gexf(path='./train/4.gexf')

# Get node and edge attribute sets
V_set = []
E_set = []

dirName = 'train/'
filenames = os.listdir(dirName)
for filename in filenames:
    if filename.endswith(".gexf"):
        temp = nx.read_gexf(path=dirName+"/"+filename)
        for node in temp.nodes:
            temp_type = temp.nodes[node]['type']
            if temp_type not in V_set:
                V_set.append(temp_type)
        for edge in temp.edges:
            temp_type = temp.edges[edge]['valence']
            if temp_type not in E_set:
                E_set.append(temp_type)

print("Set of node attributes:", V_set)
print("Set of edge attributes:", E_set)

# Assign pair graph G_s to G
G_s = G
V_s = list(nx.nodes(G))                        # List of node names
V_s_att = nx.get_node_attributes(G, 'type')    # List of node attributes
E_s = list(nx.edges(G))                        # List of edge names
E_s_att = nx.get_edge_attributes(G, 'valence') # List of edge attributes

# print("Nodes:", V_s)
print("Node attributes:", V_s_att)
# print("Edges:", E_s)
print("Edge attributes:", E_s_att)

# Convert to graph format
def write_graph(graph, nodes, edges):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

# Draw graph
def draw_graph(graph, v_labels, e_labels):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12,12))
    nx.draw(graph, pos, edge_color='black', width=1, linewidths=1, node_size=400, node_color='purple', font_color='white', alpha=1, labels=v_labels)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=e_labels)
    plt.show()

draw_graph(G, V_s_att, E_s_att)

# Create GEV
GEV = {"NR": 1, "NID": 1, "ER": 1, "EID": 2}
print("GEV:", GEV)

# ----Node Relabeling----

non_relabelled_nodes = V_s_att

for i in range(GEV["NR"]):
    node_to_relabel = random.choice(V_s) # Randomly select a node
    new_label = random.choice(list(filter((non_relabelled_nodes[str(node_to_relabel)]).__ne__, V_set))) # Check that the new label is not equal to the old one and it is not relabelled
    print("Relabel node", node_to_relabel, "with current label", V_s_att[node_to_relabel], "to", new_label)
    print("Previous node labels:", V_s_att)
    V_s_att[str(node_to_relabel)] = new_label # Relabel the node
    print("New node labels:", V_s_att)

draw_graph(G_s, V_s_att, E_s_att)

# ----Node Insertion----

for i in range(GEV["NID"]):
    node_keys = list(map(int, list(V_s_att.keys())))
    new_key = str(max(node_keys) + 1) # Get next node index
    new_value = random.choice(V_set)
    print("Insert new node", new_key, "with label", new_value)
    print("Previous node labels:", V_s_att)
    V_s_att.update({new_key:new_value}) # Insert new node
    print("New node labels:", V_s_att)

# Randomly select ToDel in 0, 1, ... GEV[EID]
to_del = random.randint(1, GEV["EID"])
to_del = 1 # Force to 1 for now (when using low GEV/testing)
print("Number of edges to delete:", to_del)

# Initialize Del_Edge = [] as empty list
del_edge = []

# ----Edge Deletion----

for i in range(to_del):
    edge_to_delete = random.choice(E_s) # Randomly select an edge
    del_edge.append(edge_to_delete) # Append the edge to the deleted edges list
    print("Delete edge", edge_to_delete)
    print("Previous edge labels:", E_s_att)
    del E_s_att[edge_to_delete] # Delete the edge
    print("New edge labels:", E_s_att)

# ----Edge Relabeling----

non_relabelled_edges = E_s_att

for i in range(GEV["ER"]):
    edge_to_relabel = random.choice(E_s) # Randomly select an edge
    new_label = random.choice(list(filter((non_relabelled_edges[tuple(edge_to_relabel)]).__ne__, E_set))) # Check that the edge has not been relabelled and will not have the same label as the old one
    print("Relabel edge", edge_to_relabel, "with current label", E_s_att[edge_to_relabel], "to", new_label)
    print("Previous edge labels:", E_s_att)
    E_s_att[tuple(edge_to_relabel)] = new_label # Relabel edge
    print("New edge labels:", E_s_att)
    # print("Previous non-relabelled edges:", non_relabelled_edges)
    del non_relabelled_edges[tuple(edge_to_relabel)]
    # print("New non-relabelled edges:", non_relabelled_edges)

# ----Edge Insertion----

for i in range(GEV["EID"]-to_del):
    # Generate all possible edge pairs
    node_keys = list(V_s_att.keys())
    existing_edges = E_s
    for j in range(len(E_s)):
        tup = E_s[j]
        existing_edges.append(tup[::-1])

    possible_edges = set()
    for comb in itertools.combinations(node_keys, 2):
        if comb not in possible_edges:
            possible_edges.add(comb[::-1])
    possible_edges = list(possible_edges)

    deleted_edges = del_edge
    for x in range(len(del_edge)):
        tup = del_edge[x]
        deleted_edges.append(tup[::-1])

    # Filter out the edges that already exist (and make undirected)
    empty_edges = [] # Candidates for a new edge
    for k in range(len(possible_edges)):
        if (possible_edges[k] not in existing_edges and possible_edges[k] not in del_edge):
            empty_edges.append(possible_edges[k])
    print("Empty edges:", empty_edges)

    # Choose a random edge to insert from the empty pairs
    new_edge = random.choice(empty_edges)
    new_edge_label = random.choice(E_set)
    print("Insert new edge", new_edge, "with label", new_edge_label)
    print("Previous edge labels:", E_s_att)
    E_s_att.update({new_edge:new_edge_label})
    print("New edge labels:", E_s_att)

# Output (return): Graph pair (G, G_s); ground truth GEV
