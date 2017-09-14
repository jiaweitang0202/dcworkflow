import os
import shutil, sys
from graphviz import *
from IPython.display import Image, display
import pydot
from services import *
from data_reader import *
##########################
# Functions for projects #
##########################
WorkingDir = '../CivilizerWorkspace/'

class node:
    """Class to store information about individual components in the project"""
    global WorkingDir
    node_id = ""
    node_functionality = ""
    input_sources = ""
    input_file = ""
    output_file = ""
    tracking_file = "" 
    
    def createNode(self, node_name, node_type, Project):
        self.node_id = node_name
        self.node_functionality = node_type
        inputF = WorkingDir + Project + '_' + node_name + '.input'
        self.input_file = os.path.abspath(inputF) 
        outputF = WorkingDir + Project + '_' + node_name + '.output'
        self.output_file = os.path.abspath(outputF)
        tracker = WorkingDir + Project + '_' + node_name + '.tracker'
        self.tracking_file = os.path.abspath(tracker)
    
    def printNode(self):
        print("Name:", self.node_id)
        print("input file:", self.input_file)
        print("output file:", self.output_file)
        print("input sources:", self.input_sources)
        print("==================================")

class Project:
    """Class to store project information """
    Project_Name = ""
    wg = None
    nodes_details = []
    global WorkingDir
    """ Printing the nodes and eges as string """
    def printProject(self):
        if self.wg:
            wg_str = self.wg.to_string()
            print(wg_str)
        else:
            print("Error: either the project is empty or it has been closed ...")

    def newProject(self, P_Name):
        Project_Directory = WorkingDir + P_Name
        self.Project_Name = P_Name
        if not os.path.exists(WorkingDir):
            os.makedirs(WorkingDir)
        if not os.path.exists(Project_Directory):
            os.makedirs(Project_Directory)
            print ("New project created successfully\n")
        if self.nodes_details:
            for i in range(len(self.nodes_details)):
                self.nodes_details.remove(self.nodes_details[0])
        self.wg = pydot.Dot(type = 'digraph')
        
    def loadProject(self, P_Name):
        self.saveProject(1);
        self.closeProject(1)
        input_file = WorkingDir + P_Name +'/' + P_Name + '.dot'
        print ("load an existing project from: " + input_file + "\n")
        oldwg = pydot.graph_from_dot_file(input_file)[0]
        self.newProject(P_Name)
        self.wg = oldwg
        if not self.wg:
            print("This is an empty project .. the system will create a new project .. ")
            return
        for n in self.wg.get_nodes():
            newN = node()
            functionality = n.get_label().replace("\"", "")
            newN.createNode(n.get_name(), functionality, self.Project_Name)
            self.nodes_details.append(newN)
        for e in self.wg.get_edges():
            for i in range(len(self.nodes_details)):
                if self.nodes_details[i].node_id == e.get_destination():
                    # print ("To", to_nd.node_id, to_node) 
                    for j in range(len(self.nodes_details)):
                        if self.nodes_details[j].node_id == e.get_source():
                            # print ("From : ", self.nodes_details[j].output_file)
                            if not (self.nodes_details[j].output_file in self.nodes_details[i].input_sources):
                                self.nodes_details[i].input_sources = self.nodes_details[i].input_sources + self.nodes_details[j].output_file + ";"
                                # print("Modified : ", self.nodes_details[i].input_sources)
                                break
                    break

    def saveProject(self, flag = 0):
        if self.wg:
            output_file = WorkingDir + self.Project_Name +'/' + self.Project_Name + '.dot'
            if not flag: 
                print ("save the current project to: " + output_file + "\n")
            self.wg.write(output_file)

        
    def closeProject(self, flag = 0):
        self.saveProject(1)
        self.Project_Name = ""
        self.nodes_details = []
        self.wg = None
        if not flag:
            print ("close the current project")

    def deleteProject(self, Project_Name=None):
        if not Project_Name:
            Project_Name = self.Project_Name
        if not Project_Name:
            print("Project is not available or it has been closed .. ")
        else:
            Project_Directory = WorkingDir + Project_Name
            if os.path.exists(Project_Directory):
                shutil.rmtree(Project_Directory)
                self.Project_Name = ""
                self.wg = None
                self.nodes_details = []
                print ("Project ( ", Project_Name, ") has been deleted successfully .. ")

    """
        Adding a new node requires creating an object of the class 'node' to hold the 
        information about the node. This object is added to the nodes_details list
        and a node is added to the working graph
    """
    def addNode(self, node_name, functionality):
        if not self.wg:
            print("Error: Node cannot be added .. project is not available or it has been closed .. ")
            return
        Nodes = self.wg.get_nodes()
        for n in Nodes:
            if n.get_name() == node_name:
                print("Error: node (", node_name, ") was added before .. Please consider using different node name")
                return
        newN = node()
        newN.createNode(node_name, functionality, self.Project_Name)
        new_node = pydot.Node(node_name, label=functionality)
        self.wg.add_node(new_node)
        self.nodes_details.append(newN)

    """
        Deleting a given node requires deleting its information in nodes_details, 
        the edges from and to that node and finally removing the node from the graph
    """
    def deleteNode(self, node_name):
        if not self.wg:
            print("Error: Node cannot be added .. project is not available or it has been closed .. ")
            return
        Nodes = self.wg.get_nodes()
        reqNode = None
        for n in Nodes:
            if n.get_name() == node_name:
                reqNode = n
                break
        if not reqNode:
            print("Error: attempting to delete non-existing node .. ")
            return 
        Edges = self.wg.get_edges()
        for e in Edges:
            if ((e.get_source() == node_name) or (e.get_destination() == node_name)):
                self.wg.del_edge(e.get_source(), e.get_destination())
                # return
        self.wg.del_node(reqNode)
        for nn in self.nodes_details:
            if nn.node_id == node_name:
                self.nodes_details.remove(nn)
                break
        self.wg.del_node(n)
        print("Node (", node_name, ") was deleted successfully .. ")

    """Remove an edge from the graph"""
    def deleteEdge(self, from_node, to_node):
        if not self.wg:
            print("Error: attempting to delete non-existing edge .. ")
            return
        Edges = self.wg.get_edges()
        for e in Edges:
            if ((e.get_source() == from_node) and (e.get_destination() == to_node)):
                self.wg.del_edge(from_node, to_node)
                return
        print("Error: attempting to delete non-existing edge .. ")

    """Check if the edge already exist or not """
    def edge_exists(self, from_node, to_node):
        Edges = self.wg.get_edges()
        for e in Edges:
            if ((e.get_source() == from_node) and (e.get_destination() == to_node)):
                print("Error: Edge already exists .. ")
                return 1
        return 0

    def addEdge(self, from_node, to_node):
        edge_nodes = []
        """Check if the working graph has been created or not """
        if not self.wg:
            print("Error: Edge cannot be added .. project is not available or it has been closed .. ")
            return

        if (self.edge_exists(from_node, to_node)): 
            return 
        Nodes = self.wg.get_nodes()
        """ Search for 'from_node' int the graph """
        node_exist = 0
        for e in Nodes:
            if e.get_name() == from_node:
                node_exist = 1
                edge_nodes.append(e)
                break;
        if not node_exist: 
            print("Error: node (", from_node, ") doesn\'t exist")
            return 
        """ Search for 'to_node' int the graph """
        node_exist = 0
        for e in Nodes:
            if e.get_name() == to_node:
                node_exist = 1
                edge_nodes.append(e)
                break;
        if not node_exist: 
            print("The node (", to_node, ") doesn\'t exist")
            return 
        self.wg.add_edge(pydot.Edge(edge_nodes[0], edge_nodes[1]))

        # print ("Modifying the list of sources")
        for i in range(len(self.nodes_details)):
            if self.nodes_details[i].node_id == to_node:
                # print ("To", to_nd.node_id, to_node) 
                for j in range(len(self.nodes_details)):
                    if self.nodes_details[j].node_id == from_node:
                        # print ("From : ", self.nodes_details[j].output_file)
                        if not (self.nodes_details[j].output_file in self.nodes_details[i].input_sources):
                            self.nodes_details[i].input_sources = self.nodes_details[i].input_sources + self.nodes_details[j].output_file + ";"
                            # print("Modified : ", self.nodes_details[i].input_sources)
                            break
                break
        

    # def createEdge(from_node, to_node):
    def addNodeInput(self, node_name, newInputFile):
        if not self.wg:
            print("Error (Empty Project): project is not available or it has been closed .. ")
            return
        inputFileAdd = os.path.abspath(newInputFile)
        for n in self.nodes_details:
            if n.node_id == node_name:
                n.input_sources = n.input_sources + inputFileAdd + ";"
                break
    def executeNode(self, node_name):
        target_node = None
        for n in self.nodes_details:
            if n.node_id == node_name:
                functionality = n.node_functionality
                target_node = n
                break;
        if not target_node:
            print("Error, incorrect node_id .. ")
            return
        X = self.get_class_by_func(functionality)
        X.execute(target_node.input_file)

    def get_class_by_func(self, fn):
        if fn == 'Aurum': 
            X = Aurum(); return X
        elif fn == 'Tamr':
            X = Tamr(); return X
        elif fn == 'DBXFormer':
            X = DBXFormer(); return X
        elif fn == 'GoldenRecord':
            X = GoldenRecord(); return X
        elif fn == 'DongJoin':
            X = DongJoin(); return X
        elif fn == 'WenboMethod':
            X = WenboMethod(); return X
        elif fn == 'DetectDisguisedMissingValues':
            X = DetectDisguisedMissingValues(); return X
        elif fn == 'DBoost':
            X = DBoost(); return X 
        
            
##################################
#    Operating Workflow graph    #
##################################    


    
##########################
#    Helper Functions    #
##########################    
    
def viewPydot(pdot_graph):
    display(Image(pdot_graph.create_png())) 
    
# Node attributes
# 1. Tracker file for each node


# Tracker file
# 1. Input Tables: a string, by default "null"
# 2. Output Tables: a string, by default "null"
# 3. Function
# 4. Other informaiton for tracking 