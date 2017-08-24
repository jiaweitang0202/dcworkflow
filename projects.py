#import jgraph
from graphviz import *

def newProject():
    print ("create a new project\n")
    dot = Digraph('workflow_graph')

    return dot
    
    
def loadProject(input_file):
    print ("load an existing project from: " + input_file + "\n")
    
    file = open(input_file, 'r')
    text = file.read()
    dot = Source(text)
    
    return dot


def saveProject(dot, output_file):
    print ("save the current project to: " + output_file + "\n")
    dot.render(output_file)
    
def closeProject():
    print ("close the current project")
    
def addFunction(dot):
    dot.add_node('D', 'Golden Record')
    #dot.addedge('C', 'D')
    return dot