# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 01:07:18 2013

@author: drewhill
"""

from Tkinter import Tk, Label, Button, Frame, Canvas, Grid, Scrollbar, Entry, StringVar, Toplevel, Message
from Tkinter import Text, INSERT, DISABLED, NORMAL, END
from Tkconstants import N,S,W,E,NW,NE,SW,SE,CENTER,TOP,BOTTOM,LEFT,RIGHT,BOTH,Y,X,YES,NO,RAISED,FLAT,GROOVE,SUNKEN,RIDGE,VERTICAL,FALSE,TRUE
from ttk import Style,Combobox
from EmpListClass import EmpList
from ProjListClass import ProjList
from AbilListClass import AbilListClass
from EmpClass import employee
from ProjClass import project
from AbilClass import ability
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import tkFileDialog
import tkMessageBox
from AutoSuggest import AutoSug
from Emailler import mailto
import webbrowser
import datetime

class MainGui(Frame):
  
    def __init__(self, parent):

        Frame.__init__(self, parent) 
        self.parent = parent  

        
        self.parent.title("Stage 2 Contract Engineering")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.iconWidth=20
        self.iconHeight=20

        Grid.rowconfigure(self,0,weight=1)
        Grid.columnconfigure(self,1,weight=1)        
        
        self.sideFr=self.sideMenu() #Put in side menu
        self.sideFr.grid(row=0,column=0,sticky=N+S)
        
        #self.activeFr=self.homeScreen() #Put in active frame
        #self.activeFr.grid(row=0,column=1,sticky=N+S+W+E)
        
        self.scFr=VerticalScrolledFrame(self)      
        self.scFr.grid(row=0,column=1,sticky=N+S+W+E)
        self.scFr.columnconfigure(0,weight=1)
        self.scFr.rowconfigure(0,weight=1)        
        #self.scFr.configure(borderwidth=10,relief=RAISED)
        
        #self.scFr.interior.configure(borderwidth=10,relief=GROOVE)
        self.scFr.interior.columnconfigure(0,weight=1)
        self.scFr.interior.rowconfigure(0,weight=1)
        #self.scFr.interior.grid(sticky=W)
        
        self.rightFr=Frame(self.scFr.interior)
        self.rightFr.grid(row=0,column=1,sticky=N+S+W+E)
        self.rightFr.columnconfigure(0,weight=1)
        self.rightFr.rowconfigure(0,weight=1)
       
        

        self.parent.bind_all("<MouseWheel>", self._on_mousewheel)

        self.initFolders()
        
        self.empList = EmpList()
        self.empList.inFile()
        
        self.projList = ProjList()
        self.projList.inFile()
        
        self.skillList = AbilListClass("Skill")
        self.skillList.inFile()
        
        self.intList = AbilListClass("Int")
        self.intList.inFile()        

        self.activeFr=self.homeScreen()
        self.activeFr.grid(row=0,column=0,sticky=N+S+W+E,padx=(0,8000000)) #Bad form, but can't get it to left align otherwise
        self.rightFr.columnconfigure(0,weight=1)
        self.rightFr.rowconfigure(0,weight=1)
                
        
        #self.initUI()
        
        
    def _on_mousewheel(self, event):
        self.scFr.mwheel(-1*(event.delta/120))
        #self.scFr.yview_scroll(-1*(event.delta/120), "units")        
               
    def initUI(self,screen="Home",val1="",val2="",val3="",val4=""):
      
          
        sideMenuFr=self.sideMenu()
        sideMenuFr.grid(row=0,column=0,sticky=N+S)
        self.activeFr.grid_forget()
        if(screen == "Home"):
            self.activeFr=self.homeScreen()            
        elif(screen == "Employee List"):
            self.activeFr=self.empListScreen()
        elif(screen == "Project List"):
            self.activeFr=self.projListScreen()
        elif(screen == "Skill List"):
            self.activeFr=self.skillListScreen(val1)
        elif(screen == "Interest List"):
            self.activeFr=self.intListScreen(val1)
        elif(screen=="Employee"):
            self.activeFr=self.empScreen(val1)
        elif(screen=="Project"):
            self.activeFr=self.projScreen(val1)      
        elif(screen=="EmpEdit"):
            self.activeFr=self.empEdit(val1,val2,val3)
        elif(screen=="Confirm EmpStuff Del"):
            self.activeFr=self.confirmEmpStuffDel(val1,val2,val3,val4)
        elif(screen=="Email"):
            self.activeFr=self.empEdit(val1,val2,val3)
        elif(screen=="Work Phone"):
            self.activeFr=self.empEdit(val1,val2,val3)
        elif(screen=="Cell Phone"):
            self.activeFr=self.empEdit(val1,val2,val3)
        elif(screen=="SkillLvl"):
            self.activeFr=self.empAbilEdit("Skill",val1,val2,val3)
        elif(screen=="IntLvl"):
            self.activeFr=self.empAbilEdit("Int",val1,val2,val3)
        elif(screen=="Employee Skill"):
            self.activeFr=self.empAbilAdd("Skill",val1)
        elif(screen=="Employee Interest"):
            self.activeFr=self.empAbilAdd("Int",val1) 
        elif(screen=="Employee Notes"):
            self.activeFr=self.empEditNotes(val1)            
        elif(screen=="Add Skill"):
            self.activeFr=self.newAbil("Skill",val1,val2)
        elif(screen=="Add Interest"):
            self.activeFr=self.newAbil("Int",val1,val2)  
        elif(screen=="Add Proj Hier"):
            self.activeFr=self.addHier(val1,val2,val3)
        elif(screen=="EmpProjEdit"):
            self.activeFr=self.empProjEdit(val1,val2,val3)
        elif(screen=="Confirm EmpProj Del"):
            self.activeFr=self.empProjDel(val1,val2)   
        elif(screen=="Add New Project"):
            self.activeFr=self.empProjAdd(val1)             
        elif(screen=="Create Project"):
            self.activeFr=self.createProj(val1)             
        elif(screen=="ProjEmpEdit"):
            self.activeFr=self.projEmpEdit(val1,val2,val3)
        elif(screen=="Confirm ProjEmp Del"):
            self.activeFr=self.projEmpDel(val1,val2)  
        elif(screen=="Add Emp to Project"):
            self.activeFr=self.projEmpAdd(val1)
        elif(screen=="Create Employee"):
            self.activeFr=self.createEmp(val1)                  
        elif(screen=="ProjNameEdit"):
            self.activeFr=self.projNameEdit(val1,val2)
        elif(screen=="ProjLeadEdit"):
            self.activeFr=self.projLeadEdit(val1,val2)
        elif(screen=="Project Description"):
            self.activeFr=self.projEditDesc(val1)               
        elif(screen=="Confirm ProjStuff Del"):
            self.activeFr=self.confirmProjStuffDel(val1,val2,val3,val4)
        elif(screen=="AddEmpToInt"):
        	self.activeFr=self.addEmpToInt(val1)
        elif(screen=="CreateNewInt"):
        	self.activeFr=self.createNewInt()
        elif(screen=="DeleteInt"):
        	self.activeFr=self.deleteInt(val1)
        elif(screen=="EditEmpInt"):
        	self.activeFr=self.editEmpInt(val1,val2)
        elif(screen=="DelEmpInt"):
        	self.activeFr=self.delEmpInt(val1,val2)            
        elif(screen=="RenameInt"):
        	self.activeFr=self.renameInt(val1)          
        elif(screen=="AddEmpToSkill"):
        	self.activeFr=self.addEmpToSkill(val1)
        elif(screen=="CreateNewSkill"):
        	self.activeFr=self.createNewSkill()
        elif(screen=="DeleteSkill"):
        	self.activeFr=self.deleteSkill(val1)
        elif(screen=="EditEmpSkill"):
        	self.activeFr=self.editEmpSkill(val1,val2)
        elif(screen=="DelEmpSkill"):
        	self.activeFr=self.delEmpSkill(val1,val2)
        elif(screen=="RenameSkill"):
        	self.activeFr=self.renameSkill(val1)              
        elif(screen=="ProjShareSet"):
        	self.activeFr=self.projShareSet(val1)
        elif(screen=="Confirm Share Del"):
        	self.activeFr=self.confShareDel(val1)   
        elif(screen=="DeleteEmployee"):
        	self.activeFr=self.deleteEmployee(val1)
        elif(screen=="DeleteProject"):
        	self.activeFr=self.deleteProject(val1)         
            
        self.activeFr.columnconfigure(0,weight=1)
        self.activeFr.rowconfigure(0,weight=1)        
        self.activeFr.grid(row=0,column=1,sticky=N+S+W+E,padx=(0,8000000))#Bad form, but can't get it to left align otherwise
        self.scFr.scrollTop()
        
    def initFolders(self):
        #Make sure on startup that folders exist. If not, create them. 
        if not os.path.exists(os.path.join(os.getcwd(),"ProjArchive")):
            os.mkdir(os.path.join(os.getcwd(),"ProjArchive"))
        if not os.path.exists(os.path.join(os.getcwd(),"EmpArchive")):
            os.mkdir(os.path.join(os.getcwd(),"EmpArchive"))
        if not os.path.exists(os.path.join(os.getcwd(),"EmpList")):
            os.mkdir(os.path.join(os.getcwd(),"EmpList"))
        if not os.path.exists(os.path.join(os.getcwd(),"employees")):
            os.mkdir(os.path.join(os.getcwd(),"employees"))
        if not os.path.exists(os.path.join(os.getcwd(),"projects")):
            os.mkdir(os.path.join(os.getcwd(),"projects"))
        if not os.path.exists(os.path.join(os.getcwd(),"ProjectList")):
            os.mkdir(os.path.join(os.getcwd(),"ProjectList"))
        if not os.path.exists(os.path.join(os.getcwd(),"Skill")):
            os.mkdir(os.path.join(os.getcwd(),"Skill"))
        if not os.path.exists(os.path.join(os.getcwd(),"Int")):
            os.mkdir(os.path.join(os.getcwd(),"Int"))  
        if not os.path.exists(os.path.join(os.getcwd(),"img")):
            self.parent.withdraw()
            #self.parent.event_generate("WM_DELETE_WINDOW") 
            errMsg = Toplevel()
            errMsg.lift()
            errMsg.title("Missing folder")
            about_message = 'The "img" folder is missing. Please restore the img folder to use this program'
            msg = Message(errMsg, text=about_message)
            msg.pack()
            
            button = Button(errMsg, text="OK", command=lambda errMsg=errMsg: self.errMsgCallback(errMsg))
            button.pack()        
        
        
    def errMsgCallback(self,topLvl):
        topLvl.destroy()
        self.parent.eval('::ttk::CancelRepeat')
        self.parent.destroy()
        
        
        
    def initPage(self):
        self.parent.title("Employee Directory")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        Grid.rowconfigure(self,0,weight=1)
        Grid.columnconfigure(self,1,weight=1) #fit anything else in the 2nd column spot
        sideMenuFr=self.sideMenu()
        sideMenuFr.grid(row=0,column=0,sticky=N+S)

    def sideMenu(self):
        separator = Frame(self, width=30, relief=RAISED, borderwidth=3)
        separator.rowconfigure(0,weight=1)
        separator.rowconfigure(1,weight=1)
        separator.rowconfigure(2,weight=1)
        separator.rowconfigure(3,weight=1)
        
        btnFont=("Helvetica",12, "bold")
        
        EmpList = Button(separator,width=25, text="Employee List", relief=RAISED, borderwidth=5, 
                         font=btnFont, command= lambda: self.initUI("Employee List"))
        EmpList.grid(column=0, row=0, sticky=N+S+E+W) 
        
        ProjList = Button(separator, text="Project List", relief=RAISED, borderwidth=5, font=btnFont, 
                          command= lambda: self.initUI("Project List"))
        ProjList.grid(column=0, row=1, sticky=N+S+E+W)
        
        SkList = Button(separator, text="Skill List", relief=RAISED, borderwidth=5, font=btnFont, 
                        command= lambda: self.initUI("Skill List"))
        SkList.grid(column=0, row=2, sticky=N+S+E+W)

        IntList = Button(separator, text="Interest List", relief=RAISED, borderwidth=5, font=btnFont, 
                         command= lambda: self.initUI("Interest List"))
        IntList.grid(column=0, row=3, sticky=N+S+E+W)   

        return separator       

    def homeScreen(self):
        activeFr = Frame(self.rightFr)
        #activeFr.columnconfigure(0,weight=1)
        #activeFr.rowconfigure(0,weight=1)
        companyName = "Employee Directory"
        mainFont=("Helvetica",16,"bold")
        mainLabel = Label(activeFr, text = (companyName+" Employee Directory"), anchor=CENTER, font=mainFont)
        mainLabel.grid(row=0,column=0, sticky=N+S+W+E)
        mainLabel.rowconfigure(0,weight=1)
        mainLabel.columnconfigure(0,weight=1)
        bdayList = self.bdays()
        if not bdayList==[]:
            bdayLabel = Label(activeFr,text = "Birthdays Today")
            bdayLabel.grid(row=1,column=0,sticky=N+S+W+E)
            nameList=""
            for empName in bdayList:
                if not nameList=="":
                    nameList=nameList+", "+empName
                else:
                    nameList=empName
            nameListLabel = Label(activeFr,text=nameList)
            nameListLabel.grid(row=2,column=0,sticky=N+S+W+E)
            
            
        return activeFr
        
    def bdays(self):
        now = datetime.datetime.now()
        curMon = str(now.month)
        curDay = str(now.day)
        if(len(curMon)==1): #turn m to mm
            curMon="0"+curMon
        if(len(curDay)==1): #turn d to dd
            curDay="0"+curDay

        bdayList = []

        for empID,empName in sorted(self.empList.empList.items(), 
                                    key=lambda x:x[1].lower()):
            tempEmp = employee(empID)
            tempEmp.inFile()
            bday = tempEmp.retBday()
            bday=bday.split("/")
            if(len(bday)>1):#if more than 1 split, assume we have month/day
                mon=bday[0]
                day=bday[1]
                if(len(mon)==1): #turn m to mm
                    mon="0"+mon
                if(len(day)==1): #turn d to dd
                    day="0"+day
                if(mon == curMon): #TODO:eventually add upcoming birthdays
                    if(day==curDay):
                        bdayList.append(empName)
        
        return bdayList
        
        
################################################################################################
###########################HINT:Employee List Screen############################################        
################################################################################################          
        
    def empListScreen(self):        
        
        
        iconWidth=self.iconWidth
        iconHeight=self.iconHeight

        
        self.empList.inFile()
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1) 
        curRow=0
        titleFont=("Helvetica",16,"bold")
        titleLabel = Label(activeFr,text="Employee List",font=titleFont)
        titleLabel.grid(column=0,row=0, sticky=N)
        empListFont=("Helvetica",10)
        bList = dict()
        
        for empID,empName in sorted(self.empList.empList.items(), 
                                    key=lambda x:x[1].lower()):
            curRow+=1
            bList[curRow]=empID
            empButton=Button(activeFr,text=empName, font=empListFont, 
                             command= lambda empID=empID: self.initUI("Employee",empID))
            empButton.grid(column=0,row=curRow, sticky=N)    
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(activeFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda empID=empID: self.initUI("DeleteEmployee",empID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=1,row=curRow,sticky=W+E)                                

        curRow+=1

        tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
        tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
        tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
        nmAddBut=Button(activeFr,image=tempAddImgTk,relief=FLAT,
                        command=lambda:self.initUI("Create Employee"))
        nmAddBut.image=tempAddImgTk
        nmAddBut.grid(column=1,row=curRow,sticky=W+E)                      
        
        return activeFr     
        
    def deleteEmployee(self,empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you sure you want to delete the employee "'+
                    str(self.empList.retName(int(empID)))+'"?')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        titleLb2=Label(activeFr,text='This action CANNOT be undone.')
        titleLb2.grid(column=0,row=1,sticky=W+E,columnspan=2)             

        okBut=Button(activeFr,text="OK",
                     command=lambda empID=empID: self.deleteEmployeeCallback(empID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Employee List"))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr           
        
    def deleteEmployeeCallback(self,empID):
        self.empList.remEmp(empID)
        self.initUI("Employee List")
        return 1                
        
################################################################################################
###########################HINT:Project List Screen#############################################        
################################################################################################          
        
        
    def projListScreen(self): 
                
        iconWidth=self.iconWidth
        iconHeight=self.iconHeight

        
        self.projList.inFile()
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1) 
        curRow=0
        titleFont=("Helvetica",16,"bold")
        titleLabel = Label(activeFr,text="Project List",font=titleFont)
        titleLabel.grid(column=0,row=0, sticky=N)
        projListFont=("Helvetica",10)
        for projID,projName in sorted(self.projList.projList.items(),
                                      key=lambda x:x[1].lower()):
            curRow+=1
            projButton=Button(activeFr,text=projName, font=projListFont,
                              command= lambda projID=projID: self.initUI("Project",projID))
            projButton.grid(column=0,row=curRow, sticky=N)      

            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(activeFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda projID=projID: self.initUI("DeleteProject",projID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=1,row=curRow,sticky=W+E)            

        curRow+=1

        tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
        tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
        tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
        nmAddBut=Button(activeFr,image=tempAddImgTk,relief=FLAT,
                        command=lambda:self.initUI("Create Project"))
        nmAddBut.image=tempAddImgTk
        nmAddBut.grid(column=1,row=curRow,sticky=W+E)                                        
        
        return activeFr   
     
    def deleteProject(self,projID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you sure you want to delete the project "'+
                    str(self.projList.retName(int(projID)))+'"?')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        titleLb2=Label(activeFr,text='This action CANNOT be undone.')
        titleLb2.grid(column=0,row=1,sticky=W+E,columnspan=2)             

        okBut=Button(activeFr,text="OK",
                     command=lambda projID=projID: self.deleteProjectCallback(projID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda projID=projID: self.initUI("Project List"))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr           
        
    def deleteProjectCallback(self,projID):
        self.projList.remProj(projID)
        self.initUI("Project List")
        return 1        

        
        
################################################################################################
###########################HINT:Skill List Screen###############################################        
################################################################################################          
        

    def skillListScreen(self,expand=""): 
        iconWidth=self.iconWidth
        iconHeight=self.iconHeight        
        
        
        self.skillList.inFile()
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1) 
        curRow=0
        titleFont=("Helvetica",16,"bold")
        titleLabel = Label(activeFr,text="Skill List",font=titleFont)
        titleLabel.grid(column=0,row=0, sticky=N)
        skillListFont=("Helvetica",10)
        for skID,skillName in sorted(self.skillList.abilList.items(),
                                     key=lambda x:x[1].lower()):
            curRow+=1
            if(expand==skID):
                skillButton=Button(activeFr,text=skillName, font=skillListFont, 
                                 command=lambda skID=skID: self.initUI("Skill List",skID))
                skillButton.grid(column=0,row=curRow, sticky=N)
                
                tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
                tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
                tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
                nmEditBut=Button(activeFr,image=tempEditImgTk,relief=FLAT,
                                 command=lambda skID=skID:self.initUI("RenameSkill",skID))
                nmEditBut.image=tempEditImgTk
                nmEditBut.grid(column=1,row=curRow,sticky=W+E)
                
                tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
                tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
                tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
                nmDelBut=Button(activeFr,image=tempDelImgTk,relief=FLAT,
                                command = lambda skID=skID: self.initUI("DeleteSkill",skID))
                nmDelBut.image=tempDelImgTk
                nmDelBut.grid(column=2,row=curRow,sticky=W+E)                    
            
                
                curRow+=1
                expFr=Frame(activeFr,relief=RIDGE,borderwidth=4)
                expAbil=ability(skID,"","Skill")
                expAbil.inFile()
                empRow=1
                tempFrNm=Label(expFr,text="Employee",relief=RIDGE,borderwidth=4)
                tempFrNm.grid(column=0,row=0,sticky=N+S+W+E)
                tempFrLvl=Label(expFr,text="Level",relief=RIDGE,borderwidth=4)
                tempFrLvl.grid(column=1,row=0)                
                for empID,empLvl in expAbil.empList.items():
                    empIDBut=Button(expFr,text=self.empList.retName(empID),
                                    command= lambda empID=empID: self.initUI("Employee",empID))
                    empIDBut.grid(column=0,row=empRow,sticky=N+S+W+E)
                    tempSkillLvlFr = self.abilLvl(empLvl,expFr)
                    tempSkillLvlFr.grid(column=1, row=empRow,sticky=N+S+W+E)
                    
                    tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
                    tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
                    tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
                    nmEditBut=Button(expFr,image=tempEditImgTk,relief=FLAT,
                                     command=lambda skID=skID, empID=empID:self.initUI("EditEmpSkill",skID,empID))
                    nmEditBut.image=tempEditImgTk
                    nmEditBut.grid(column=2,row=empRow,sticky=W+E)
                    
                    tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
                    tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
                    tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
                    nmDelBut=Button(expFr,image=tempDelImgTk,relief=FLAT,
                                    command = lambda skID=skID, empID=empID: self.initUI("DelEmpSkill",skID,empID))
                    nmDelBut.image=tempDelImgTk
                    nmDelBut.grid(column=3,row=empRow,sticky=W+E)                           
                    
                    
                    
                    empRow+=1
                
                tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
                tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
                tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
                nmAddBut=Button(expFr,image=tempAddImgTk,relief=FLAT,
                                command=lambda skID=skID:self.initUI("AddEmpToSkill",skID))
                nmAddBut.image=tempAddImgTk
                nmAddBut.grid(column=1,row=0,sticky=W+E)                                        
                
                
                expFr.grid(column=0,row=curRow,sticky=N)
            else:
                skillButton=Button(activeFr,text=skillName, font=skillListFont, 
                                 command=lambda skID=skID: self.initUI("Skill List",skID))
                skillButton.grid(column=0,row=curRow, sticky=N)
                
        tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
        tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
        tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
        nmAddBut=Button(activeFr,image=tempAddImgTk,relief=FLAT,
                        command=lambda:self.initUI("CreateNewSkill"))
        nmAddBut.image=tempAddImgTk
        nmAddBut.grid(column=0,row=(curRow+1),sticky=W+E)  
        return activeFr
        
    def addEmpToSkill(self,skID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text="Add new employee to "+str(self.skillList.retName(int(skID))))
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)


        nameLbl=Label(activeFr,text="Employee Name")
        nameLbl.grid(column=0,row=1,sticky=W)
        
        lvlLbl=Label(activeFr,text="Level")
        lvlLbl.grid(column=1,row=1,sticky=W+E,columnspan=2)        


        tempSkill=ability(skID,"","Skill")
        tempSkill.inFile()

        empVals = self.empList.retListItems()
        if not empVals == []:
            empID,empName=zip(*empVals) #unpack skillo lists
        else:
            empID=""
            empName=""
        if not tempSkill.empList.values() ==[]:
            empskID,empSkillLvl=zip(*tempSkill.empList.items())
        else:
            empskID=""

        revDict=dict(zip(empName,empID))
        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        
        empName=list(empName)
        empID=list(empID) #convert from tuple to list so it is mutable

        for curEmp in empskID:
            if curEmp in empID:
                #don't list emps already on skill
                empName.remove(self.empList.retName(curEmp)) 
                empID.remove(curEmp)

        empName=tuple(empName)
        empID=tuple(empID)

        if not empName == "":
            box['values'] = empName
            box.grid(column=0,row=2,sticky=W+E)

        self.v2=StringVar()
        box = Combobox(activeFr, textvariable=self.v2)
        box['values'] = (0,1,2,3,4)
        box.grid(column=1,row=2,sticky=W+E,columnspan=2)
        box.set(0)

#        if(kind=="Skill"):
#            expl=Label(activeFr,text="Legend:\n"+"0 - no knowledge of task\n"+
#                                "1 - exposed to the task\n"+"2 - can only perform task with assistance\n"+
#                                "3 - can perform task without assistance\n"+"4 - can train others")
    
        expl=Label(activeFr,text="Legend:\n"+"0 - no skill\n"+
                            "1 - light skill\n"+"2 - medium skill\n"+
                            "3 - strong skill\n"+"4 - obsessed")
        expl.grid(column=0,row=4,sticky=W+E,columnspan=2)                

        okBut=Button(activeFr,text="OK",
                     command=lambda skID=skID: self.addEmpToSkillCallback(skID,revDict))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda skID=skID: self.initUI("Skill List",skID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr         
        
        
    def addEmpToSkillCallback(self,skID,revDict):
        empNm=self.v.get()
        empLvl=self.v2.get()
        empID=revDict[empNm]
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.addSkill(skID,int(empLvl))

        self.initUI("Skill List",skID)
        return 1
        
    def createNewSkill(self):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Create a new skill.')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
         
         
         
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        
        trEv=0

        fn="lambda trEv=trEv, self=self: self.createNewSkillCallback()"
        rtnfn='lambda trEv=trEv, self=self: self.initUI("Skill List")'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn)) #this isn't working, fix this
        valEntry.bind('<Escape>',eval(rtnfn))        
             
        return activeFr
        
    def createNewSkillCallback(self):
        skillNm=self.v.get()
        if not self.skillList.abilExist(skillNm):#If it doesn't already exist, add it
            self.skillList.addAbil(skillNm)
        self.initUI("Skill List")
        return 1
                
    def deleteSkill(self,skID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you sure you want to delete the skill "'+
                    str(self.skillList.retName(int(skID)))+'"?')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        titleLb2=Label(activeFr,text='This action CANNOT be undone.')
        titleLb2.grid(column=0,row=1,sticky=W+E,columnspan=2)             

        okBut=Button(activeFr,text="OK",
                     command=lambda skID=skID: self.deleteSkillCallback(skID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda skID=skID: self.initUI("Skill List",skID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr           
        
    def deleteSkillCallback(self,skID):
        self.skillList.remAbil(skID)
        self.initUI("Skill List")
        return 1        
        
    def editEmpSkill(self,skID,empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Set the skill level in '+self.skillList.retName(skID)+' for '+
                                self.empList.retName(empID)+' to ')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        box['values'] = (0,1,2,3,4)
        box.grid(column=0,row=1,sticky=W+E,columnspan=2)
        box.set(0)

#        if(kind=="Skill"):
#            expl=Label(activeFr,text="Legend:\n"+"0 - no knowledge of task\n"+
#                                "1 - exposed to the task\n"+"2 - can only perform task with assistance\n"+
#                                "3 - can perform task without assistance\n"+"4 - can train others")
    
        expl=Label(activeFr,text="Legend:\n"+"0 - no skill\n"+
                            "1 - light skill\n"+"2 - medium skill\n"+
                            "3 - strong skill\n"+"4 - obsessed")
        expl.grid(column=0,row=4,sticky=W+E,columnspan=2)                

        okBut=Button(activeFr,text="OK",
                     command=lambda skID=skID, empID=empID: self.editEmpSkillCallback(skID,empID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda skID=skID: self.initUI("Skill List",skID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr   
        
    def editEmpSkillCallback(self,skID,empID):
        empLvl=self.v.get()
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.chgSkillLvl(skID,int(empLvl))
        self.initUI("Skill List",skID)
        return 1        
        
    def delEmpSkill(self,skID,empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you sure you want to delete the employee '+self.empList.retName(empID)+
                            ' from the skill "'+str(self.skillList.retName(int(skID)))+'"?')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        okBut=Button(activeFr,text="OK",
                     command=lambda skID=skID,empID=empID: self.delEmpSkillCallback(skID,empID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda skID=skID: self.initUI("Skill List",skID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)
        return activeFr
        
    def delEmpSkillCallback(self,skID,empID):
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.remSkill(skID)
        self.initUI("Skill List",skID)
        return 1        
        
    def renameSkill(self,skID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Rename the skill "'+self.skillList.retName(skID)+'" to ')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        
        trEv=0

        fn="lambda trEv=trEv, self=self, skID=skID: self.renameSkillCallback(skID)"
        rtnfn='lambda trEv=trEv, self=self, skID=skID: self.initUI("Skill List", skID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn)) #this isn't working, fix this
        valEntry.bind('<Escape>',eval(rtnfn))        
             
        return activeFr
        
    def renameSkillCallback(self,skID):
        skillNm=self.v.get()
        if not self.skillList.abilExist(skillNm):#If it doesn't already exist, add it
            self.skillList.renameAbil(skID,skillNm)
        self.initUI("Skill List",skID)        
        return 1        


################################################################################################
###########################HINT:Interest List Screen############################################        
################################################################################################  


    def intListScreen(self,expand=""): 
        iconWidth=self.iconWidth
        iconHeight=self.iconHeight        
        
        
        self.intList.inFile()
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1) 
        curRow=0
        titleFont=("Helvetica",16,"bold")
        titleLabel = Label(activeFr,text="Interest List",font=titleFont)
        titleLabel.grid(column=0,row=0, sticky=N)
        intListFont=("Helvetica",10)
        for intID,intName in sorted(self.intList.abilList.items(),
                                    key=lambda x:x[1].lower()):
            curRow+=1
            if(expand==intID):
                intButton=Button(activeFr,text=intName, font=intListFont, 
                                 command=lambda intID=intID: self.initUI("Interest List",intID))
                intButton.grid(column=0,row=curRow, sticky=N)
                
                tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
                tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
                tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
                nmEditBut=Button(activeFr,image=tempEditImgTk,relief=FLAT,
                                 command=lambda intID=intID:self.initUI("RenameInt",intID))
                nmEditBut.image=tempEditImgTk
                nmEditBut.grid(column=1,row=curRow,sticky=W+E)
                
                tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
                tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
                tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
                nmDelBut=Button(activeFr,image=tempDelImgTk,relief=FLAT,
                                command = lambda intID=intID: self.initUI("DeleteInt",intID))
                nmDelBut.image=tempDelImgTk
                nmDelBut.grid(column=2,row=curRow,sticky=W+E)                    
            
                
                curRow+=1
                expFr=Frame(activeFr,relief=RIDGE,borderwidth=4)
                expAbil=ability(intID,"","Int")
                expAbil.inFile()
                empRow=1
                tempFrNm=Label(expFr,text="Employee",relief=RIDGE,borderwidth=4)
                tempFrNm.grid(column=0,row=0,sticky=N+S+W+E)
                tempFrLvl=Label(expFr,text="Level",relief=RIDGE,borderwidth=4)
                tempFrLvl.grid(column=1,row=0)                
                for empID,empLvl in expAbil.empList.items():
                    empIDBut=Button(expFr,text=self.empList.retName(empID),
                                    command= lambda empID=empID: self.initUI("Employee",empID))
                    empIDBut.grid(column=0,row=empRow,sticky=N+S+W+E)
                    tempIntLvlFr = self.abilLvl(empLvl,expFr)
                    tempIntLvlFr.grid(column=1, row=empRow,sticky=N+S+W+E)
                    
                    tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
                    tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
                    tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
                    nmEditBut=Button(expFr,image=tempEditImgTk,relief=FLAT,
                                     command=lambda intID=intID, empID=empID:self.initUI("EditEmpInt",intID,empID))
                    nmEditBut.image=tempEditImgTk
                    nmEditBut.grid(column=2,row=empRow,sticky=W+E)
                    
                    tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
                    tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
                    tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
                    nmDelBut=Button(expFr,image=tempDelImgTk,relief=FLAT,
                                    command = lambda intID=intID, empID=empID: self.initUI("DelEmpInt",intID,empID))
                    nmDelBut.image=tempDelImgTk
                    nmDelBut.grid(column=3,row=empRow,sticky=W+E)                           
                    
                    
                    
                    empRow+=1
                
                tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
                tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
                tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
                nmAddBut=Button(expFr,image=tempAddImgTk,relief=FLAT,
                                command=lambda intID=intID:self.initUI("AddEmpToInt",intID))
                nmAddBut.image=tempAddImgTk
                nmAddBut.grid(column=1,row=0,sticky=W+E)                                        
                
                
                expFr.grid(column=0,row=curRow,sticky=N)
            else:
                intButton=Button(activeFr,text=intName, font=intListFont, 
                                 command=lambda intID=intID: self.initUI("Interest List",intID))
                intButton.grid(column=0,row=curRow, sticky=N)
                
        tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
        tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
        tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
        nmAddBut=Button(activeFr,image=tempAddImgTk,relief=FLAT,
                        command=lambda:self.initUI("CreateNewInt"))
        nmAddBut.image=tempAddImgTk
        nmAddBut.grid(column=0,row=(curRow+1),sticky=W+E)  
        return activeFr
        
    def addEmpToInt(self,intID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text="Add new employee to "+str(self.intList.retName(int(intID))))
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)


        nameLbl=Label(activeFr,text="Employee Name")
        nameLbl.grid(column=0,row=1,sticky=W)
        
        lvlLbl=Label(activeFr,text="Level")
        lvlLbl.grid(column=1,row=1,sticky=W+E,columnspan=2)        


        tempInt=ability(intID,"","Int")
        tempInt.inFile()

        empVals = self.empList.retListItems()
        empID,empName=zip(*empVals) #unpack into lists
        if not tempInt.empList.values() ==[]:
            empIntID,empIntLvl=zip(*tempInt.empList.items())
        else:
            empIntID=""

        revDict=dict(zip(empName,empID))
        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        
        empName=list(empName)
        empID=list(empID) #convert from tuple to list so it is mutable

        for curEmp in empIntID:
            if curEmp in empID:
                #don't list emps already on interest
                empName.remove(self.empList.retName(curEmp)) 
                empID.remove(curEmp)

        empName=tuple(empName)
        empID=tuple(empID)

        box['values'] = empName
        box.grid(column=0,row=2,sticky=W+E)

        self.v2=StringVar()
        box = Combobox(activeFr, textvariable=self.v2)
        box['values'] = (0,1,2,3,4)
        box.grid(column=1,row=2,sticky=W+E,columnspan=2)
        box.set(0)

#        if(kind=="Skill"):
#            expl=Label(activeFr,text="Legend:\n"+"0 - no knowledge of task\n"+
#                                "1 - exposed to the task\n"+"2 - can only perform task with assistance\n"+
#                                "3 - can perform task without assistance\n"+"4 - can train others")
    
        expl=Label(activeFr,text="Legend:\n"+"0 - no interest\n"+
                            "1 - light interest\n"+"2 - medium interest\n"+
                            "3 - strong interest\n"+"4 - obsessed")
        expl.grid(column=0,row=4,sticky=W+E,columnspan=2)                

        okBut=Button(activeFr,text="OK",
                     command=lambda intID=intID: self.addEmpToIntCallback(intID,revDict))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda intID=intID: self.initUI("Interest List",intID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr         
        
        
    def addEmpToIntCallback(self,intID,revDict):
        empNm=self.v.get()
        empLvl=self.v2.get()
        empID=revDict[empNm]
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.addInt(intID,int(empLvl))

        self.initUI("Interest List",intID)
        return 1
        
    def createNewInt(self):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Create a new interest.')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
         
         
         
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        
        trEv=0

        fn="lambda trEv=trEv, self=self: self.createNewIntCallback()"
        rtnfn='lambda trEv=trEv, self=self: self.initUI("Interest List")'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn)) #this isn't working, fix this
        valEntry.bind('<Escape>',eval(rtnfn))        
             
        return activeFr
        
    def createNewIntCallback(self):
        intNm=self.v.get()
        if not self.intList.abilExist(intNm):#If it doesn't already exist, add it
            self.intList.addAbil(intNm)
        self.initUI("Interest List")
        return 1
                
    def deleteInt(self,intID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you sure you want to delete the interest "'+
                    str(self.intList.retName(int(intID)))+'"?')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        titleLb2=Label(activeFr,text='This action CANNOT be undone.')
        titleLb2.grid(column=0,row=1,sticky=W+E,columnspan=2)             

        okBut=Button(activeFr,text="OK",
                     command=lambda intID=intID: self.deleteIntCallback(intID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda intID=intID: self.initUI("Interest List",intID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr           
        
    def deleteIntCallback(self,intID):
        self.intList.remAbil(intID)
        self.initUI("Interest List")
        return 1        
        
    def editEmpInt(self,intID,empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Set the interest level in '+self.intList.retName(intID)+' for '+
                                self.empList.retName(empID)+' to ')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        box['values'] = (0,1,2,3,4)
        box.grid(column=0,row=1,sticky=W+E,columnspan=2)
        box.set(0)

#        if(kind=="Skill"):
#            expl=Label(activeFr,text="Legend:\n"+"0 - no knowledge of task\n"+
#                                "1 - exposed to the task\n"+"2 - can only perform task with assistance\n"+
#                                "3 - can perform task without assistance\n"+"4 - can train others")
    
        expl=Label(activeFr,text="Legend:\n"+"0 - no interest\n"+
                            "1 - light interest\n"+"2 - medium interest\n"+
                            "3 - strong interest\n"+"4 - obsessed")
        expl.grid(column=0,row=4,sticky=W+E,columnspan=2)                

        okBut=Button(activeFr,text="OK",
                     command=lambda intID=intID, empID=empID: self.editEmpIntCallback(intID,empID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda intID=intID: self.initUI("Interest List",intID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr   
        
    def editEmpIntCallback(self,intID,empID):
        empLvl=self.v.get()
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.chgIntLvl(intID,int(empLvl))
        self.initUI("Interest List",intID)
        return 1        
        
    def delEmpInt(self,intID,empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you sure you want to delete the employee '+self.empList.retName(empID)+
                            ' from the interest "'+str(self.intList.retName(int(intID)))+'"?')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        okBut=Button(activeFr,text="OK",
                     command=lambda intID=intID,empID=empID: self.delEmpIntCallback(intID,empID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda intID=intID: self.initUI("Interest List",intID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)
        return activeFr
        
    def delEmpIntCallback(self,intID,empID):
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.remInt(intID)
        self.initUI("Interest List",intID)
        return 1        
        
    def renameInt(self,intID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Rename the interest "'+self.intList.retName(intID)+'" to ')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        
        trEv=0

        fn="lambda trEv=trEv, self=self, intID=intID: self.renameIntCallback(intID)"
        rtnfn='lambda trEv=trEv, self=self, intID=intID: self.initUI("Interest List", intID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn)) #this isn't working, fix this
        valEntry.bind('<Escape>',eval(rtnfn))        
             
        return activeFr
        
    def renameIntCallback(self,intID):
        intNm=self.v.get()
        if not self.intList.abilExist(intNm):#If it doesn't already exist, add it
            self.intList.renameAbil(intID,intNm)
        self.initUI("Interest List",intID)        
        return 1        


################################################################################################
###########################HINT:Project Screen##################################################        
################################################################################################  

        
    def projScreen(self,projID):
        #Frame lists, from top to bottom
        #Project Name, edit
        #Group 1:
        #   Left - photo
        #   Right - Lead, edit
        #   Right - Email team button
        #   Right - Sharepoint Link
        #   Right - Description, edit
        #List of all employees + roles, delete/edit
        #Add employee   
        #TODO: Add Org Chart, dynamically generated
        
        
        
        maxImgHeight = 300
        maxImgWidth = 300
        
        iconWidth=self.iconWidth
        iconHeight=self.iconHeight

        proj=project(projID,"")        
        proj.inFile()
        
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)   
        tempLbl=Label(activeFr,text="proj: "+str(projID))
        tempLbl.grid(column=0,row=0)


        ##### NAME FRAME #####        
        nameFr = Frame(activeFr)
        nameFr.grid(column=0,row=0,sticky=N+S+W+E)
        nameFr.rowconfigure(0,weight=1)
        projNameFont=("Helvetica",16,"bold")
        projNameLabel = Label(nameFr,text=self.projList.retName(projID),font=projNameFont)
        projNameLabel.grid(column=0,row=0, sticky=N+S+W+E)
        
        tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
        tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
        tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
        nmEditBut=Button(nameFr,image=tempEditImgTk,relief=FLAT,
                         command=lambda:self.initUI("ProjNameEdit",projID,self.projList.retName(projID)))
        nmEditBut.image=tempEditImgTk
        nmEditBut.grid(column=1,row=0,sticky=W+E)
        ##### NAME FRAME #####        
        

        groupOneFr = Frame(activeFr)
        #Photo, title, email, work num, cell num
        
        groupOneFr.grid(column=0,row=1,sticky=N+S+W+E)    
        
        groupOneLeft = Frame(groupOneFr)
        groupOneLeft.grid(column=0,row=0,sticky=N+S+W+E)  
        
        groupOneRight = Frame(groupOneFr)
        groupOneRight.grid(column=1,row=0,sticky=N+S+W+E)        
                
        ##### PHOTO FRAME #####        
        photoFr=Frame(groupOneLeft)
        photoLink=proj.retPhotoLink()
        if not photoLink=="":
            tempIm = Image.open(photoLink)
            (width, height) = tempIm.size
            if height > maxImgHeight:
                width = (width*maxImgHeight)/height
                height = maxImgHeight
            if width > maxImgWidth:
                height = (height*maxImgWidth)/width
                width = maxImgWidth
            tempIm=tempIm.resize((width, height))
            projIm=ImageTk.PhotoImage(tempIm)
            projPhoto=Label(photoFr,image=projIm)
            projPhoto.image = projIm #Store a reference
            projPhoto.grid(column=0, row=0, sticky=N+S+W+E)
            #projPhoto.pack(expand=YES, fill=BOTH)
        else:
            photoCanv=Canvas(photoFr, width=maxImgWidth, height=maxImgHeight)
            photoCanv.grid(column=0,row=0,sticky=N+S+W+E)
            photoCanv.create_rectangle(2,2,maxImgWidth,maxImgHeight)
            photoCanv.create_line(1,1,maxImgWidth,maxImgHeight)
            photoCanv.create_line(1,maxImgHeight,maxImgWidth,1)
            photoCanv.create_text(maxImgWidth/2,maxImgHeight/2,text="Photo")
        photoFr.grid(column=0,row=0, sticky=N+S+W+E)
        
        groupOneLeftLow=Frame(groupOneLeft)        
        groupOneLeftLow.grid(column=0,row=1, sticky=N+S+W+E)
        
        photoBrowse = Button(groupOneLeftLow, text = "Browse", 
                             command = lambda: self.loadProjTemplate(projID), width = 10)
        photoBrowse.grid(column=0,row=1)
        
        tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
        tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
        tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
        nmDelBut=Button(groupOneLeftLow,image=tempDelImgTk,relief=FLAT, 
                        command = lambda: self.initUI("Confirm ProjStuff Del","Photo Link", projID))
        nmDelBut.image=tempDelImgTk
        nmDelBut.grid(column=1,row=1,sticky=W+E)    
        ##### PHOTO FRAME #####
        
        ##### LEAD FRAME #####
        leadFr = Frame(groupOneRight)
        projLead=proj.retLead()
        projLeadFont=("Helvetica",13,"bold")
        if not(projLead==""):
            leadNm=self.empList.retName(projLead)
        else:
            leadNm=""
        projLeadLabel = Label(leadFr,text="Project Lead: "+leadNm,font=projLeadFont)
        projLeadLabel.grid(column=0,row=0, sticky=N+S+W+E)
        if projLead == "":
            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(leadFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda:self.initUI("ProjLeadEdit",projID,""))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=1,row=0,sticky=W+E)            
        else:
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(leadFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda:self.initUI("ProjLeadEdit",projID,projLead))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(leadFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda: self.initUI("Confirm ProjStuff Del","Lead", projID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)                
        leadFr.grid(column=0,row=0, sticky=N+S+W+E)
        ##### LEAD FRAME #####        
        
        
        
        ##### EMAIL ALL FRAME #####
        emailFr = Frame(groupOneRight)
        projEmail=proj.retEmailList()
        projEmailFont=("Helvetica",13,"bold")
        projEmailButton = Button(emailFr,text='Email project team',
                                font=projEmailFont, relief=RAISED,
                                command = lambda projEmail=projEmail: mailto(projEmail))
        projEmailButton.grid(column=0,row=0, sticky=N+S+W+E)
        emailFr.grid(column=0,row=1, sticky=N+S+W+E)
        ##### EMAIL ALL FRAME #####
        
        ##### SHAREPOINT LINK FRAME #####
        shareFr = Frame(groupOneRight)
        projShare=proj.retSharepointLink()
        if not projShare=="":
            projShareFont=("Helvetica",13,"bold")
            projShareButton = Button(shareFr,text='Sharepoint Site',
                                    font=projShareFont, relief=RAISED,
                                    command = lambda projShare=projShare: self.browserCallback(projShare))
            projShareButton.grid(column=0,row=0, sticky=N+S+W+E)
            
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(shareFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda projID=projID:self.initUI("ProjShareSet",projID))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(shareFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda projID=projID: self.initUI("Confirm ProjStuff Del","Sharepoint", projID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)
        else:
            projShareFont=("Helvetica",13,"bold")
            projShareButton = Button(shareFr,text='Add Sharepoint Site',
                                    font=projShareFont, relief=RAISED,
                                    command = lambda projShare=projShare: self.initUI("ProjShareSet", projID))
            projShareButton.grid(column=0,row=0, sticky=N+S+W+E)
            
        
        shareFr.grid(column=0,row=2, sticky=N+S+W+E)
        ##### SHAREPOINT LINK FRAME #####        
        
        ##### Description #####        

        descFr = Frame(groupOneRight)     
        curBg=self.cget('bg')
        descFr.grid(column=0,row=3)
        descHdr = Frame(descFr,relief=RIDGE,borderwidth=4)
        descHdr.grid(column=0,row=0,sticky=N+S+W+E)
        descLbl = Label(descHdr,text="Project Description")
        descLbl.grid(column=0,row=0,sticky=N+S+W+E)
        
        tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
        tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
        tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
        nmEditBut=Button(descHdr,image=tempEditImgTk,relief=FLAT,
                         command=lambda:self.initUI("Project Description",projID))
        nmEditBut.image=tempEditImgTk
        nmEditBut.grid(column=1,row=0,sticky=W)        

        scrollbar = Scrollbar(descFr)
                
        descTxt=Text(descFr,yscrollcommand=scrollbar.set)
        descTxt.insert(INSERT,proj.retDesc())
        descTxt.config(state=DISABLED)
        descTxt.config(height=10)
        descTxt.config(width=50)
        descTxt.config(bg=curBg) #Make the bg of the text widget the same as overall bg
        descTxt.grid(column=0,row=1)
        
        scrollbar.grid(column=2,row=1, sticky=N+S+W+E)        
        scrollbar.config(command=descTxt.yview)        
        ##### Description #####
        
        ##### Employee List #####
     
        groupTwoFr = Frame(activeFr) 
        groupTwoFr.grid(column=0,row=2,sticky=N+S+W+E)    
        
        lblFont=("Helvetica",13,"bold")                 
        empLbl = Label(groupTwoFr,text="Employee Name",font=lblFont)
        empLbl.grid(column=0,row=0,sticky=W+E)
        
        empLbl = Label(groupTwoFr,text="Employee Role",font=lblFont)
        empLbl.grid(column=1,row=0,sticky=W+E,padx=30)      
        curRow=1
        
        for empID in proj.retList():
            tempEmp=employee(empID)            
            tempEmp.inFile()
            
            empName=self.empList.retName(empID)
            empNmFont=("Helvetica",13,"bold")
            empNmButton=Button(groupTwoFr,text=str(empName),font=empNmFont,
                                command= lambda empID=empID: self.initUI("Employee",empID))
            empNmButton.grid(column=0,row=curRow,sticky=W+E)
            
            empRole=tempEmp.retProjRole(projID)
            empRoleFont=("Helvetica",13,"bold")
            empRoleLabel=Label(groupTwoFr,text=str(empRole),font=empRoleFont,padx=30)
            empRoleLabel.grid(column=1,row=curRow,sticky=W+E)      
            projHier=tempEmp.retProjHier(projID)
            
            buttonFr=Frame(groupTwoFr)
            buttonFr.grid(column=2,row=curRow)
        
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(buttonFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda empID=empID, projID=projID, projHier=projHier:self.initUI("ProjEmpEdit",empID,projID,projHier))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=0,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(buttonFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda empID=empID, projID=projID: self.initUI("Confirm ProjEmp Del", empID, projID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=1,row=0,sticky=W+E)  
            
            curRow+=1
            
        empAddFr=Frame(groupTwoFr)
        empAddFr.grid(column=0,row=curRow, sticky=N+S+W+E)
        addProj=Button(empAddFr,text="Add New Employee",
                       command=lambda projID=projID:self.initUI("Add Emp to Project", projID))
        addProj.grid(column=0,row=0,pady=7)
        ##### Employee List #####
        
        return activeFr

    def browserCallback(self,url):
        ie = webbrowser.get(webbrowser.iexplore)
        ie.open(url)

    def projShareSet(self,projID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text="Set Sharepoint Link")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        trEv=0 #not sure why it won't work without this, but doesn't like 
        #something to do with the events - first lambda variable absorbs "event"

        fn="lambda trEv=trEv, self=self, projID=projID: self.projShareCallback(1,projID)"
        rtnfn='lambda trEv=trEv, self=self, projID=projID: self.initUI("Project",projID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn))
        valEntry.bind('<Escape>',eval(rtnfn))
        return activeFr
        
        
    def projShareCallback(self,chg,projID):
        newVal=self.v.get()
        tempProj=project(projID)
        tempProj.inFile()
        tempProj.setSharepointLink(newVal)
        self.initUI("Project",projID) #either no change or done, go back to main page
        return 1             
        

    def loadProjTemplate(self,projID): 
        tempProj=project(projID)
        tempProj.inFile()        
        filename = tkFileDialog.askopenfilename(filetypes = (("Image Types", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),("All files", "*.*")))
        if filename == "":
            return
            
        tempProj.setPhotoLink(filename)
        self.initUI("Project",projID)

    def delProjStuff(self,what,projID,val1="",val2=""):
        tempProj=project(projID)
        tempProj.inFile()
        if(what=="Photo Link"):
            tempProj.setPhotoLink()
        elif(what=="Lead"):
            tempProj.chgLead()
        elif(what=="Sharepoint"):
            tempProj.setSharepointLink()
        self.initUI("Project",projID)     
        
    def confirmProjStuffDel(self, what, projID, val1="", val2=""):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)   
        dispWhat=what
        if(what=="Lead"):
            dispWhat='the lead'
        elif(what=="Photo Link"):
            dispWhat='the photo'
        elif(what=="Sharepoint"):
            dispWhat='the Sharepoint link'
        titleLb=Label(activeFr,text='Are you SURE you want to delete '+str(dispWhat)+
                                ' from the project "'+str(self.projList.retName(projID))+'"?')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        okBut=Button(activeFr,text="Confirm", command=lambda: self.delProjStuff(str(what),projID,val1,val2))
        canBut=Button(activeFr,text="Cancel",command=lambda: self.initUI("Project",projID))       
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)      
        return activeFr
                 
    def projEditDesc(self,projID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
                
        tempProj=project(projID)
        tempProj.inFile()
        
        descEditHdr = Label(activeFr,text='Edit the description for the "'+self.projList.retName(projID)+
                                        '" project')
        descEditHdr.grid(column=0,row=0,sticky=W+E,columnspan=2)
        
        descTxt = Text(activeFr)
        descTxt.insert(INSERT,tempProj.retDesc())
        descTxt.mark_set(INSERT,END)
        descTxt.focus_set()
        descTxt.grid(column=0,row=1,sticky=W+E,columnspan=2)
        
        okBut=Button(activeFr,text="OK",
                     command=lambda projID=projID, descTxt=descTxt: self.projDescCallback(projID,descTxt))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda projID=projID: self.initUI("Project",projID))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        
        return activeFr

    def projDescCallback(self,projID,descTxt):
        tempProj=project(projID)
        tempProj.inFile()
        descTxt=descTxt.get("1.0","end-1c") #cover for the added newline
        tempProj.setDesc(descTxt)
        self.initUI("Project",projID)
        return 1          
        
    def projEmpEdit(self,empID,projID,projHier):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Set the role for '+self.empList.retName(empID)+' on the "'+
                                    self.projList.retName(projID)+'" project to:')
        titleLb.grid(column=0,row=0,sticky=N+S+W+E,columnspan=2)
        
        curVal=projHier.retRole()        
        
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.insert(END,str(curVal))
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()        
        
        okBut=Button(activeFr,text="OK",
                     command=lambda empID=empID, projID=projID: self.projEmpChgRoleCallback(empID,projID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Project",projID))
        okBut.grid(column=0,row=2,sticky=W+E)
        canBut.grid(column=1,row=2,sticky=W+E)        
        return activeFr
        
    def projEmpChgRoleCallback(self,empID,projID):
        newVal=self.v.get()
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.setRole(projID,newVal)
        self.initUI("Project",projID) #either no change or done, go back to main page
        return 1        
                
    def projEmpDel(self,empID,projID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you SURE you want to delete the "'+self.projList.retName(projID)+
                                    '" project from '+self.empList.retName(empID)+'?')
        titleLb.grid(column=0,row=0,sticky=N+S+W+E,columnspan=2)
        
        title2Lb=Label(activeFr,text="This action CANNOT be undone.")
        title2Lb.grid(column=0,row=1,sticky=N+S+W+E,columnspan=2)        
        
        okBut=Button(activeFr,text="DELETE",
                     command=lambda empID=empID, projID=projID: self.projEmpDelCallback(empID,projID))
        canBut=Button(activeFr,text="DO NOT DELETE",
                      command=lambda projID=projID: self.initUI("Project",projID))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)        
        
        return activeFr
        
    def projEmpDelCallback(self,empID,projID):
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.remProj(projID)
        self.initUI("Project",projID)
        return 1
                    
    def projEmpAdd(self, projID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)

        tempProj=project(projID)
        tempProj.inFile()

        titleLb=Label(activeFr,text='Add a new employee to the "'+str(self.projList.retName(projID))+
                                    '" project')
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        empVals = self.empList.retListItems()
        empID,empName=zip(*empVals) #unpack into lists

        revDict=dict(zip(empName,empID))
        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        
        empName=list(empName)
        empID=list(empID) #convert from tuple to list so it is mutable

        for curEmp in tempProj.retList():
            if curEmp in empID:
                #don't list emps already on project
                empName.remove(self.empList.retName(curEmp)) 
                empID.remove(curEmp)

        empName=tuple(empName)
        empID=tuple(empID)

        box['values'] = "New Employee",
        box['values'] += empName
        box.grid(column=0,row=1,sticky=W+E,columnspan=2)

        okBut=Button(activeFr,text="OK",
                     command=lambda projID=projID,revDict=revDict: self.projEmpAddCallback(projID,revDict))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda projID=projID: self.initUI("Project",projID))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)        
                
        
        return activeFr

    def projEmpAddCallback(self,projID,revDict):
        empNm=self.v.get()

        if(empNm=="New Employee"):
            #Need to create a new project
            self.initUI("Create Employee",projID)
        else:
            empID=revDict[empNm] #get current ID
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.addProjOrRole(projID) #add to them
            self.initUI("ProjEmpEdit",empID,projID,tempEmp.retProjHier(projID)) #Go to add role

        return 1                 
          
    def createEmp(self,projID=""):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)

        titleLb=Label(activeFr,text="Create New Employee")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        
        trEv=0

        fn="lambda trEv=trEv, self=self, projID=projID: self.createEmpCallback(projID)"
        if projID=="":
            rtnfn='lambda trEv=trEv, self=self: self.initUI("Employee List")'
        else:
            rtnfn='lambda trEv=trEv, self=self, projID=projID: self.initUI("Project",projID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn)) #this isn't working, fix this
        valEntry.bind('<Escape>',eval(rtnfn))        
        
        return activeFr
        
    def createEmpCallback(self,projID=""):
        empNm=self.v.get()
        
        empID=self.empList.addEmp(empNm)#create the new emp

        if projID=="":
            self.initUI("Employee List")
        else:
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.addProjOrRole(projID) #add to them
            self.initUI("ProjEmpEdit",empID,projID,tempEmp.retProjHier(projID)) #Go to add role
        return 1
          
    def projNameEdit(self,projID,curVal=""):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text="Edit Project Name")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.insert(END,str(curVal))
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        trEv=0 #not sure why it won't work without this, but doesn't like 
        #something to do with the events - first lambda variable absorbs "event"

        fn="lambda trEv=trEv, self=self, projID=projID: self.projNameCallback(1,projID)"
        rtnfn='lambda trEv=trEv, self=self, projID=projID: self.initUI("Project",projID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn))
        valEntry.bind('<Escape>',eval(rtnfn))
        return activeFr
          
    def projNameCallback(self,chg,projID):
        newVal=self.v.get()
        if(newVal==""):
            chg=0
        if(chg==1):
            tempProj=project(projID)
            tempProj.inFile()
            tempProj.renameProj(newVal)
        self.initUI("Project",projID) #either no change or done, go back to main page
        return 1        
          
    def projLeadEdit(self,projID,curVal=""):

        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)

        tempProj=project(projID)
        tempProj.inFile()

        titleLb=Label(activeFr,text="Set Project Lead")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        
        empIDList=tempProj.retList()
        revDict=dict()
        empNmList=list()
        for empID in empIDList:
            revDict[self.empList.retName(empID)]=empID
            empNmList.append(self.empList.retName(empID))

        if not empNmList==[]:
            
            empNmList=tuple(empNmList)
            empIDList=tuple(empIDList)

            box['values'] = empNmList
            box.grid(column=0,row=1,sticky=W+E,columnspan=2)

            okBut=Button(activeFr,text="OK",
                         command=lambda projID=projID,revDict=revDict: self.projLeadCallback(projID,revDict))
            okBut.grid(column=0,row=2,sticky=W)
        else:
            warnLb=Label(activeFr,text="There are no employees on this project")
            warnLb.grid(column=0,row=1)
        canBut=Button(activeFr,text="Cancel",
                      command=lambda projID=projID: self.initUI("Project",projID))
        
        canBut.grid(column=1,row=2,sticky=E)        
                
                
        return activeFr          
          
    def projLeadCallback(self,projID,revDict):
        newVal=self.v.get()
        empID=revDict[newVal]
        tempProj=project(projID)
        tempProj.inFile()
        tempProj.chgLead(empID)
        self.initUI("Project",projID) #either no change or done, go back to main page
        return 1                  
          
          
          
          
################################################################################################
################################HINT:Employee Screen############################################
################################################################################################            
          
          
          
    def empScreen(self,empID):
        #Frame lists, from top to bottom
        #Name, edit
        #Group 1:
        #   Left - photo
        #   Right - Title, edit
        #   Right - Email, edit
        #   Right - Work Number, edit
        #   Right - Cell Number, edit
        #Group 2:
        #   Each project has separate sub frame
        #   Project, role headers, edit
        #       Left: Reports to, Oversees
        #       Right: Name of appropriate person
        #Group 3:
        #   Left - skill list
        #   Right - Interest list
        #Notes        
        
        maxImgHeight = 300
        maxImgWidth = 300
        
        iconWidth=self.iconWidth
        iconHeight=self.iconHeight
        
        emp=employee(empID)
        emp.inFile()
        
#        self.scrollCanv=Canvas(self.parent,borderwidth=0)
#        self.vsb = Scrollbar(self.parent, orient="vertical", command=self.scrollCanv.yview)
#        self.scrollCanv.configure(yscrollcommand=self.vsb.set)
#        self.vsb.pack(side="right",fill="y")
#        self.scrollCanv.pack(side="left", fill="both", expand=True)
#        
#        self.activeFr=Frame(self.scrollCanv)
#        self.activeFr.columnconfigure(0,weight=1)
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)   
        
        ##### NAME FRAME #####        
        nameFr = Frame(activeFr)
        nameFr.grid(column=0,row=0,sticky=N+S+W+E)
        nameFr.rowconfigure(0,weight=1)
        empNameFont=("Helvetica",16,"bold")
        empNameLabel = Label(nameFr,text=emp.retName(),font=empNameFont)
        empNameLabel.grid(column=0,row=0, sticky=N+S+W+E)
        
        tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
        tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
        tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
        nmEditBut=Button(nameFr,image=tempEditImgTk,relief=FLAT,
                         command=lambda:self.initUI("EmpEdit",empID,"Name",self.empList.retName(empID)))
        nmEditBut.image=tempEditImgTk
        nmEditBut.grid(column=1,row=0,sticky=W+E)
        ##### NAME FRAME #####        
        

        groupOneFr = Frame(activeFr)
        #Photo, title, birthday, email, work num, cell num
        
        groupOneFr.grid(column=0,row=1,sticky=N+S+W+E)    
        
        groupOneLeft = Frame(groupOneFr)
        groupOneLeft.grid(column=0,row=0,sticky=N+S+W+E)  
        
        groupOneRight = Frame(groupOneFr)
        groupOneRight.grid(column=1,row=0,sticky=N+S+W+E)        
                
        ##### PHOTO FRAME #####     
        #TODO: Copy photo to local link
        photoFr=Frame(groupOneLeft)
        photoLink=emp.retPhotoLink()
        if not photoLink=="":
            tempIm = Image.open(photoLink)
            (width, height) = tempIm.size
            if height > maxImgHeight:
                width = (width*maxImgHeight)/height
                height = maxImgHeight
            if width > maxImgWidth:
                height = (height*maxImgWidth)/width
                width = maxImgWidth
            tempIm=tempIm.resize((width, height))
            empIm=ImageTk.PhotoImage(tempIm)
            empPhoto=Label(photoFr,image=empIm)
            empPhoto.image = empIm #Store a reference
            empPhoto.grid(column=0, row=0, sticky=N+S+W+E)
            #empPhoto.pack(expand=YES, fill=BOTH)
        else:
            photoCanv=Canvas(photoFr, width=maxImgWidth, height=maxImgHeight)
            photoCanv.grid(column=0,row=0,sticky=N+S+W+E)
            photoCanv.create_rectangle(2,2,maxImgWidth,maxImgHeight)
            photoCanv.create_line(1,1,maxImgWidth,maxImgHeight)
            photoCanv.create_line(1,maxImgHeight,maxImgWidth,1)
            photoCanv.create_text(maxImgWidth/2,maxImgHeight/2,text="Photo")
        photoFr.grid(column=0,row=0, sticky=N+S+W+E)
        
        groupOneLeftLow=Frame(groupOneLeft)        
        groupOneLeftLow.grid(column=0,row=1, sticky=N+S+W+E)
        
        photoBrowse = Button(groupOneLeftLow, text = "Browse", 
                             command = lambda: self.loadtemplate(empID), width = 10)
        photoBrowse.grid(column=0,row=1)
        
        tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
        tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
        tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
        nmDelBut=Button(groupOneLeftLow,image=tempDelImgTk,relief=FLAT, 
                        command = lambda: self.initUI("Confirm EmpStuff Del","Photo Link", empID))
        nmDelBut.image=tempDelImgTk
        nmDelBut.grid(column=1,row=1,sticky=W+E)    
        ##### PHOTO FRAME #####
        
        ##### TITLE FRAME #####
        titleFr = Frame(groupOneRight)
        empTitle=emp.retTitle()
        empTitleFont=("Helvetica",13,"bold")
        empTitleLabel = Label(titleFr,text="Title: "+empTitle,font=empTitleFont)
        empTitleLabel.grid(column=0,row=0, sticky=N+S+W+E)
        if empTitle == "":
            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(titleFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda:self.initUI("EmpEdit",empID,"Title",emp.retTitle()))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=1,row=0,sticky=W+E)            
        else:
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(titleFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda:self.initUI("EmpEdit",empID,"Title",emp.retTitle()))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(titleFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda: self.initUI("Confirm EmpStuff Del","Title", empID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)                
        titleFr.grid(column=0,row=0, sticky=N+S+W+E)
        ##### TITLE FRAME #####        
        
        ##### B-DAY FRAME #####
        bdayFr = Frame(groupOneRight)
        empBday=emp.retBday()
        empBdayFont=("Helvetica",13,"bold")
        empBdayLabel = Label(bdayFr,text="Birthday: "+empBday,font=empBdayFont)
        empBdayLabel.grid(column=0,row=0, sticky=N+S+W+E)
        if empBday == "":
            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(bdayFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda:self.initUI("EmpEdit",empID,"Birthday",emp.retBday()))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=1,row=0,sticky=W+E)            
        else:
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(bdayFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda:self.initUI("EmpEdit",empID,"Birthday",emp.retBday()))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(bdayFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda: self.initUI("Confirm EmpStuff Del","Birthday", empID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)                
        bdayFr.grid(column=0,row=1, sticky=N+S+W+E)
        ##### B-DAY FRAME #####
        
        
        
        ##### EMAIL FRAME #####
        emailFr = Frame(groupOneRight)
        empEmail=emp.retEmail()
        empEmailFont=("Helvetica",13,"bold")
        empEmailButton = Button(emailFr,text="E-mail: "+empEmail, font=empEmailFont, relief=FLAT,
                                command = lambda empEmail=empEmail: mailto(empEmail))
        empEmailButton.grid(column=0,row=0, sticky=N+S+W+E)
        if empEmail == "":
            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(emailFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda:self.initUI("Email",empID,"Email",emp.retEmail()))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=1,row=0,sticky=W+E)            
        else:
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(emailFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda:self.initUI("Email",empID,"Email",emp.retEmail()))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(emailFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda: self.initUI("Confirm EmpStuff Del","Email", empID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)    
        emailFr.grid(column=0,row=2, sticky=N+S+W+E)
        ##### EMAIL FRAME #####
        
        ##### WORK PHONE #####
        workPhoneFr = Frame(groupOneRight)
        empWorkPh=emp.retWorkPhone()
        empWorkPhFont=("Helvetica",13,"bold")
        empWorkPhLabel = Label(workPhoneFr,text=("Work Phone: "+empWorkPh),font=empWorkPhFont)
        empWorkPhLabel.grid(column=0,row=0, sticky=N+S+W+E)
        if empWorkPh == "":
            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(workPhoneFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda:self.initUI("Work Phone",empID,"Work Phone",emp.retWorkPhone()))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=1,row=0,sticky=W+E)            
        else:
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(workPhoneFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda:self.initUI("Work Phone",empID,"Work Phone",emp.retWorkPhone()))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(workPhoneFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda: self.initUI("Confirm EmpStuff Del","Work Phone", empID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)            
        
        
        workPhoneFr.grid(column=0,row=3, sticky=N+S+W+E)
        ##### WORK PHONE #####
        
        ##### CELL PHONE #####
        cellPhoneFr = Frame(groupOneRight)
        empCellPh=emp.retCellPhone()
        empCellPhFont=("Helvetica",13,"bold")
        empCellPhLabel = Label(cellPhoneFr,text=("Cell Phone: "+empCellPh),font=empCellPhFont)
        empCellPhLabel.grid(column=0,row=0, sticky=N+S+W+E)
        if empCellPh == "":
            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(cellPhoneFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda:self.initUI("Cell Phone",empID,"Cell Phone",emp.retCellPhone()))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=1,row=0,sticky=W+E)            
        else:
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(cellPhoneFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda:self.initUI("Cell Phone",empID,"Cell Phone",emp.retCellPhone()))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(cellPhoneFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda: self.initUI("Confirm EmpStuff Del","Cell Phone", empID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)            
        
        cellPhoneFr.grid(column=0,row=4, sticky=N+S+W+E)
        ##### CELL PHONE #####
        
        groupOneRight.rowconfigure(0,weight=1)
        groupOneRight.rowconfigure(1,weight=1)
        groupOneRight.rowconfigure(2,weight=1)
        groupOneRight.rowconfigure(3,weight=1)
        
        groupTwoFr = Frame(activeFr, pady=20)     
        #Project and structure
        groupTwoFr.grid(column=0,row=2,sticky=N+S+W+E)
        
        ##### PROJECTS, ROLES, SUPERIORS, SUBORDS #####
        projList = emp.retProjList()
        curRow=0
        self.projList.inFile() #update list in case of changes
        self.empList.inFile()

        for projID, projHier in projList:
            projFr=Frame(groupTwoFr,borderwidth=2,relief=GROOVE)
            projFr.grid(column=0,row=curRow,sticky=W+E)
            
            titleBandFr=Frame(projFr)
            titleBandFr.grid(column=0,row=0,sticky=W+E)
            
            titleLeftFr = Frame(titleBandFr)
            titleLeftFr.grid(column=0,row=0,sticky=W+E)
            
            titleRightFr = Frame(titleBandFr)
            titleRightFr.grid(column=1,row=0,sticky=W+E) #role in 2nd column
            
            projName=self.projList.retName(projID)
            projNmFont=("Helvetica",13,"bold")
            projNmButton=Button(titleLeftFr,text=str(projName),font=projNmFont,
                                command= lambda projID=projID: self.initUI("Project",projID))
            projNmButton.grid(column=0,row=0,sticky=W+E)
            
            projRole=projHier.retRole()
            projRoleFont=("Helvetica",13,"bold")
            projRoleLabel=Label(titleRightFr,text=str(projRole),font=projRoleFont,padx=30)
            projRoleLabel.grid(column=0,row=0,sticky=W+E)            
            
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(titleRightFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda projID=projID, projHier=projHier:self.initUI("EmpProjEdit",empID,projID,projHier))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(titleRightFr,image=tempDelImgTk,relief=FLAT,
                            command = lambda projID=projID: self.initUI("Confirm EmpProj Del", empID, projID))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)  
            
            
            ####Superiors####
            supTitleFr = Frame(projFr)
            supTitleFr.grid(column=0,row=1) #left side, below the name/role
            supTitleFont=("Helvetica",13,"bold")
            supTitleTxt = Label(supTitleFr,text="Reports to:",font=supTitleFont)            
            supTitleTxt.grid(row=0,column=0,sticky=W+E)
            supFr=Frame(projFr)            
            supFr.grid(column=0,row=2) #follows right below title
            supRow=0
            for sup in projHier.retSup():
                listBlankFr=Frame(supFr) #have a blank frame on the left side to indent this
                listBlankFr.grid(column=0,row=supRow, sticky=W+E) #right side, extending down
                supBut=Button(listBlankFr,text=self.empList.retName(sup),
                              command=lambda sup=sup: self.initUI("Employee",sup))
                supBut.grid(column=1,row=0)
                
                tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
                tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
                tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
                nmDelBut=Button(listBlankFr,image=tempDelImgTk,relief=FLAT,
                                command = lambda projID=projID, sup=sup: self.initUI("Confirm EmpStuff Del","Sup", empID, projID, sup))
                nmDelBut.image=tempDelImgTk
                nmDelBut.grid(column=2,row=0,sticky=W+E) 

                supRow+=1

            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(supFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda projID=projID:self.initUI("Add Proj Hier","Sup", empID, projID))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=0,row=supRow,sticky=W+E)                  
                                   
            ####Subordinates####
            subTitleFr = Frame(projFr)
            subTitleFr.grid(column=0,row=3) #left side, below the supervisors            
            subTitleFont=("Helvetica",13,"bold")
            subTitleTxt = Label(subTitleFr,text="Oversees:",font=subTitleFont)            
            subTitleTxt.grid(row=0,column=0,sticky=W+E)
            subFr=Frame(projFr)            
            subFr.grid(column=0,row=4) #follows below superiors section
            subRow=0
            for sub in projHier.retSub():
                listBlankFr=Frame(subFr) #have a blank frame on the left side to indent this
                listBlankFr.grid(column=0,row=subRow, sticky=W+E) #right side, extending down
                subBut=Button(listBlankFr,text=self.empList.retName(sub),
                               command=lambda sub=sub: self.initUI("Employee",sub))
                subBut.grid(column=1,row=0)

                tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
                tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
                tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
                nmDelBut=Button(listBlankFr,image=tempDelImgTk,relief=FLAT,
                                command = lambda projID=projID, sub=sub: self.initUI("Confirm EmpStuff Del","Sub", empID, projID, sub))
                nmDelBut.image=tempDelImgTk
                nmDelBut.grid(column=2,row=0,sticky=W+E) 

                subRow+=1   
                
            tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
            tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
            tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
            nmAddBut=Button(subFr,image=tempAddImgTk,relief=FLAT,
                            command=lambda projID=projID:self.initUI("Add Proj Hier","Sub", empID, projID))
            nmAddBut.image=tempAddImgTk
            nmAddBut.grid(column=0,row=subRow,sticky=W+E)    
            
            curRow+=1
        #Add Project button
        projFr=Frame(groupTwoFr)
        projFr.grid(column=0,row=curRow, sticky=N+S+W+E)
        addProj=Button(projFr,text="Add New Project",
                       command=lambda empID=empID:self.initUI("Add New Project", empID))
        addProj.grid(column=0,row=0)
        ##### PROJECTS, ROLES, SUPERIORS, SUBORDS #####
        
        abilFr=Frame(activeFr)
        abilFr.grid(column=0,row=3,sticky=N+S+W+E)
       
        ##### SKILLS #####
        skillsFr=Frame(abilFr,borderwidth=4,relief=GROOVE)
        skillsFr.grid(column=0,row=0,sticky=N+S+W+E)
        
        self.skillList.inFile()
                
        skTitle = Label(skillsFr,text="Skill",relief=RIDGE,borderwidth=2)
        skTitle.grid(column=0,row=0,sticky=N+S+W+E)
        
        skLvlTitle = Label(skillsFr,text="Level",relief=RIDGE,borderwidth=2)
        skLvlTitle.grid(column=1,row=0,sticky=N+S+W+E)
        skillsFr.grid_columnconfigure(0,weight=1)
        curRow = 1
        for skill,skLvl in emp.retSkillList():
            tempSkFr = Frame(skillsFr,relief=RIDGE,borderwidth=3)
            tempSkFr.grid(column=0, row=curRow,sticky=N+S+W+E)
            
            skLbl=Button(tempSkFr,relief=GROOVE,text=str(self.skillList.retName(int(skill))), 
                         command=lambda skill=skill: self.initUI("Skill List",skill))
            #skLbl.grid(column=0,row=0,sticky=N+S+W+E)
            skLbl.pack(expand=YES,fill=BOTH)
            
            #skLbl=Label(tempSkFr,text=str(self.skillList.retName(int(skill))))
            #skLbl.grid(column=0,row=0,sticky=N+S+W+E)            
        
            #tempSkLvlFr = Frame(skillsFr,relief=RIDGE,borderwidth=3)
            lvlFr = Frame(skillsFr,relief=RIDGE, borderwidth=3)
            lvlFr.grid(column=1,row=curRow,sticky=N+S+W+E)
            tempSkLvlFr = self.abilLvl(skLvl,lvlFr)
            tempSkLvlFr.grid(column=0, row=0,sticky=N+S+W+E)
            
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(lvlFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda skill=skill,skLvl=skLvl:self.initUI("SkillLvl",empID,skill,skLvl))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=N+S+W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(lvlFr,image=tempDelImgTk,relief=FLAT,
                            command=lambda empID=empID, skill=skill: self.initUI("Confirm EmpStuff Del","Skill",empID,skill))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)   
            

            curRow+=1
            
        tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
        tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
        tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
        nmAddBut=Button(skillsFr,image=tempAddImgTk,relief=FLAT,
                        command=lambda:self.initUI("Employee Skill",empID))
        nmAddBut.image=tempAddImgTk
        nmAddBut.grid(column=0,row=curRow,sticky=W+E)    
               
        
        ##### SKILLS #####


        ##### INTERESTS #####

        interestsFr=Frame(abilFr,borderwidth=4,relief=GROOVE)
        interestsFr.grid(column=0,row=1,sticky=N+S+W+E)
        
        self.intList.inFile()
        intTitle = Label(interestsFr,text="Interest",relief=RIDGE,borderwidth=2)
        intTitle.grid(column=0,row=0,sticky=N+S+W+E)
        
        intLvlTitle = Label(interestsFr,text="Level",relief=RIDGE,borderwidth=2)
        intLvlTitle.grid(column=1,row=0,sticky=N+S+W+E)
        interestsFr.grid_columnconfigure(0,weight=1)
        
        curRow = 1
        
        for interest,intLvl in emp.retIntList():
            tempIntFr = Frame(interestsFr,relief=RIDGE,borderwidth=3)
            tempIntFr.grid(column=0, row=curRow,sticky=N+S+W+E)
               
            intLbl=Button(tempIntFr,relief=GROOVE,text=str(self.intList.retName(int(interest))),
                         command=lambda interest=interest: self.initUI("Interest List",interest))
            intLbl.pack(expand=YES,fill=BOTH)          
            
            #intLbl=Label(tempIntFr,text=str(self.intList.retName(int(interest))))
            #intLbl.grid(column=0,row=0,sticky=N+S+W+E)
            
            lvlFr = Frame(interestsFr,relief=RIDGE, borderwidth=3)
            lvlFr.grid(column=1,row=curRow,sticky=N+S+W+E)
            tempIntLvlFr = self.abilLvl(intLvl,lvlFr)
            tempIntLvlFr.grid(column=0, row=0,sticky=N+S+W+E)
            
            tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
            tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
            tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
            nmEditBut=Button(lvlFr,image=tempEditImgTk,relief=FLAT,
                             command=lambda interest=interest,intLvl=intLvl:
                                 self.initUI("IntLvl",empID,interest,intLvl))
            nmEditBut.image=tempEditImgTk
            nmEditBut.grid(column=1,row=0,sticky=N+S+W+E)
            
            tempDelImg=Image.open(os.path.join(os.getcwd(),"img","DeleteIcon.png"))
            tempDelImg=tempDelImg.resize((iconWidth,iconHeight))
            tempDelImgTk=ImageTk.PhotoImage(tempDelImg)
            nmDelBut=Button(lvlFr,image=tempDelImgTk,relief=FLAT,
                            command=lambda empID=empID, interest=interest: self.initUI("Confirm EmpStuff Del","Interest",empID,interest))
            nmDelBut.image=tempDelImgTk
            nmDelBut.grid(column=2,row=0,sticky=W+E)               
            
            curRow+=1
            
        tempAddImg=Image.open(os.path.join(os.getcwd(),"img","AddIcon.png"))
        tempAddImg=tempAddImg.resize((iconWidth,iconHeight))
        tempAddImgTk=ImageTk.PhotoImage(tempAddImg)
        nmAddBut=Button(interestsFr,image=tempAddImgTk,relief=FLAT,
                        command=lambda:self.initUI("Employee Interest",empID))
        nmAddBut.image=tempAddImgTk
        nmAddBut.grid(column=0,row=curRow,sticky=W+E)                

        ##### INTERESTS #####        


        ##### Notes #####        
        notesFr = Frame(activeFr)     
        #Project and structure
        curBg=self.cget('bg')
        notesFr.grid(column=0,row=4,sticky=W+E)
        notesHdr = Frame(notesFr,relief=RIDGE,borderwidth=2)
        notesHdr.grid(column=0,row=0,sticky=N+S+W+E)
        notesLbl = Label(notesHdr,text="Notes")
        notesLbl.grid(column=0,row=0,sticky=N+S+W+E)
        tempEditImg=Image.open(os.path.join(os.getcwd(),"img","EditIcon.png"))
        tempEditImg=tempEditImg.resize((iconWidth,iconHeight))
        tempEditImgTk=ImageTk.PhotoImage(tempEditImg)
        nmEditBut=Button(notesHdr,image=tempEditImgTk,relief=FLAT,
                         command=lambda:self.initUI("Employee Notes",empID))
        nmEditBut.image=tempEditImgTk
        nmEditBut.grid(column=1,row=0,sticky=W)        

        scrollbar = Scrollbar(notesFr)
        
        noteTxt=Text(notesFr,yscrollcommand=scrollbar.set)
        noteTxt.insert(INSERT,emp.retNotes())
        noteTxt.config(state=DISABLED)
        noteTxt.config(bg=curBg) #Make the bg of the text widget the same as overall bg
        noteTxt.grid(column=0,row=1,sticky=W+E,columnspan=2)
        
        scrollbar.grid(column=2,row=1, sticky=N+S+W+E)        
        scrollbar.config(command=noteTxt.yview)
        
        ##### Notes #####        

        return activeFr      


    def empProjEdit(self,empID,projID,projHier):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Set the role for '+self.empList.retName(empID)+' on the "'+
                                    self.projList.retName(projID)+'" project to:')
        titleLb.grid(column=0,row=0,sticky=N+S+W+E,columnspan=2)
        
        curVal=projHier.retRole()        
        
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.insert(END,str(curVal))
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()        
        
        okBut=Button(activeFr,text="OK",
                     command=lambda empID=empID, projID=projID: self.empChgRoleCallback(empID,projID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Employee",empID))
        okBut.grid(column=0,row=2,sticky=W+E)
        canBut.grid(column=1,row=2,sticky=W+E)        
        return activeFr
        
    def empChgRoleCallback(self,empID,projID):
        newVal=self.v.get()
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.setRole(projID,newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1        
        
        
    def empProjDel(self,empID,projID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        titleLb=Label(activeFr,text='Are you SURE you want to delete the "'+self.projList.retName(projID)+
                                    '" project from '+self.empList.retName(empID)+'?')
        titleLb.grid(column=0,row=0,sticky=N+S+W+E,columnspan=2)
        
        title2Lb=Label(activeFr,text="This action CANNOT be undone.")
        title2Lb.grid(column=0,row=1,sticky=N+S+W+E,columnspan=2)        
        
        okBut=Button(activeFr,text="DELETE",
                     command=lambda empID=empID, projID=projID: self.empProjDelCallback(empID,projID))
        canBut=Button(activeFr,text="DO NOT DELETE",
                      command=lambda empID=empID: self.initUI("Employee",empID))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)        
        
        return activeFr
        
    def empProjDelCallback(self,empID,projID):
        tempEmp=employee(empID)
        tempEmp.inFile()
        tempEmp.remProj(projID)
        self.initUI("Employee",empID)
        return 1


    def addHier(self,what,empID,projID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        
        tempProj=project(projID,"temp")
        tempProj.inFile()
        
        tempEmp=employee(empID)
        tempEmp.inFile()
        
        empOnProj=tempProj.retList()
        if empID in empOnProj:
            empOnProj.remove(empID)                   
        if(what=="Sup"):
            titleLb=Label(activeFr,text="Add employee to oversee "+self.empList.retName(empID))
            for tempID in tempEmp.retProjSup(projID):
                if tempID in empOnProj:
                    empOnProj.remove(tempID)
        else:
            titleLb=Label(activeFr,text="Add employee overseen by "+self.empList.retName(empID))
            for tempID in tempEmp.retProjSub(projID):
                if tempID in empOnProj:
                    empOnProj.remove(tempID)            
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        empNmOnProj=list()
        for emp in empOnProj:
            empNmOnProj.append(self.empList.retName(emp))
        
        if not empNmOnProj==[]:
            box['values'] = empNmOnProj
            box.grid(column=0,row=1,sticky=W+E)
    
            okBut=Button(activeFr,text="OK",
                         command=lambda empID=empID, what=what: self.empAddHierCallback(what,empID,projID))
            okBut.grid(column=0,row=3,sticky=W+E)   
        else:
            warnLbl=Label(activeFr,text="No Available Employees On Project To Add")
            warnLbl.grid(column=0,row=3)
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Employee",empID))
        canBut.grid(column=1,row=3,sticky=W+E)

        return activeFr    
        
    def empAddHierCallback(self,what,empID,projID):
        newVal=self.v.get()
        revDict=dict()
        tempID,tempNm=zip(*self.empList.empList.items())
        revDict=dict(zip(tempNm,tempID))
        newEmpID=revDict[newVal]
        if(newVal==""):
            chg=0
        else:
            chg=1
        if(chg==1):
            tempEmp=employee(empID)
            tempEmp.inFile()
            if(what=="Sup"):
                tempEmp.addProjSup(projID,newEmpID)
            else:
                tempEmp.addProjSub(projID,newEmpID)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1    

    def empProjAdd(self, empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)

        tempEmp=employee(empID)
        tempEmp.inFile()

        titleLb=Label(activeFr,text="Add a new project to "+str(self.empList.retName(empID)))
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        projVals = self.projList.retListItems()
        projID,projName=zip(*projVals) #unpack into lists

        revDict=dict(zip(projName,projID))
        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        
        projName=list(projName)
        projID=list(projID) #convert from tuple to list so it is mutable

        for curEmpProj in tempEmp.retProjIDList():
            if curEmpProj in projID:
                #don't list projects emp is already on
                projName.remove(self.projList.retName(curEmpProj)) 
                projID.remove(curEmpProj)

        projName=tuple(projName)
        projID=tuple(projID)

        box['values'] = "New Project",
        box['values'] += projName
        box.grid(column=0,row=1,sticky=W+E,columnspan=2)

        okBut=Button(activeFr,text="OK",
                     command=lambda empID=empID,revDict=revDict: self.empProjAddCallback(empID,revDict))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Employee",empID))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)        
                
        
        return activeFr


    def empProjAddCallback(self,empID,revDict):
        projNm=self.v.get()

        if(projNm=="New Project"):
            #Need to create a new project
            self.initUI("Create Project",empID)
        else:
            projID=revDict[projNm] #get current ID
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.addProjOrRole(projID) #add to them
            self.initUI("EmpProjEdit",empID,projID,tempEmp.retProjHier(projID)) #Go to add role

        return 1       

    def createProj(self,empID=""):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)

        titleLb=Label(activeFr,text="Create New Project")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        
        trEv=0

        fn="lambda trEv=trEv, self=self, empID=empID: self.createProjCallback(empID)"
        if empID=="":
            rtnfn='lambda trEv=trEv, self=self: self.initUI("Project List")'
        else:
            rtnfn='lambda trEv=trEv, self=self, empID=empID: self.initUI("Employee",empID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn)) #this isn't working, fix this
        valEntry.bind('<Escape>',eval(rtnfn))        
        
        return activeFr
        
    def createProjCallback(self,empID):
        projNm=self.v.get()
        projID=self.projList.addProj(projNm)
        if empID=="":
            self.initUI("Project List")
        else:
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.addProjOrRole(projID) #add to them
            self.initUI("EmpProjEdit",empID,projID,tempEmp.retProjHier(projID)) #Go to add role
        return 1



    def abilLvl(self,lvl,frame):
        lvlFr=Frame(frame,relief=RIDGE,borderwidth=3)
        abilImg=Image.open(os.path.join(os.getcwd(),"img",str(lvl)+".png"))
        abilImg=abilImg.resize((30,30))
        abilImgTk=ImageTk.PhotoImage(abilImg)
        abilImgLbl=Label(lvlFr,relief=FLAT,image=abilImgTk)
        abilImgLbl.image=abilImgTk
        abilImgLbl.grid(column=0,row=0,sticky=W+E)
        return lvlFr

    def loadtemplate(self,empID): 
        tempEmp=employee(empID)
        tempEmp.inFile()        
        filename = tkFileDialog.askopenfilename(filetypes = (("Image Types", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),("All files", "*.*")))
        if filename == "":
            return
            
        tempEmp.setPhotoLink(filename)
        self.initUI("Employee",empID)
        
    def empEdit(self,empID,what,curVal=""):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        if(what == "Birthday"):
            what = "Birthday (format mm/dd)"
        titleLb=Label(activeFr,text="Edit "+str(what))
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        if(what=="Cell Phone"): #update it for the function call
            what="CellPhone"
        elif(what=="Work Phone"):
            what="WorkPhone"
        elif(what=="Birthday (format mm/dd)"):
            what = "Birthday"
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.insert(END,str(curVal))
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        fn="self."+what+"Callback(1,empID)"
        rtnfn='self.initUI("Employee",empID)'
        trEv=0 #not sure why it won't work without this, but doesn't like 
        #something to do with the events - first lambda variable absorbs "event"

        fn="lambda trEv=trEv, self=self, empID=empID: self."+what+"Callback(1,empID)"
        rtnfn='lambda trEv=trEv, self=self, empID=empID: self.initUI("Employee",empID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn))
        valEntry.bind('<Escape>',eval(rtnfn))
        return activeFr
        
    def empAbilEdit(self,kind,empID,abilID,abilLvl):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        if(kind=="Int"):
            what="Interest"
        else:
            what="Skill"
        titleLb=Label(activeFr,text="Edit "+str(what)+" Level")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)


        if(kind=="Skill"):
            abilName=Label(activeFr,text=self.skillList.retName(int(abilID)))
        else:
            abilName=Label(activeFr,text=self.intList.retName(int(abilID)))
        abilName.grid(column=0,row=1,sticky=W+E,columnspan=2)

        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        box['values'] = (0,1,2,3,4)
        box.set(int(abilLvl))
        box.grid(column=0,row=2,sticky=W+E,columnspan=2)

        if(kind=="Skill"):
            expl=Label(activeFr,text="Legend:\n"+"0 - no knowledge of task\n"+
                                "1 - exposed to the task\n"+"2 - can only perform task with assistance\n"+
                                "3 - can perform task without assistance\n"+"4 - can train others")
        else:
            expl=Label(activeFr,text="Legend:\n"+"0 - no interest\n"+
                                "1 - light interest\n"+"2 - medium interest\n"+
                                "3 - strong interest\n"+"4 - obsessed")
        expl.grid(column=0,row=4,sticky=W+E,columnspan=2)                

        okBut=Button(activeFr,text="OK",
                     command=lambda empID=empID, abilID=abilID, kind=kind: self.empAbilCallback(kind,empID,abilID))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Employee",empID))
        okBut.grid(column=0,row=3,sticky=W)
        canBut.grid(column=1,row=3,sticky=E)

        return activeFr        

    def empEditNotes(self,empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
                
        tempEmp=employee(empID)
        tempEmp.inFile()
        
        noteEditHdr = Label(activeFr,text="Edit the notes section for "+self.empList.retName(empID))
        noteEditHdr.grid(column=0,row=0,sticky=W+E,columnspan=2)
        
        noteTxt = Text(activeFr)
        noteTxt.insert(INSERT,tempEmp.retNotes())
        noteTxt.mark_set(INSERT,END)
        noteTxt.focus_set()
        noteTxt.grid(column=0,row=1,sticky=W+E,columnspan=2)
        
        okBut=Button(activeFr,text="OK",
                     command=lambda empID=empID, noteTxt=noteTxt: self.empNoteCallback(empID,noteTxt))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Employee",empID))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        
        return activeFr

    def empNoteCallback(self,empID,noteTxt):
        tempEmp=employee(empID)
        tempEmp.inFile()
        txtVal=noteTxt.get("1.0","end-1c") #cover for the added newline
        tempEmp.setNotes(txtVal)
        self.initUI("Employee",empID)
        return 1

    def delEmpStuff(self,what,empID,val1="",val2=""):
        tempEmp=employee(empID)
        tempEmp.inFile()
        if(what=="Photo Link"):
            tempEmp.setPhotoLink()
        elif(what=="Title"):
            tempEmp.setTitle()
        elif(what=="Cell Phone"):
            tempEmp.setCell()
        elif(what=="Work Phone"):
            tempEmp.setWork()
        elif(what=="Email"):
            tempEmp.setEmail()
        elif(what=="Skill"):
            tempEmp.remSkill(val1)
        elif(what=="Interest"):
            tempEmp.remInt(val1)   
        elif(what=="Sup"):
            tempEmp.remProjSup(val1,val2,1)
        elif(what=="Sub"):
            tempEmp.remProjSub(val1,val2,1)   
        elif(what=="Birthday"):
            tempEmp.setBday()
        self.initUI("Employee",empID)     
        
    def confirmEmpStuffDel(self, what, empID, val1="", val2=""):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)   
        dispWhat=what
        if(what=="Skill"):
            dispWhat=what+" \""+self.skillList.retName(val1)+"\""
        elif(what=="Interest"):
            dispWhat=what+" \""+self.intList.retName(val1)+"\""
        elif(what=="Sup"):
            #val1=projID,val2=supID
            dispWhat=str(self.empList.retName(val2))+" as overseer of "+str(self.empList.retName(empID))
        elif(what=="Sub"):
            #val1=projID,val2=subID
            dispWhat=str(self.empList.retName(empID))+" as overseer of "+str(self.empList.retName(val2))
        titleLb=Label(activeFr,text="Are you SURE you want to delete "+str(dispWhat)+"?")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
        okBut=Button(activeFr,text="Confirm", command=lambda: self.delEmpStuff(str(what),empID,val1,val2))
        canBut=Button(activeFr,text="Cancel",command=lambda: self.initUI("Employee",empID))       
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)      
        return activeFr
      
    def empAbilCallback(self,kind,empID,abilID):
        newVal=self.v.get()
        tempEmp=employee(empID)
        tempEmp.inFile()
        if(kind=="Skill"):
            tempEmp.chgSkillLvl(abilID,newVal)
        else:
            tempEmp.chgIntLvl(abilID,newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1       

    def empAddAbilCallback(self,kind,empID,revDict):
        abilNm=self.v2.get()
        abilLvl=self.v.get()
        if(kind=="Int"):
            what="Interest"
        else:
            what="Skill"
        if(abilNm=="New "+what):
            #Need to add a new ability
            self.initUI("Add "+what,empID,abilLvl)
        else:
            abilID=revDict[abilNm] #get current ID
            tempEmp=employee(empID)
            tempEmp.inFile()
            if(kind=="Skill"):
                tempEmp.addSkill(abilID,abilLvl)
                self.initUI("Employee",empID) #either no change or done, go back to main page
            else:
                tempEmp.addInt(abilID,abilLvl)
                self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1       
        
    def newAbil(self,kind,empID="",abilLvl=""):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        if(kind=="Int"):
            what="Interest"
        else:
            what="Skill"
        titleLb=Label(activeFr,text="Create New "+what)
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)
            
        self.v=StringVar()
        valEntry=Entry(activeFr,textvariable=self.v)
        valEntry.icursor(END)
        valEntry.grid(column=0,row=1,sticky=W+E,columnspan=2)
        valEntry.focus_set()
        trEv=0 #not sure why it won't work without this, but doesn't like 
        #something to do with the events - first lambda variable absorbs "event"

        fn="lambda trEv=trEv, self=self, empID=empID, kind=kind, abilLvl=abilLvl: self.newAbilCallback(1,empID,kind,abilLvl)"
        rtnfn='lambda trEv=trEv, self=self, empID=empID: self.initUI("Employee",empID)'
        okBut=Button(activeFr,text="OK",command=eval(fn))
        canBut=Button(activeFr,text="Cancel",command=eval(rtnfn))
        okBut.grid(column=0,row=2,sticky=W)
        canBut.grid(column=1,row=2,sticky=E)
        valEntry.bind('<Return>',eval(fn))
        valEntry.bind('<Escape>',eval(rtnfn))


        return activeFr    
        
    def empAbilAdd(self,kind,empID):
        activeFr=Frame(self.rightFr)
        activeFr.columnconfigure(0,weight=1)
        if(kind=="Int"):
            what="Interest"
        else:
            what="Skill"
        titleLb=Label(activeFr,text="Add "+str(what)+" and level")
        titleLb.grid(column=0,row=0,sticky=W+E,columnspan=2)

        if(kind=="Skill"):
            skVals = self.skillList.retListItems()
            if skVals == []:
                abilID=""
                abilName=""
            else:
                abilID,abilName=zip(*skVals) #unpack into lists
        else:
            intVals = self.intList.retListItems()
            if intVals ==[]:
                abilID=""
                abilName=""
            else:                
                abilID,abilName=zip(*intVals) #unpack into lists

        revDict=dict(zip(abilName,abilID))
        self.v2=StringVar()
        box = Combobox(activeFr, textvariable=self.v2)

        box['values'] = "New "+what,
        if not abilName == "":
            box['values'] +=abilName
        box.grid(column=0,row=1,sticky=W+E)

        self.v=StringVar()
        box = Combobox(activeFr, textvariable=self.v)
        box['values'] = (0,1,2,3,4)
        box.set(0)
        box.grid(column=1,row=1,sticky=W+E)


        if(kind=="Skill"):
            expl=Label(activeFr,text="Legend:\n"+"0 - no knowledge of task\n"+
                                "1 - exposed to the task\n"+"2 - can only perform task with assistance\n"+
                                "3 - can perform task without assistance\n"+"4 - can train others")
        else:
            expl=Label(activeFr,text="Legend:\n"+"0 - no interest\n"+
                                "1 - light interest\n"+"2 - medium interest\n"+
                                "3 - strong interest\n"+"4 - obsessed")
        expl.grid(column=0,row=4,sticky=W+E,columnspan=2)                


        okBut=Button(activeFr,text="OK",
                     command=lambda empID=empID, kind=kind: self.empAddAbilCallback(kind,empID,revDict))
        canBut=Button(activeFr,text="Cancel",
                      command=lambda empID=empID: self.initUI("Employee",empID))
        okBut.grid(column=0,row=3,sticky=W+E)
        canBut.grid(column=1,row=3,sticky=W+E)

        return activeFr    

    def newAbilCallback(self,chg,empID,kind,abilLvl):
        abilNm=self.v.get()
        tempEmp=employee(empID)
        tempEmp.inFile()
        if(abilLvl==""):
            abilLvl=0
        if(abilNm==""):
            chg=0
        if(chg==1):
            #Add new abil to master list
            if(kind=="Skill"):
                if(self.skillList.abilExist(abilNm)):
                    self.initUI("Employee",empID) #already exists, abort
                    return 1
                abilID=self.skillList.addAbil(abilNm)
                #And then update the employee file
                tempEmp.addSkill(abilID,abilLvl)
            else: #Int
                if(self.intList.abilExist(abilNm)):
                    self.initUI("Employee",empID) #already exists, abort
                    return 1
                abilID=self.intList.addAbil(abilNm)
                #And then update the employee file
                tempEmp.addInt(abilID,abilLvl)            

        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1        
            
    def NameCallback(self,chg,empID):
        newVal=self.v.get()
        if(newVal==""):
            chg=0
        if(chg==1):
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.chgName(newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1
        
    def BirthdayCallback(self,chg,empID):
        newVal=self.v.get()
        if(newVal==""):
            chg=0
        if(chg==1):
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.setBday(newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1        
        
    def TitleCallback(self,chg,empID):
        newVal=self.v.get()
        if(newVal==""):
            chg=0
        if(chg==1):
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.setTitle(newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1
        
    def EmailCallback(self,chg,empID):
        newVal=self.v.get()
        if(newVal==""):
            chg=0
        if(chg==1):
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.setEmail(newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1
        
    def WorkPhoneCallback(self,chg,empID):
        newVal=self.v.get()
        if(newVal==""):
            chg=0
        if(chg==1):
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.setWork(newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1   

    def CellPhoneCallback(self,chg,empID):
        newVal=self.v.get()
        if(newVal==""):
            chg=0
        if(chg==1):
            tempEmp=employee(empID)
            tempEmp.inFile()
            tempEmp.setCell(newVal)
        self.initUI("Employee",empID) #either no change or done, go back to main page
        return 1           
        
        
        
        
################################################################################################
###########################HINT:Scroll Frame####################################################        
################################################################################################        
        
        
        
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def scrollTop(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        
    def mwheel(self,amt):
        self.canvas.yview_scroll(amt,"units")
        
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.grid(row=0,column=1,sticky=N+S)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.grid(row=0,column=0,sticky=N+S+W+E)
        vscrollbar.rowconfigure(0,weight=1)
        canvas.rowconfigure(0,weight=1)
        canvas.columnconfigure(0,weight=1)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        
        self.canvas=canvas        
        
        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)






def main():
  
    root = Tk()
    #root.geometry("900x900+100+100")
    #w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #root.geometry("%dx%d+0+0" % (w, h))
    root.wm_state('zoomed')
    app = MainGui(root)
    def shutdown_ttk_repeat():
        root.eval('::ttk::CancelRepeat')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", shutdown_ttk_repeat) #make sure everything gets shut down properly
    root.mainloop()  

if __name__ == '__main__':
    main()  
    
