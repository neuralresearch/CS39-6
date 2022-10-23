import networkx as nx
import os
import matplotlib.pyplot as plt
import random
import itertools

# Set directory
os.chdir('/Users/ruby/Desktop/Development/DATA5703/Graph Pair Generator')

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

print("Graphs have been imported with:")
print("    Set of all node attributes:", V_set)
print("    Set of all edge attributes:", E_set)

# Obtain graph from file
G = nx.read_gexf(path='./train/4.gexf')

# Assign pair graph G_s to G
G_s = G
V_s = list(nx.nodes(G_s))                        # List of node names
V_s_att = nx.get_node_attributes(G_s, 'type')    # List of node attributes
E_s = list(nx.edges(G_s))                        # List of edge names
E_s_att = nx.get_edge_attributes(G_s, 'valence') # List of edge attributes

print("Chose a graph to generate a pair for with:")
# print("    Nodes:", V_s)
print("    Node attributes:", V_s_att)
# print("    Edges:", E_s)
print("    Edge attributes:", E_s_att)

# Define methods for drawing and formatting
# - Convert to graph format
def write_graph(graph, nodes, edges):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

# - Draw graph
def draw_graph(graph, v_labels, e_labels):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12,12))
    nx.draw(graph, pos, edge_color='black', width=1, linewidths=1, node_size=400, node_color='purple', font_color='white', alpha=1, labels=v_labels)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=e_labels)
    plt.show()

# Create GEV
def generate_GEV(NR, NID, ER, EID):
    GEV = {"NR": NR, "NID": NID, "ER": ER, "EID": EID}
    print("Target graph edit vector (GEV):", GEV)

# ----Node Relabeling----

def NR(node_set, available_nodes, non_relabelled_nodes, node_attributes):
    node_to_relabel = random.choice(available_nodes) # Randomly select an available node to relabel
    new_label = random.choice(list(filter((non_relabelled_nodes[str(node_to_relabel)]).__ne__, node_set))) # Create a new label which is not equal to the old label, for a node that is non-relabelled

    print("Relabel node", node_to_relabel, "with current label", non_relabelled_nodes[node_to_relabel], "to", new_label)
    node_attributes[str(node_to_relabel)] = new_label # Relabel the node

    del non_relabelled_nodes[node_to_relabel]
    available_nodes.remove(node_to_relabel)

    return available_nodes, non_relabelled_nodes, node_attributes

# ----Node Insertion----

def NID(node_set, node_attributes):
    node_keys = list(map(int, list(node_attributes.keys())))
    new_key = str(max(node_keys) + 1) # Get the index of the next node
    new_value = random.choice(node_set) # Choose a random label from the node label set
    print("Insert new node", new_key, "with label", new_value)
    node_attributes.update({new_key:new_value}) # Insert new node
    return node_attributes

# ----Edge Deletion----

def ED(edges_to_delete, edges, edge_attributes, deleted_edges):
    available_edges = edges
    for i in range(edges_to_delete):
        edge_to_delete = random.choice(available_edges) # Randomly select an edge to delete
        deleted_edges.append(edge_to_delete) # Append the edge to delete to the deleted edges list
        print("Delete edge", edge_to_delete)
        print("Previous edge labels:", edge_attributes)
        del edge_attributes[edge_to_delete] # Delete the edge
        print("New edge labels:", edge_attributes)
        available_edges.remove(edge_to_delete)
    return deleted_edges, edge_attributes

# ----Edge Relabeling----

def ER(edge_set, available_edges, non_relabelled_edges, edge_attributes):
    edge_to_relabel = random.choice(available_edges) # Randomly select an available edge to relabel
    new_label = random.choice(list(filter((non_relabelled_edges[tuple(edge_to_relabel)]).__ne__, edge_set))) # Create a new label which is not equal to the old label, for an edge that is non-relabelled

    print("Relabel edge", edge_to_relabel, "with current label", non_relabelled_edges[edge_to_relabel], "to", new_label)
    edge_attributes[tuple(edge_to_relabel)] = new_label # Relabel the edge

    del non_relabelled_edges[tuple(edge_to_relabel)]
    available_edges.remove(edge_to_relabel)

    return available_edges, non_relabelled_edges, edge_attributes

# ----Edge Insertion----

def EI(node_attributes, edges, del_edges, edge_set, edge_attributes):
    # Generate all possible edge pairs
    node_keys = list(node_attributes.keys())
    existing_edges = edges
    for j in range(len(edges)):
        tup = edges[j]
        existing_edges.append(tup[::-1])

    possible_edges = set()
    for comb in itertools.combinations(node_keys, 2):
        if comb not in possible_edges:
            possible_edges.add(comb[::-1])
    possible_edges = list(possible_edges)

    deleted_edges = del_edges
    for x in range(len(del_edges)):
        tup = del_edges[x]
        deleted_edges.append(tup[::-1])

    # Filter out the edges that already exist (and make undirected)
    empty_edges = [] # Candidates for a new edge
    for k in range(len(possible_edges)):
        if (possible_edges[k] not in existing_edges and possible_edges[k] not in del_edges):
            empty_edges.append(possible_edges[k])

    # Choose a random edge to insert from the empty pairs
    new_edge = random.choice(empty_edges)
    new_edge_label = random.choice(edge_set)
    print("Insert new edge", new_edge, "with label", new_edge_label)
    edge_attributes.update({new_edge:new_edge_label})

    return edge_attributes

def generate_graph_pair(G, V_s, V_s_att, E_s, E_s_att):

    # Establish target GEV
    generate_GEV(NR=2, NID=2, ER=2, EID=4)

    # Node Relabelling
    nodes_NR = V_s.copy()
    node_attributes_NR = V_s_att.copy()

    print("Previous node labels:", V_s_att)
    for i in range(GEV["NR"]):
        nodes_NR, node_attributes_NR, V_s_att = NR(V_set, nodes_NR, node_attributes_NR, V_s_att)
    print("New node labels:", V_s_att)

    # Node Insertion
    print("Previous node labels:", V_s_att)
    for i in range(GEV["NID"]): # Perform for number of NID operations in the GEV
        node_attributes_NID = V_s_att.copy()
        V_s_att = NID(V_set, node_attributes_NID)
    print("New node labels:", V_s_att)

    # Randomly select ToDel in 0, 1, ... GEV[EID]
    to_del = random.randint(1, GEV["EID"]) # Select how many deletions will occur out of the number of EID operations
    to_del = 2 # Force to 1 or 2 for now (when using low GEV/testing)
    print("Number of edges to delete:", to_del)

    # Initialize Del_Edge = [] as empty list
    del_edge = [] # Store deleted edges

    # Edge Deletion
    del_edge, E_s_att = ED(to_del, E_s, E_s_att, del_edge)
    print("The following edges were deleted:", del_edge)

    # Edge Relabelling
    edges_ER = E_s.copy()
    edge_attributes_ER = E_s_att.copy()

    print("Previous edge labels:", E_s_att)
    for i in range(GEV["ER"]):
        edges_ER, edge_attributes_ER, E_s_att = ER(E_set, edges_ER, edge_attributes_ER, E_s_att)
    print("New edge labels:", E_s_att)

    # Edge Insertion
    print("Previous edges:", E_s_att)
    for i in range(GEV["EID"]-to_del): # Perform for number of NID operations in the GEV
        edge_attributes_EID = E_s_att.copy()
        node_attributes_EID = V_s_att.copy()
        edges_EID = E_s.copy()
        E_s_att = EI(node_attributes_EID, edges_EID, del_edge, E_set, edge_attributes_EID)
    print("New edges:", E_s_att)

generate_graph_pair(G, V_s, V_s_att, E_s, E_s_att)
