#!/usr/bin/env python

class Box:
    def __init__(self, index, column, row, bloc):
        self.index = index
        self.column = column
        self.row = row
        self.bloc = bloc
        self.value = 0
        self.color = "white"

    def makeBoxGrey(self):
        if (self.color == "white"):
            self.color = "grey"

    def setValue(self, value):
        self.value = value
        self.color = "black"

    def reSet(self):
        if (self.value == 0):
            self.color = "white"
        
