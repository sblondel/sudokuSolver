#!/usr/bin/env python

class Row:
    def __init__(self, index):
        self.index = index
        self.boxList = []

    def addBox(self, i):
        self.boxList.append(i)
