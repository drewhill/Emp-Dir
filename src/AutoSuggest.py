# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 01:05:15 2013

Graciously stolen from an online forum
"""

import Tkinter as tk
import re

class AutoSug:
    MAX_LIST_SIZE = 10

    BASE_FRAME = {'bd'     : 2          ,
                  'bg'     : 'white'    ,
                  'class'  : 'ComboBox' ,
                  'relief' : tk.SUNKEN  }
  
    ENTRY      = {'bd'     : 2          ,
                  'relief' : tk.FLAT    }
    
    LABEL      = {'anchor' : tk.W       ,
                  'bg'     : 'white'    }
    
    LIST       = {'bd'     : 1          ,
                  'bg'     : 'black'    }
    
    LABEL_ENTER_FG = 'white'
    LABEL_ENTER_BG = '#0A246A'
    LABEL_LEAVE_FG = 'black'
    LABEL_LEAVE_BG = 'white'

    def __init__(self, parent):
        
        def valTrace(name, index, mode):
            if self.__showingList: self.__hideList()
            if self.__val.get():
                match = re.compile('^%s' % self.__val.get()).match
                items = []
                for item in self.__items:
                    if match(item): items.append(item)
                    if len(items) == self.MAX_LIST_SIZE: break
                if items: self.__showList(items)
        
        self.__items       = []
        self.__parent      = parent
        self.__showingList = False
        
        self.__baseFrame = tk.Frame(self.__parent, cnf = self.BASE_FRAME)
        self.__baseFrame.columnconfigure(0, weight = 1)
        
        self.__val = tk.StringVar(master = self.__baseFrame)
        self.__val.trace('w', valTrace)
        
        self.__entry     = tk.Entry (self.__baseFrame, cnf = self.ENTRY)        
        self.__entry['textvariable'] = self.__val
        self.__entry.grid(row = 0, column = 0, stick=tk.NSEW)              
    
    def __showList(self, items):
        def labelEnter(event):
            event.widget.focus_set()
            event.widget['bg'] = self.LABEL_ENTER_BG
            event.widget['fg'] = self.LABEL_ENTER_FG
    
        def labelLeave(event):
            event.widget['bg'] = self.LABEL_LEAVE_BG
            event.widget['fg'] = self.LABEL_LEAVE_FG
        
        def labelSelect(event):
            self.__val.set( event.widget.cget('text') )
            self.__hideList()
        
        self.__showingList = True
        
        topLevel    = self.__parent.winfo_toplevel()
        self.__list = tk.Frame(topLevel, cnf = self.LIST)
        
        self.__list.bind('<ButtonRelease-1>', self.__hideList)
        self.__list.columnconfigure(0, weight = 1)
        self.__list.grab_set()
        self.__list.place(in_ = self.__baseFrame, relx = 0, rely = 1,
                          relwidth = 1, anchor = tk.NW, bordermode = tk.OUTSIDE)
        
        if len(items) > self.MAX_LIST_SIZE: items = items[:self.MAX_LIST_SIZE]
    
        for i, item in enumerate(items):
            new = tk.Label(self.__list, cnf = self.LABEL)
            
            new['text'] = item
            
            new.bind('<Enter>'          , labelEnter )
            new.bind('<Leave>'          , labelLeave )
            
            new.bind('<Return>'         , labelSelect)
            new.bind('<ButtonRelease-1>', labelSelect)
            
            new.bind('<Tab>',             self.__hideList)
            new.grid(row = i, column = 0, stick = tk.EW)

    def __hideList(self, event=None):
        self.__showingList = False
        self.__list.destroy()
    
    def get(self):
        return self.__val.get()
    
    def addItems(self, *Items):
        self.__items.extend(Items)
    
    def grid(self, *args, **kw):
        return self.__baseFrame.grid(*args, **kw)
    def focus_set(self):
        return self.__entry.focus_set()
    def pack(self, *args, **kw):
        return self.__baseFrame.pack(*args, **kw)
    def place(self, *args, **kw):
        return self.__baseFrame.place(*args, **kw)

def TestSuite():
    root = tk.Tk()
    root.geometry('500x500')
    
    c = AutoSug(root)
    c.addItems('hello','hh','lllop','ll','p','oiuyhg','poiujk','poiuyf','tgvygv')
    c.focus_set()
    c.grid()
    
    root.mainloop()

if __name__ == '__main__':
    TestSuite()