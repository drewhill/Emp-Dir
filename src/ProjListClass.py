# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 23:27:57 2013

@author: drewhill
"""
import os
import shutil
from ProjClass import project
from EmpClass import employee


class ProjList:
    #Master project list
    def __init__(self):
        self.projList = dict() #dictionary with id as key and name as value
        self.lastID = 0
        
    def addProj(self,name):
        self.inFile()
        self.lastID += 1
        self.projList[self.lastID]=name   
        self.outFile()
        from ProjClass import project
        newProj = project(self.lastID,name)
        newProj.outFile()        
        return self.lastID
        
    def remProj(self,projID):
        self.inFile()
        self.projList.pop(projID)
        self.outFile()

        self.breakLinks(projID)        
        
        if not os.path.exists(os.path.join(os.getcwd(),"ProjArchive")):
            os.mkdir(os.path.join(os.getcwd(),"ProjArchive"))
        filename = str(projID)+".prj"
        shutil.move(os.path.join(os.getcwd(),"projects",filename),os.path.join(os.getcwd(),"ProjArchive",filename))
        #Move the file to an archive folder

    def breakLinks(self,projID):
        #break external links, but don't change existing proj file for archive purposes
        tempProj=project(projID)        
        tempProj.inFile()        

        #remove each project and all superiors/subordinates        
        for empID in tempProj.retList():
            tempEmp=employee(empID)
            tempEmp.remProjArch(projID)
        
        return 1
        
    def inFile(self):
        if not os.path.isfile(os.path.join(os.getcwd(),"ProjectList","projList.lst")):
            return -1
        with open(os.path.join(os.getcwd(),"ProjectList","projList.lst"),'r') as f:
            line=f.readline()
            line=line.rstrip("\n") #"LastID"
            line=f.readline()
            line=line.rstrip("\n") #last ID
            self.lastID=int(line)
            line=f.readline()
            line=line.rstrip("\n") #"Project List"
            for line in f:
                line=line.rstrip("\n")
                projID,projName=line.split(":")
                self.projList[int(projID)]=projName                       
        
    def outFile(self):
        with open(os.path.join(os.getcwd(),"ProjectList","projList.lst"),'w+') as f:
            f.write("LastID"+"\n")            
            f.write(str(self.lastID)+"\n")
            #TODO: Sanitize output for colons and newlines
            f.write("Project List"+"\n")            
            for projID, projName in self.projList.items():
                f.write(str(projID))
                f.write(":")
                f.write(projName)
                f.write("\n")
          
    def retLastID(self):
        self.inFile()
        return self.lastID
            
    def retName(self,projID):
        self.inFile()
        return self.projList[projID]
        
    def renamePL(self,projID,pName):
        self.inFile()
        self.projList[projID]=pName
        self.outFile()
        
    def retListItems(self):
        self.inFile()
        return self.projList.items()