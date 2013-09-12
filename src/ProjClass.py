# -*- coding: utf-8 -*-
"""
Created on Thu Jul 04 19:57:11 2013

@author: drewhill
"""
import os

class project:
    
    def __init__(self,newID,val="tempload"): #constructor
        self.name = val
        self.id = newID
        self.notes=""
        self.empList=[]
        self.lead=""
        self.desc=""
        self.sharepointLink=""
        self.photo=""

    def setNotes(self,val=""):
        self.inFile()
        self.notes = val
        self.outFile()
        
    def setDesc(self,val=""):
        self.inFile()
        self.desc = val
        self.outFile()        
    
    def setSharepointLink(self,val=""):
        self.inFile()        
        self.sharepointLink=val
        self.outFile()
        
    def setPhotoLink(self,val=""):
        self.inFile()
        self.photo=val
        self.outFile()

    def addEmp(self,val):
        self.inFile()        
        if val not in self.empList:
            self.empList.append(val)
        self.outFile()
			
    def setLead(self,val=""):
        self.inFile()        
        self.lead = val
        self.outFile()
		
    def remEmp(self,val):
        self.inFile()
        self.empList.remove(val)
        self.outFile()        
		
    def chgLead(self,val=""):
        self.inFile()        
        self.lead = val
        self.outFile()        
		
    def retList(self):
        return self.empList
		
    def retLead(self):
        return self.lead
		
    def retID(self):
        return self.id
        
    def retDesc(self):
        return self.desc
        
    def retEmailList(self):
        emList=str()
        from EmpClass import employee
        for empID in self.empList:
            tempEmp=employee(empID)            
            tempEmp.inFile()
            empEm=tempEmp.retEmail()
            if not empEm=="":
                emList+=empEm+"; "
        return emList #return a list of employee emails
            
    
    def retSharepointLink(self):
        return self.sharepointLink
        
    def retPhotoLink(self):
        return self.photo
	
    def renameProj(self,val):
        self.inFile()        
        if not self.name == val:
            self.name = val
            self.outFile()
            from ProjListClass import ProjList
            tempList = ProjList()
            tempList.inFile() #get most updated list
            tempList.renamePL(self.id,val)
            
    def inFile(self):
        if not os.path.isfile(os.path.join(os.getcwd(),"projects",str(self.id)+".prj")):
            return -1
        with open(os.path.join(os.getcwd(),"projects",str(self.id)+".prj"),'r') as f:
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
            line=line.rstrip("\n") #"Lead"            
            line=f.readline()
            line=line.rstrip("\n") #Lead                        
            if not line=="Desc":
                self.lead=int(line)            
                line=f.readline()
                line=line.rstrip("\n") #"Desc"            
            else:
                self.lead=""
            line=f.readline()
            line=line.rstrip("\n") #Desc
            if not line=="Notes":
                line = "\n".join(line.split("<br>"))
                self.desc=line
                line=f.readline()
                line=line.rstrip("\n") #"Notes"
            else:
                self.desc=""
            line=f.readline()
            line=line.rstrip("\n") #Notes  
            if not line=="Sharepoint Link":
                self.notes=line
                line=f.readline()
                line=line.rstrip("\n") #"Sharepoint"
            else:
                self.notes=""
            line=f.readline()
            line=line.rstrip("\n") #sharepointLink
            if not line=="Photo Link":            
                self.sharepointLink=line
                line=f.readline()
                line=line.rstrip("\n") #PhotoLink
            else:
                self.sharepointLink=""
            line=f.readline()
            line=line.rstrip("\n") #"Photo Link"
            if not line=="EmpList":            
                self.photo=line
                line=f.readline()
                line=line.rstrip("\n") #EmpList
            else:
                self.photo=""
            self.empList=list() #clear it, start over
            for line in f:
                line=line.rstrip("\n")
                self.empList.append(int(line))   
        
    def outFile(self):
        with open(os.path.join(os.getcwd(),"projects",str(self.id)+".prj"),'w+') as f:
            f.write("ID"+"\n")
            f.write(str(self.id)+"\n")
            f.write("Name"+"\n")
            f.write(str(self.name)+"\n")
            f.write("Lead"+"\n")
            if(not self.lead == ""):
                f.write(str(self.lead)+"\n")
            f.write("Desc"+"\n")
            if(not self.desc == ""):
                tempDesc=self.desc
                tempDesc = "<br>".join(tempDesc.split("\n"))
                tempDesc = "<br>".join(tempDesc.split("\r"))
                f.write(str(tempDesc)+"\n")
            f.write("Notes"+"\n")
            if(not self.notes == ""):            
                f.write(str(self.notes)+"\n")
            f.write("Sharepoint Link"+"\n")
            if(not self.sharepointLink == ""):            
                f.write(str(self.sharepointLink)+"\n")            
            #TODO: Sanitize output for colons and newlines
            f.write("Photo Link"+"\n")
            if(not self.photo == ""):            
                f.write(str(self.photo)+"\n")                       
            f.write("EmpList"+"\n")
            for empID in self.empList:
                f.write(str(empID))
                f.write("\n")
                