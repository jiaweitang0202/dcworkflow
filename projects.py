import os
import shutil, sys
from graphviz import *
from IPython.display import Image, display
import pydot

##########################
# Functions for projects #
##########################


class Project:
    """Class to store project information """
    Project_Name = ""
    wg = None

    def printProject(self):
        if self.wg:
            wg_str = self.wg.to_string()
            print(wg_str)
        else:
            print("Empty Project ...")

    def newProject(self, P_Name):
        ProjectsParentDir = '../Workspace/'
        Project_Directory = ProjectsParentDir + P_Name
        self.Project_Name = P_Name
        if not os.path.exists(ProjectsParentDir):
            os.makedirs(ProjectsParentDir)
        if not os.path.exists(Project_Directory):
            os.makedirs(Project_Directory)
            print ("New project created successfully\n")
        self.wg = pydot.Dot(type = 'diagraph')
        
    def loadProject(self, P_Name):
        self.saveProject(1);
        ProjectsParentDir = '../Workspace/'
        self.Project_Name = P_Name
        input_file = ProjectsParentDir + P_Name +'/' + P_Name + '.dot'
        print ("load an existing project from: " + input_file + "\n")
        self.wg = pydot.graph_from_dot_file(input_file)[0]

    def saveProject(self, flag = 0):
        if self.wg:
            ProjectsParentDir = '../Workspace/'
            output_file = ProjectsParentDir + self.Project_Name +'/' + self.Project_Name + '.dot'
            if not flag: 
                print ("save the current project to: " + output_file + "\n")
            self.wg.write(output_file)

        
    def closeProject(self):
        self.saveProject(1)
        self.Project_Name = ""
        self.wg = None
        print ("close the current project")

    def deleteProject(self, Project_Name=None):
        if not Project_Name:
            Project_Name = self.Project_Name
        if not Project_Name:
            print("Project is not available or it has been closed .. ")
        else:
            ProjectsParentDir = '../Workspace/'
            Project_Directory = ProjectsParentDir + Project_Name
            if os.path.exists(Project_Directory):
                shutil.rmtree(Project_Directory)
                self.Project_Name = ""
                self.wg = None
                print ("Project ( ", Project_Name, ") has been deleted successfully .. ")
        
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