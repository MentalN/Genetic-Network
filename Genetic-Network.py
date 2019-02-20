import random
import decimal
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import gVar

decimal.getcontext().prec = 5


# Global method to assign genetic code
def assign_genetic_code(i_code):
    """
    :param i_code: string variable that will be storing the genetic code of the node
    :return: the gene code string of the node
    """
    for i in range(0, 9):
        i_code += random.choice(gVar.genotype)
    return i_code


#   Node class
class Node:
    """
    Graph node. Processes number input, and returns an output that was calculated depending on the instructions of the
    randomly chosen gene code.
    """
    def __init__(self, i_name=None):
        """
        Initializes node name, data contained, adjacency list, activation status, and gene code string variable.
        :param i_name: Optional label for the node
        """
        self.name = i_name
        self.data = 1
        self.adjacencyList = []
        self.activated = False
        self.gene_code = ""
        self.gene_code = assign_genetic_code(self.gene_code)

    def transcriber(self, in_data):
        """
        Transcribe the input of data depending on the instructions of the node's genetic code.
        :param in_data: some number to be processed
        :return: processed data
        """
        for i in self.gene_code:
            if i == "+":
                self.data = self.data + in_data
            elif i == "-":
                self.data = self.data - in_data
            elif i == "*":
                self.data = self.data * in_data
            elif i == "/":
                self.data = self.data / in_data
            elif i == "e":
                self.data = self.data ** in_data
            elif i == "2":
                self.data = self.data + 2 * in_data
            elif i == "9":
                self.data = self.data + 9 * in_data
            elif i == "p":
                self.data = self.data + 3.14
            else:
                continue
        return self.data

    def get_degree(self):
        """
        :return: Node degree, or the number of edges, by calculating the length of the adjacency list array.
        """
        return len(self.adjacencyList)


#   Graph class
class Graph:
    """
    A network of connected nodes with random genetic code per each node.
    """

    num_nodes_created = 0

    def __init__(self, i_name=None):
        """
        - Add a random number of nodes to the graph upon its instantiation.
        - Initializes the graph list of nodes
        - Initializes the graph net value given by the processing from node to node within the graph
        - Assign adjacency to each node in the graph
        :param i_name: Optional label for the graph
        """
        self.name = i_name
        self.node_lists = []
        self.graph_net_value = 0

        #   Add a random number of nodes
        for num in range(random.randint(gVar.min_nodes, gVar.max_nodes)):
            self.node_lists.append(Node("N"+str(self.num_nodes_created)))
            self.num_nodes_created += 1

        #   Add random adjacency to the graph nodes
        pos = 0
        for i in self.node_lists:
            while len(i.adjacencyList) <= gVar.max_adj:
                if len(i.adjacencyList) >= gVar.max_adj:
                    break
                else:
                    print("A: " + str(pos + 1))
                    print("B:" + str(len(self.node_lists) - 1))
                    rand_node_index = random.randint(pos + 1, len(self.node_lists) - 1)
                    if len(self.node_lists[rand_node_index].adjacencyList) >= gVar.max_adj:
                        continue
                    else:
                        i.adjacencyList.append(self.node_lists[rand_node_index])
                        self.node_lists[rand_node_index].adjacencyList.append(i)
            pos += 1

    def activate(self, in_data):
        """
        Activates the graph processing of input data.
        - Start with a random node:
        1-  if the specific node is not already active:
            - Feed it input.
            - Add the returned result to graph's net total.
            - Set the node to activated status to true so it won't be used for processing again.
        2- If the specific node is already active:
            - Check if all the other graph nodes are also already active. If they all indeed are: break.
            - If all graph nodes are still not active, then check the adjacent nodes:
                2A- If not all adjacent nodes are active, set the current node to the next inactive adjacent node.
                2B- If all adjacent nodes are already active, set the current node to the next inactive node in graph
        :param in_data: input data
        :return: the graph's net value
        """
        #   pick a random node to start processing from
        curr_node = random.choice(self.node_lists)
        while True:
            if curr_node.activated is False:
                self.graph_net_value += curr_node.transcriber(in_data)
                curr_node.activated = True
            elif curr_node.activated is True:
                #   Check if the whole graph has been traversed
                if self.coverage_check() is True:
                    break
                else:
                    #   Check if all adjacent nodes have been traversed, but the whole graph is still not
                    if self.adjacency_check(curr_node.adjacencyList) is False:
                        curr_node = next(node for node in curr_node.adjacencyList if node.activated is False)
                    elif self.adjacency_check(curr_node.adjacencyList) is True:
                        curr_node = next(node for node in self.node_lists if node.activated is False)
        return self.graph_net_value

    def coverage_check(self):
        """
        Check if all the nodes in the graph are active
        :return: True if all the nodes in the graph have been activated, False if not.
        """
        covered = True
        for n in self.node_lists:
            if n.activated is False:
                covered = False
        return covered

    def adjacency_check(self, adj_list):
        """
        Check if all adjacent nodes are active
        :return: True if all adjacent nodes have been activated, False if not.
        """
        adj_covered = True
        for n in adj_list:
            if n.activated is False:
                adj_covered = False
        return adj_covered

    def regenerate_nodes(self, num_nodes):
        """
        generate nodes again in the graph with random genetic code
        :param num_nodes: number of nodes to be generated
        """
        for num in range(num_nodes):
            self.node_lists.append(Node("N"+str(self.num_nodes_created)))
            self.num_nodes_created += 1

    def reset(self):
        """
        Reset the graph's net value for reprocessing.
        """
        self.graph_net_value = 0

    def plot(self):
        from_list = []
        to_list = []
        for i in self.node_lists:
            print("node " + str(i.name))
            attr = []
            for X in i.adjacencyList:
                attr.append(X.name)
            print(attr)
            for j in i.adjacencyList:
                from_list.append(i.name)
                to_list.append(j.name)
        df = pd.DataFrame({'from': from_list, 'to': to_list})
        G = nx.from_pandas_edgelist(df, 'from', 'to')
        nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.random_layout(G))
        plt.title("random")
        plt.show()


class Environment:
    """
    Implements genetic algorithm that selects for a user specified criteria.
    """
    def __init__(self):
        """
        Initializes an empty graph list.
        """
        self.graph_list = []
        self.dead_graphs = []

    def add_graph(self, i_graph):
        """
        Add graph networks to the selection environment, accept a list of graphs or a single graph object.
        :param i_graph: graph list or a graph object
        """
        #   If the input is a list
        if type(i_graph) is list:
            self.graph_list.extend(i_graph)
        #   If the input is an object
        else:
            self.graph_list.append(i_graph)

    def reset(self):
        """
        Reset graph list to empty
        """
        self.graph_list = []

    def select_for_largest(self, num_dying, in_data):
        """
        Apply artificial selection to the graphs in the environment selecting for highest graph net value.
        :param num_dying: number of the least performing graphs that won't survive selection and be removed from list.
        :param in_data: data fed to each graph.
        """
        #   Check if the number of graphs to die is equal or larger than the number of graphs in the environment.
        if num_dying >= len(self.graph_list):
            #   Raise value error if that is the case
            raise ValueError("Selection value must be less than the number of graphs in the environment!")
        for g in self.graph_list:
            g.activate(in_data)
        #   Sort graphs by their net value from highest to lowest
        self.graph_list.sort(key=lambda x: x.graph_net_value, reverse=True)
        for i in range(0, num_dying):
            dead_graph = self.graph_list.pop()
            self.dead_graphs.append(dead_graph.name)

    def select_for_smallest(self, num_dying, in_data):
        """
        Apply artificial selection to the graphs in the environment selecting for highest graph net value.
        :param num_dying: number of the least performing graphs that won't survive selection and be removed from list.
        :param in_data: data fed to each graph.
        """
        #   Check if the number of graphs to die is equal or larger than the number of graphs in the environment.
        if num_dying >= len(self.graph_list):
            #   Raise value error if that is the case
            raise ValueError("Selection value must be less than the number of graphs in the environment!")
        for g in self.graph_list:
            g.activate(in_data)
        #   Sort graphs by their net value from highest to lowest
        self.graph_list.sort(key=lambda x: x.graph_net_value, reverse=False)
        for i in range(0, num_dying):
            dead_graph = self.graph_list.pop()
            self.dead_graphs.append(dead_graph.name)

    def replace_dead_nodes(self, num_nodes):
        """
        replaces the dead nodes with new nodes with different gene code
        :param num_nodes: number of new nodes to be generated in each graph.
        """
        for g in self.graph_list:
            g.regenerate_nodes(num_nodes)

    def plot_all_graphs(self):
        for i in self.graph_list:
            i.plot()


g1 = Graph("g1")
g1.plot()
