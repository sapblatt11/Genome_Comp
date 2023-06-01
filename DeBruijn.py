import networkx as nx
import matplotlib.pyplot as plt
''' 
Split a sequence into parts of length k and return them with their 
respect counts.

Parameters: 
	- seq: an input string
	- k: chunk sizes to test for overlap
Returns a dictionary.
'''


def get_counts_from_seq(seq, k=50, circular=True):
    collection = {}  # dict

    for i in range(0, len(seq)):
        chunk = seq[i:i + k]  # Gets the next sequence chunk between i and k

        chunk_length = len(chunk)

        # For sequences that ideally wrap around
        if circular:
            if chunk_length != k:
                chunk += seq[:(k - chunk_length)]

        # Linear sequences
        else:
            if chunk_length != k:
                continue

        if chunk in collection:
            collection[chunk] += 1  # Already exists in collection
        else:
            collection[chunk] = 1  # New entry to the collection

    return collection


'''
'''
def get_edges(collection):

    edges = set()

    for j in collection:
        for k in collection:
            if j != k:
                if j[1:] == k[:-1]:
                    edges.add((j[:-1], k[:-1]))  # Add overlap from j to k
                if j[:-1] == k[:-1]:
                    edges.add((k[:-1], j[:-1]))  # Add overlap from k to j

    return edges

#edges should be a list of tuples    
def generate_diGraph(edges):
    graph = nx.DiGraph()
    graph.add_edges_from(edges)

    return graph

# TODO: Add name as file name parameter
def save_graph(graph):
    ## Saves the graph as an image
    plt.rcParams['figure.figsize'] = [300, 300]
    nx.draw_networkx(graph, arrows=True, with_labels=False, node_size=10)
    plt.show()
    #plt.savefig("graph.png", format="PNG")
    plt.clf()

# TODO: https://networkx.org/documentation/stable/reference/functions.html#nodes
# Returns true when the graph is a loop with no deadends
# Assumption: a graph is a loop when no input or output edge exists more than once
def loop_test(graph):
    all_inputs = []
    all_outputs = []
    total_edges = 0

    for node in graph.nodes(): 
        in_edges = list(nx.neighbors(graph, node))
        all_edges = list(nx.all_neighbors(graph, node)) #Becomes only output edges

        for edge in all_edges:
            if edge in in_edges:
                all_edges.remove(edge)
        all_inputs.extend(in_edges)
        all_outputs.extend(all_edges)

    total_edges = len(all_inputs) + len(all_outputs)

    #Implies graph loops on itself (edges/2 because total_edges counts in and out)
    edges_eq_nodes = (total_edges/2 == len(graph.nodes()))

    #Checks that no input or output edge exists twice
    is_loop = not(check_dupes(all_inputs) and check_dupes(all_outputs))

    return is_loop and edges_eq_nodes


# Utilize that sets cannot have duplicates to efficiently check for dupes
# True indicates that there are duplicates
def check_dupes(input_list):
    return len(input_list) != len(set(input_list))
	