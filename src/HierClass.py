# -*- coding: utf-8 -*-
"""
Created on Thu Jul 04 19:57:35 2013

@author: drewhill
"""

class hier:
    
    def __init__(self,projID):
        self.id = projID
        self.role = ""
        self.superiors = []
        self.subordinates = []
        
    def impSup(self,empID):
        #Assume all is good
        self.superiors.append(empID)
        
    def impSub(self,empID):
        #Assume all is good
        self.subordinates.append(empID)
    
    def addSup(self,empID):
        if empID not in self.superiors:        
            self.superiors.append(empID)
            return 1
        return 0
            
    def addSub(self,empID):
        if empID not in self.subordinates:
            self.subordinates.append(empID)
            return 1
        return 0
            
    def remSup(self,empID):
        self.superiors.remove(empID)
        
    def remSub(self,empID):
        self.subordinates.remove(empID)
        
    def setRole(self,rol):
        self.role=rol
        
    def retSup(self):
        return self.superiors
        
    def retSub(self):
        return self.subordinates
    
    def retRole(self):
        return self.role
    
    def retID(self):
        return self.id