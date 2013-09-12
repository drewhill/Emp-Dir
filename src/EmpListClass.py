# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 00:07:09 2013

@author: drewhill
"""
import os
import shutil
from EmpClass import employee
from AbilClass import ability

class EmpList:
    #This is only for the master emp list
    def __init__(self):
        self.empList = dict() #dictionary with id as key and name as value
        self.lastID = 0
        
    def addEmp(self,name):
        self.inFile()
        nmList=self.empList.values()
        if name in nmList:
            #already exists
            for nmID,nm in self.empList.items():
                if nm == name:
                    return nmID #return the ID for already existing emp
        self.lastID += 1
        self.empList[self.lastID]=name
        self.outFile()
        newEmp = employee(self.lastID,name)
        newEmp.outFile()
        return self.lastID
        
    def renameEmp(self,empID,newNm):
        self.inFile()
        self.empList[empID]=newNm
        self.outFile()
        
    def remEmp(self,empID):
        self.inFile()
        self.empList.pop(empID)
        self.outFile()
        
        self.breakLinks(empID) 
        
        if not os.path.exists(os.path.join(os.getcwd(),"EmpArchive")):
            os.mkdir(os.path.join(os.getcwd(),"EmpArchive")) #TODO: Move this to check at launch of main instead along with other folders
        filename = str(empID)+".emp"
        shutil.move(os.path.join(os.getcwd(),"employees",filename),os.path.join(os.getcwd(),"EmpArchive",filename))
        #Move the file to an archive folder
        
    def breakLinks(self,empID):
        #break external links, but don't change existing emp file for archive purposes
        tempEmp=employee(empID)        
        tempEmp.inFile()        


        #remove each project and all superiors/subordinates        
        for projID,projHier in tempEmp.retProjList():
            for sub in projHier.retSub():
                tempEmp=employee(sub)
                tempEmp.inFile()
                tempEmp.remProjSup(projID,empID,0)#remove sup from sub, no push
            for sup in projHier.retSup():
                tempEmp=employee(sup)
                tempEmp.inFile()
                tempEmp.remProjSub(projID,empID,0)#remove sup from sub, no push
            #remove emp from Proj
            from ProjClass import project
            tempProj = project(projID,"")
            tempProj.inFile()
            tempProj.remEmp(empID)

        for skID,skLvl in tempEmp.retSkillList():
            tempSk=ability(skID,"temp","Skill")
            tempSk.inFile()
            tempSk.remEmp(empID)

        for intID,intLvl in tempEmp.retIntList():
            tempInt=ability(intID,"temp","Int")
            tempInt.inFile()
            tempInt.remEmp(empID)       
        
        return 1
        
    def inFile(self):
        if not os.path.isfile(os.path.join(os.getcwd(),"EmpList","empList.lst")):
            return -1
        with open(os.path.join(os.getcwd(),"EmpList","empList.lst"),'r') as f:
            line=f.readline()
            line=line.rstrip("\n") #"LastID"
            line=f.readline()
            line=line.rstrip("\n") #last ID
            self.lastID=int(line)
            line=f.readline()
            line=line.rstrip("\n") #"Employee List"
            self.empList=dict() #reset it
            for line in f:
                line=line.rstrip("\n")
                empID,empName=line.split(":")
                self.empList[int(empID)]=empName    
        
    def outFile(self):
        with open(os.path.join(os.getcwd(),"EmpList","empList.lst"),'w+') as f:
            f.write("LastID"+"\n")            
            f.write(str(self.lastID)+"\n")
            #TODO: Sanitize output for colons and newlines
            f.write("Employee List"+"\n")            
            for empID, empName in self.empList.items():
                f.write(str(empID))
                f.write(":")
                f.write(empName)
                f.write("\n")
                
    def retName(self,empID):
        return self.empList[empID]
    
    def retLastID(self):
        return self.lastID
        
    def retListItems(self):
        return self.empList.items()