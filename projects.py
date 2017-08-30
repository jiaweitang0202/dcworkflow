from graphviz import *
from IPython.display import Image, display
import pydot

##########################
# Functions for projects #
##########################

def newProject():
    print ("create a new project\n")
    return pydot.Dot(type = 'diagraph')
    
def loadProject(input_file):
    print ("load an existing project from: " + input_file + "\n")
    return pydot.graph_from_dot_file(input_file)[0]

def saveProject(workflow_graph, output_file):
    print ("save the current project to: " + output_file + "\n")
    workflow_graph.write(output_file)
    
def closeProject():
    print ("close the current project")

##################################
#    Operating Workflow graph    #
##################################    

def createNode(wg, from_node, function_name):
    new_node = pydot.Node(function_name)
    wg.add_edge(pydot.Edge(from_node, new_node))
    
    return wg
    
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