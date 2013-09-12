# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 01:05:49 2013

@author: drewhill
"""

from Tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("one") # default value

w = OptionMenu(master, variable, "one", "two", "three")
w.pack()

mainloop()