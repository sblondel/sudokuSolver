#!/usr/bin/env python

from Box import Box
from Column import Column
from Row import Row
from Bloc import Bloc

class Grid:
    def __init__(self):
        self.boxList = []
        self.columnList = []
        self.rowList = []
        self.blocList = []

    def initializeGrid(self):
        for i in range(0, 9):
            column = Column(i)
            self.columnList.append(column)
            row = Row(i)
            self.rowList.append(row)
            bloc = Bloc(i)
            self.blocList.append(bloc)
        for i in range(0, 81):
            columnIndex = i % 9
            rowIndex = int(i / 9)
            blocIndex = int(columnIndex / 3) + 3 * int(rowIndex / 3)
            box = Box(i, columnIndex, rowIndex, blocIndex)
            self.boxList.append(box)
            self.columnList[columnIndex].addBox(i)
            self.rowList[rowIndex].addBox(i)
            self.blocList[blocIndex].addBox(i)

    def reSet(self):
        for i in range(0, 81):
            self.boxList[i].reSet()

    def makeGridGrey(self, value):
        for i in range(0, len(self.boxList)):
            if (self.boxList[i].value == value):
                for j in range(0, 9):
                    self.boxList[self.columnList[self.boxList[i].column].boxList[j]].makeBoxGrey()
                    self.boxList[self.rowList[self.boxList[i].row].boxList[j]].makeBoxGrey()
                    self.boxList[self.blocList[self.boxList[i].bloc].boxList[j]].makeBoxGrey()

        print "color for", value
        for i in range(0, 9):
            for j in range(0, 9):
                if (self.boxList[self.rowList[i].boxList[j]].color == "white"):
                    print " ",
                elif (self.boxList[self.rowList[i].boxList[j]].color == "grey"):
                    print ".",
                else:
                    print "*",
            print " "
        

    def solve(self):
        conti = True
        while (conti):
            conti = False
            for i in range(1, 10):
                self.makeGridGrey(i)
                for j in range(0, 8):
                    column = self.columnList[j]
                    row = self.rowList[j]
                    bloc = self.blocList[j]
                    nColumnWhite = 0
                    nRowWhite = 0
                    nBlocWhite = 0
                    columnBoxID = -1
                    rowBoxID = -1
                    blocBoxID = -1
                    for k in range(0, 8):
                        if (self.boxList[column.boxList[k]].color == "white"):
                            nColumnWhite = nColumnWhite + 1
                            columnBoxID = column.boxList[k]
                        if (self.boxList[row.boxList[k]].color == "white"):
                            nRowWhite = nRowWhite + 1
                            rowBoxID = row.boxList[k]
                        if (self.boxList[bloc.boxList[k]].color == "white"):
                            nBlocWhite = nBlocWhite + 1
                            blocBoxID = bloc.boxList[k]

                    if (nColumnWhite == 1):
                        self.boxList[columnBoxID].setValue(i)
                        conti = True
                    if (nRowWhite == 1):
                        self.boxList[rowBoxID].setValue(i)
                        conti = True
                    if (nBlocWhite == 1):
                        self.boxList[blocBoxID].setValue(i)
                        conti = True

                self.reSet()

        print "Done!"

    def printGrid(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if (self.boxList[self.rowList[i].boxList[j]].value == 0):
                    print "*",
                else:
                    print self.boxList[self.rowList[i].boxList[j]].value,
            print " "

    def readGrid(self):
        j = raw_input('Please enter the numbers one at a time, following the row order:')
        if (len(j) == 1 and j != " "):
            self.boxList[0].setValue(int(j))
        for i in range(1, 81):
            j = raw_input('?')
            if (len(j) == 1 and j != " "):
                self.boxList[i].setValue(int(j))
            
        

grid = Grid()
grid.initializeGrid()
grid.readGrid()
#grid.boxList[15].setValue(1)
#grid.boxList[20].setValue(2)
#grid.boxList[30].setValue(5)
#grid.boxList[48].setValue(7)
#grid.boxList[72].setValue(8)
grid.printGrid()
grid.solve()
grid.printGrid()
