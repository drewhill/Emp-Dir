# -*- coding: utf-8 -*-
"""
Created on Thu Jul 04 19:57:11 2013

@author: drewhill
"""
#from AbilListClass.py import AbilListClass
import os

class ability: #for both skills and interests
    def __init__(self,newID,val,kind): #constructor
        self.id = newID
        self.name = val
        self.type = kind #Skill or Int
        self.empList = dict() #empID, skill level (1-3)
        self.notes = ""

    def rename(self,val):
        self.inFile()
        self.name = val
        self.outFile()
        
    def addEmp(self,empID,lvl=1):
        self.inFile() #get most updated
        if not self.empList.has_key(empID):
            self.empList[empID]=lvl
            self.outFile()
            
    def chgLvl(self,empID,lvl):
        self.inFile()
        if self.empList.has_key(empID):
            self.empList[empID]=lvl
            self.outFile()
            
    def remEmp(self,empID):
        self.inFile() #get most updated
        if self.empList.has_key(empID):
            self.empList.pop(empID)
            self.outFile()
            
    def retList(self):
        return self.empList.items()
        
    def inFile(self):
        if self.type == "Skill":
            ext=".skl"
        else:
            ext=".int"
        if not os.path.isfile(os.path.join(os.getcwd(),str(self.type),str(self.id)+ext)):
            return -1
        with open(os.path.join(os.getcwd(),str(self.type),str(self.id)+ext),'r') as f:
            line=f.readline()
            line=line.rstrip("\n") #"ID"
            line=f.readline()
            line=line.rstrip("\n") #ID
            self.id=int(line)
            line=f.readline()
            line=line.rstrip("\n") #"Name"            
            line=f.readline()
            line=line.rstrip("\n") #Name            
            self.name=line
            line=f.readline()
            line=line.rstrip("\n") #"Type"            
            line=f.readline()
            line=line.rstrip("\n") #Type                        
            if not line=="Notes":
                self.type=line            
                line=f.readline()
                line=line.rstrip("\n") #"Notes"            
            else:
                self.type=""
            line=f.readline()
            line=line.rstrip("\n") #Notes
            if not line=="Employee List":
                self.notes=line
                line=f.readline()
                line=line.rstrip("\n") #"Employee List"
            else:
                self.notes=""
            self.empList=dict() #reset it
            for line in f:
                line=line.rstrip("\n")
                empID,empLvl=line.split(":")
                self.empList[int(empID)]=int(empLvl)
        
    def outFile(self):
        if self.type == "Skill":
            ext=".skl"
        else:
            ext=".int"
        with open(os.path.join(os.getcwd(),str(self.type),str(self.id)+ext),'w+') as f:
            f.write("ID"+"\n")            
            f.write(str(self.id)+"\n")
            f.write("Name"+"\n")            
            f.write(str(self.name)+"\n")
            f.write("Type"+"\n")            
            f.write(str(self.type)+"\n")
            f.write("Notes"+"\n")
            if(not self.notes==""):
                f.write(str(self.notes)+"\n")            
            #TODO: Sanitize output for colons and newlines
            f.write("Employee List"+"\n")            
            for empID, empLvl in self.empList.items():
                f.write(str(empID))
                f.write(":")
                f.write(str(empLvl))
                f.write("\n")