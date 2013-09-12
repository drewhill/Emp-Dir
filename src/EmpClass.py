# -*- coding: utf-8 -*-
"""
Created on Thu Jul 04 02:05:45 2013

@author: drewhill
"""

from HierClass import hier
import os

class employee:
    
    def __init__(self,newID,val="temp name"): #constructor
        self.name = val
        self.id = newID
        self.title = ""
        self.workPhone = ""
        self.cellPhone = ""
        self.email = ""
        self.birthday = ""
        self.proj = dict() #dict key = projID, value = [hier]
        self.skills = dict() #key = skillID, value = skill level
        self.interests = dict() #key = skillID, value = skill level
        self.photoLink = ""
        self.notes = ""
        
    def setTitle(self,val=""):
        self.inFile()
        self.title = val
        self.outFile()
        
    def setBday(self,val=""):
        self.inFile()
        self.birthday=val
        self.outFile()
        
    def chgName(self,val):
        if val == "":
            return -1
        self.inFile()
        self.name = val
        self.outFile()
        #change name in emp master list and push it
        from EmpListClass import EmpList
        tEmpList=EmpList()
        tEmpList.inFile()
        tEmpList.renameEmp(self.id,val)

        tEmpList.outFile()      
        
    def setEmail(self,val=""):
        self.inFile()
        self.email = val
        self.outFile()

    def setCell(self,val=""):
        self.inFile()
        self.cellPhone = val
        self.outFile()

    def setWork(self,val=""):
        self.inFile()
        self.workPhone = val
        self.outFile()

    def setPhotoLink(self,val=""):
        self.inFile()
        self.photoLink = val
        self.outFile()

    def setNotes(self,val=""):
        self.inFile()
        self.notes = val
        self.outFile()

    def addInt(self,intID,intLvl): 
        #TODO called from employee after confirming interests exists in master list
        self.inFile()
        from AbilClass import ability
        if not self.interests.has_key(intID):
            self.interests[intID]=intLvl
            tempInt=ability(intID,"TempName","Int")
            tempInt.inFile()
            tempInt.addEmp(self.id,intLvl) #Add to Ability level list
            self.outFile()
            
    def chgIntLvl(self,intID,intLvl):
        self.inFile()
        from AbilClass import ability        
        if self.interests.has_key(intID):
            self.interests[intID]=intLvl
            tempSk=ability(intID,"TempName","Int")
            tempSk.inFile()
            tempSk.chgLvl(self.id,intLvl)
            self.outFile()
        else:
            return -1 #This skill doesn't exist            

    def remInt(self,intID):
        self.inFile()
        from AbilClass import ability
        self.interests.pop(intID)
        tempInt=ability(intID,"temp","Int")
        tempInt.inFile()
        tempInt.remEmp(self.id)
        self.outFile()  

    def addSkill(self,skID,skLvl):
        #TODO called from employee after confirming skill exists in master list
        self.inFile()
        from AbilClass import ability
        if not self.skills.has_key(skID):
            self.skills[skID]=skLvl
            tempSk=ability(skID,"TempName","Skill")
            tempSk.inFile()
            tempSk.addEmp(self.id,skLvl)
            self.outFile()
            
    def chgSkillLvl(self,skID,skLvl):
        self.inFile()
        from AbilClass import ability        
        if self.skills.has_key(skID):
            self.skills[skID]=skLvl
            tempSk=ability(skID,"TempName","Skill")
            tempSk.inFile()
            tempSk.chgLvl(self.id,skLvl)
            self.outFile()
        else:
            return -1 #This skill doesn't exist
            
    def remSkill(self,skID):
        self.inFile()
        from AbilClass import ability
        self.skills.pop(skID)
        tempSk=ability(skID,"temp","Skill")
        tempSk.inFile()
        tempSk.remEmp(self.id)
        self.outFile()
                       
    def addProjSup(self,projID,supID,push = 1):
        self.inFile()
        if self.proj.has_key(projID):
            chg=self.proj[projID].addSup(supID)
            if chg == 1:
                self.outFile()
                if push == 1:
                    #this means yes push forward to emp
                    tempEmp = employee(supID,"")
                    tempEmp.inFile()
                    tempEmp.addProjSub(projID,self.id,0)
            
    def addProjSub(self,projID,subID,push = 1):
        self.inFile()
        if self.proj.has_key(projID):
            chg=self.proj[projID].addSub(subID)
            if chg == 1:
                self.outFile()
                if push == 1:
                    #this means yes push forward to emp
                    tempEmp = employee(subID,"")
                    tempEmp.inFile()
                    tempEmp.addProjSup(projID,self.id,0)
        
    def addProjOrRole(self,projID,role=""):
        self.inFile()        
        chg=0
        if not self.proj.has_key(projID): #if they aren't on project, add them
            tempHier = hier(projID)
            self.proj[projID]=tempHier
            chg=1
            #Add emp to Proj
            from ProjClass import project
            tempProj = project(projID,"")
            tempProj.inFile()
            tempProj.addEmp(self.id)
        if not role == "":
            self.proj[projID].role = role
            chg=1
        if chg==1:
            self.outFile()           
            
            
    def setRole(self,projID,role=""):
        self.inFile()        
        self.proj[projID].role = role
        self.outFile()            
            
    def remProj(self,projID):
        self.inFile()
        if self.proj.has_key(projID):
            tempHier=self.proj.pop(projID)
            self.outFile()
            for sub in tempHier.retSub():
                tempEmp=employee(sub)
                tempEmp.inFile()
                tempEmp.remProjSup(projID,self.id,0)#remove sup from sub, no push
            for sup in tempHier.retSup():
                tempEmp=employee(sup)
                tempEmp.inFile()
                tempEmp.remProjSub(projID,self.id,0)#remove sup from sub, no push
            #remove emp from Proj
            from ProjClass import project
            tempProj = project(projID,"")
            tempProj.inFile()
            tempProj.remEmp(self.id)
            #Have a previous proj/proj History subsection?
            
    def remProjArch(self,projID):
        #Just delete project, don't need to push anything
        self.inFile()
        if self.proj.has_key(projID):
            self.proj.pop(projID)        
        self.outFile()
    
    def remProjSup(self,projID,supID,push=1):
        self.inFile()
        self.proj[projID].remSup(supID)
        self.outFile()
        if push == 1:
            #this means yes push forward to emp
            tempEmp = employee(supID,"")
            tempEmp.inFile()
            tempEmp.remProjSub(projID,self.id,0)
        
    def remProjSub(self,projID,subID,push=1):     
        self.inFile()
        self.proj[projID].remSub(subID)
        self.outFile()
        if push == 1:
            #this means yes push forward to emp
            tempEmp = employee(subID,"")
            tempEmp.inFile()
            tempEmp.remProjSub(projID,self.id,0)    
    
    def retID(self):
        return self.id
        
    def retName(self):
        return self.name
        
    def retBday(self):
        return self.birthday

    def retTitle(self):
        return self.title

    def retWorkPhone(self):
        return self.workPhone

    def retCellPhone(self):
        return self.cellPhone

    def retEmail(self):
        return self.email

    def retProjIDList(self):
        return self.proj.keys()

    def retProjList(self):
        return self.proj.items()
        
    def retProjHier(self,proj):
        return self.proj[proj]
        
    def retProjSup(self,proj):
        return self.proj[proj].retSup()
        
    def retProjSub(self,proj):
        return self.proj[proj].retSub()

    def retProjRole(self,proj):
        return self.proj[proj].retRole()

    def retSkillList(self):
        return self.skills.items()
    
    def retSkillLvl(self,skID):
        return self.skills[skID]

    def retIntList(self):
        return self.interests.items()
    
    def retIntLvl(self,intID):
        return self.interests[intID]

    def retPhotoLink(self):
        return self.photoLink

    def retNotes(self):
        return self.notes
          
    def outFile(self):
        with open(os.path.join(os.getcwd(),"employees",str(self.id)+".emp"),'w+') as f:
            f.write("ID"+"\n")
            f.write(str(self.id)+"\n")
            f.write("Name"+"\n")
            f.write(self.name+"\n")
            f.write("Title"+"\n")
            if not self.title=="":
                f.write(self.title+"\n")
            f.write("Work Phone"+"\n")
            if not self.workPhone=="":
                f.write(self.workPhone+"\n")
            f.write("Cell Phone"+"\n")
            if not self.cellPhone=="":
                f.write(self.cellPhone+"\n")
            f.write("Email"+"\n")
            if not self.email=="":
                f.write(self.email+"\n")
            f.write("Birthday"+"\n")
            if not self.birthday=="":
                f.write(self.birthday+"\n")
            f.write("Photo Link"+"\n")
            if not self.photoLink=="":
                f.write(self.photoLink+"\n")            
            f.write("Notes"+"\n")
            if not self.notes=="":
                tempNotes=self.notes
                tempNotes = "<br>".join(tempNotes.split("\n"))
                tempNotes = "<br>".join(tempNotes.split("\r"))
                f.write(tempNotes+"\n")                        
            f.write("Skills"+"\n")
            for skillID, skillLvl in self.skills.items():
                f.write(str(skillID))
                f.write(":")
                f.write(str(skillLvl))
                f.write("\n")
            f.write("Interests"+"\n")            
            for intID, intLvl in self.interests.items():
                f.write(str(intID))
                f.write(":")
                f.write(str(intLvl))
                f.write("\n")      
            #TODO: Sanitize output for colons and newlines
            f.write("Projects"+"\n")
            for projID,hierCl in self.proj.items():
                f.write("----------\n")
                f.write("Project ID\n")
                f.write(str(projID)+"\n")
                f.write("Role\n")                
                if not hierCl.retRole()=="":
                    f.write(str(hierCl.retRole())+"\n")
                f.write("Superiors\n")
                supList=hierCl.retSup()
                for sup in supList:
                    f.write(str(sup)+"\n")
                f.write("Subords\n")
                subList=hierCl.retSub()
                for sub in subList:
                    f.write(str(sub)+"\n")                
    
    def inFile(self):
        if not os.path.isfile(os.path.join(os.getcwd(),"employees",str(self.id)+".emp")):
            return -1
        with open(os.path.join(os.getcwd(),"employees",str(self.id)+".emp"),'r') as f:
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
            line=line.rstrip("\n") #"Title"            
            line=f.readline()
            line=line.rstrip("\n") #Title      
            if not line=="Work Phone":
                self.title=line            
                line=f.readline()
                line=line.rstrip("\n") #"Work Phone" 
            else:
                self.title=""
            line=f.readline()
            line=line.rstrip("\n") #Work Phone
            if not line=="Cell Phone":
                self.workPhone=line
                line=f.readline()
                line=line.rstrip("\n") #"Cell Phone"
            else:
                self.workPhone=""
            line=f.readline()
            line=line.rstrip("\n") #Cell Phone  
            if not line=="Email":
                self.cellPhone=line
                line=f.readline()
                line=line.rstrip("\n") #"Email"
            else:
                self.cellPhone=""
            line=f.readline()
            line=line.rstrip("\n") #Email  
            if not line=="Birthday":
                self.email=line            
                line=f.readline()
                line=line.rstrip("\n") #"Birthday"
            else:
                self.email=""
            line=f.readline()
            line=line.rstrip("\n") #birthday  
            if not line=="Photo Link":
                self.birthday=line            
                line=f.readline()
                line=line.rstrip("\n") #"Photo Link"
            else:
                self.birthday=""
            line=f.readline()
            line=line.rstrip("\n") #Photo Link  
            if not line=="Notes":
                self.photoLink=line            
                line=f.readline()
                line=line.rstrip("\n") #"Notes"
            else:
                self.photoLink=""
            line=f.readline()
            line=line.rstrip("\n") #Notes  
            if not line=="Skills":
                line = "\n".join(line.split("<br>"))
                self.notes=line       
                line=f.readline()
                line=line.rstrip("\n") #"Skills"
            else:
                self.notes=""
            #current line is Skills                           
            line=f.readline()
            line=line.rstrip("\n") #Skill
            self.skills=dict() #reset it to base empty          
            while not line == "Interests":
                if line.find(":") == -1: #cover for earlier case
                    skID = line
                    skLvl = 1 #default to lowest lvl
                else:
                    skID,skLvl=line.split(":")
                self.skills[int(skID)]=int(skLvl)
                line=f.readline()
                line=line.rstrip("\n")                
            #current line is "Interests"
            self.interests=dict() #reset it
            line=f.readline()
            line=line.rstrip("\n") #Interest          
            while not line == "Projects":
                if line.find(":") == -1:
                    intID = line
                    intLvl = 1 #default to lowest lvl
                else:
                    intID,intLvl=line.split(":")
                self.interests[int(intID)]=int(intLvl)               
                line=f.readline()
                line=line.rstrip("\n")                
            #current line is "Projects"
            self.proj=dict() #reset it to base empty
            line=f.readline()
            line=line.rstrip("\n") #----------
            while not line == "": #not EOF
                #for line in f: #loop until end
                if line == "Project ID":
                    line=f.readline()
                    line=line.rstrip("\n") #Project ID
                    tempHier=hier(int(line))
                    line=f.readline()
                    line=line.rstrip("\n") #"Role"              
                    line=f.readline()
                    line=line.rstrip("\n") #Role or Superiors
                    if not(line == "Superiors"):
                        tempHier.setRole(line)
                        line=f.readline()
                        line=line.rstrip("\n") #"Superiors"
                    line=f.readline()
                    line=line.rstrip("\n") #Superior OR "Subords"
                    
                    while not line == "Subords": #do superiors until hit this
                        tempHier.impSup(int(line))
                        line=f.readline()
                        line=line.rstrip("\n")
                    #at line "Subords"
                    line=f.readline()
                    line=line.rstrip("\n")
                    while not ((line == "----------") | (line == "")): #not hit next hier or EOF
                        tempHier.impSub(int(line))
                        line=f.readline()
                        line=line.rstrip("\n")
                    self.proj[tempHier.retID()]=tempHier
                else:
                    line=f.readline()
                    line=line.rstrip("\n")
                    
