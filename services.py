################################
# Service Entity Consolidation #
################################

class EntityConsolidation(object): #superclass, inherits from default object
    def getName(self):
        raise NotImplementedError
    
class GoldenRecord(EntityConsolidation): #subclass, inherits from SuperHero
    def getName(self):
        return "Golden Record for Entity Consolidation" 
    def excute(inputTables):
        outputTables = "null"
        print (inputTables)
        return outputTables