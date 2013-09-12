# -*- coding: utf-8 -*-
"""
Created on Wed Sep 04 23:22:18 2013

@author: drewhill
"""

import os

from EmpClass import employee
from EmpListClass import EmpList
from ProjListClass import ProjList


class empImp:
        def __init__(self):
            self.empList = EmpList()
            self.empList.inFile()
            self.projList = ProjList()
            self.projList.inFile()
    
        def formatBday(self,val):
            if "-" in val:
               val="/".join(val.split("-"))
                #convert mm-dd to mm/dd
            return val
        
        def formatPhone(self,val):
            if "." in val:
                val="-".join(val.split("."))
            if "(" in val:
                val="".join(val.split("("))
            if ")" in val:
                val="-".join(val.split(")"))
            if " " in val[0:9]:
                firstPart="-".join(val[0:9].split(" "))
                val="".join((firstPart,val[9:val.__len__()]))
            if "-" not in val: #need to add -, assuming nnnnnnnnnn
                val="-".join((val[0:3],val[3:val.__len__()]))
                val="-".join((val[0:7],val[7:val.__len__()]))
            if "--" in val[0:10]:
                firstPart="-".join(val[0:10].split("--"))
                val="".join((firstPart,val[10:val.__len__()]))                
            return val
            
        def addToProj(self,empID,pList): 
            #projIDs,projNms=zip(*self.projList.retListItems())
            #revDict=dict(zip(projNms,projIDs))
            tempEmp = employee(empID)
            tempEmp.inFile()
            icdID = 1
            genID = 2
            waterID = 3
            skunkID = 4
            if(("icd" in pList.lower())|("ecp" in pList.lower())|("WELLNESS" in pList)):
                tempEmp.addProjOrRole(icdID)
            if(("gen" in pList.lower())|("gas" in pList.lower())|("clear" in pList)):
                tempEmp.addProjOrRole(genID)
            if("water" in pList.lower()):
                tempEmp.addProjOrRole(waterID)
            if(("skunk" in pList.lower())|("hans" in pList.lower())):
                tempEmp.addProjOrRole(skunkID)                
            if("all" in pList.lower()):
                tempEmp.addProjOrRole(icdID)
                tempEmp.addProjOrRole(genID)
                tempEmp.addProjOrRole(waterID)
                tempEmp.addProjOrRole(skunkID)
    
        def inFile(self):
            with open(os.path.join(os.getcwd(),"empImp.imp"),'r') as f:
                line=f.readline()
                line=line.rstrip("\n") #"Header"
                line=f.readline()
                line=line.rstrip("\n") #first line of data            
                while not line == "": #not EOF
                    data=line.split(",") #break out comma delimited list into array
                    #[0] - Name
                    #[1] - Email
                    #[2] - Title
                    #[3] - Birthday
                    #[4] - Business Phone
                    #[5] - Cell Phone
                    #[6] - Projects On
                    #[7] - Other
                    
                    #### Preformat data ####
                    bday = self.formatBday(data[3])
                    busPh = self.formatPhone(data[4])
                    cell = self.formatPhone(data[5])                                    
                    #Assume all others good#
                    #### Preformat data ####
                    
                    ####Add Emp and set data####
                    empID = self.empList.addEmp(data[0])
                    tempEmp = employee(empID)
                    tempEmp.inFile()
                    tempEmp.setCell(cell)
                    tempEmp.setEmail(data[1])
                    tempEmp.setWork(busPh)
                    tempEmp.setTitle(data[2])
                    tempEmp.setBday(bday)
                    ####Add Emp and set data####
                    self.addToProj(empID,data[6])
                    
                    #TODO: Add b-day support, deal with project formatting, make sure outfile works
                    line=f.readline()
                    line=line.rstrip("\n") #next line of data
                    
                    
def main():
    os.chdir(os.pardir)
    impCl = empImp()
    impCl.inFile()
    impCl.destroy()

if __name__ == '__main__':
    main()                      