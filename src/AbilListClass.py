# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 00:06:49 2013

@author: drewhill
"""

from AbilClass import ability
import os

class AbilListClass:
    def __init__(self,kind):
        self.abilList=dict() #key = id, value = name
        self.kind = kind #"Skill" or "Int"
        self.lastID = 0
    
    def inFile(self):
        if not os.path.isfile(os.path.join(os.getcwd(),str(self.kind),str(self.kind)+"List.lst")):
            return -1
        with open(os.path.join(os.getcwd(),str(self.kind),str(self.kind)+"List.lst"),'r') as f:
            line=f.readline()
            line=line.rstrip("\n") #"LastID"
            line=f.readline()
            line=line.rstrip("\n") #last ID
            self.lastID=int(line)
            line=f.readline()
            line=line.rstrip("\n") #"Kind"
            line=f.readline()
            line=line.rstrip("\n") #Kind
            self.kind=line
            line=f.readline()
            line=line.rstrip("\n") #"AbilKind List"
            self.abilList = dict() #reset it
            for line in f:
                line=line.rstrip("\n")
                abilID,abilName=line.split(":")
                self.abilList[int(abilID)]=abilName    
    
    def outFile(self):
        with open(os.path.join(os.getcwd(),str(self.kind),str(self.kind)+"List.lst"),'w+') as f:
            f.write("LastID"+"\n")            
            f.write(str(self.lastID)+"\n")
            f.write("Kind"+"\n")            
            f.write(str(self.kind)+"\n")            
            #TODO: Sanitize output for colons and newlines
            f.write(str(self.kind)+" List"+"\n")            
            for abilID, abilName in self.abilList.items():
                f.write(str(abilID))
                f.write(":")
                f.write(str(abilName))
                f.write("\n")
    
    def addAbil(self,abilName):
        #Add to master list
        #Assuming it has already been checked to not be in list
        self.inFile()
        self.lastID+=1
        tempClass = ability(self.lastID,abilName,self.kind)
        self.abilList[self.lastID]=abilName
        self.outFile() #write updated file
        tempClass.outFile() #create and write the class file          
        return self.lastID
        
    def remAbil(self,abilID):
        self.inFile()
        tempAbil=ability(abilID,"",self.kind)
        tempAbil.inFile()
        from EmpClass import employee #Remove from all employees first
        for empID, empSk in tempAbil.retList():
            tempEmp=employee(empID)
            tempEmp.inFile()
            if self.kind=="Int":
                tempEmp.remInt(abilID)
            else:
                tempEmp.remSkill(abilID)
        #Then remove from the list
        self.abilList.pop(abilID)
        self.outFile()
        
    def renameAbil(self,abilID,newNm):
        self.inFile()
        tempAbil=ability(abilID,"",self.kind)
        tempAbil.inFile()
        tempAbil.rename(newNm)
        self.abilList[abilID]=newNm
        self.outFile()
        
        
    def retName(self,ID):
        self.inFile()
        return self.abilList[ID]
        
    def retListItems(self):
        self.inFile()
        return self.abilList.items()
        
    def abilExist(self,abilName):
        self.inFile()
        return (abilName in self.abilList.values())