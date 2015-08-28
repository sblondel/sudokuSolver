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
        for i in range(0, 81):
            if (self.boxList[i].value == value):
                self.makeColumnGrey(self.boxList[i].column)
                self.makeRowGrey(self.boxList[i].row)
                self.makeBlocGrey(self.boxList[i].bloc)
        self.makeAdvancedGridGrey()

    def makeAdvancedGridGrey(self):
        for i in range(0, 9):
            previousColumnID = -1
            previousRowID = -1
            columnID = -1
            rowID = -1
            nWhites = 0
            sameColumn = True
            sameRow = True
            for j in range(0, 9):
                if (self.boxList[self.blocList[i].boxList[j]].color == "white"):
                    nWhites = nWhites + 1
                    columnID = self.boxList[self.blocList[i].boxList[j]].column
                    rowID = self.boxList[self.blocList[i].boxList[j]].row
                    if (nWhites > 1):
                        if (columnID != previousColumnID and sameColumn):
                            sameColumn = False
                        if (rowID != previousRowID and sameRow):
                            sameRow = False
                    previousColumnID = columnID
                    previousRowID = rowID
            if (nWhites > 1 and sameColumn):
                self.makeColumnExcludeBlocGrey(columnID, i)
            if (nWhites > 1 and sameRow):
                self.makeRowExcludeBlocGrey(rowID, i)

    def algorithmOne(self):
        conti = False
        standard = range(1, 10)
        for i in range(0, 9):
            column = self.columnList[i]
            columnPresent = []
            row = self.rowList[i]
            rowPresent = []
            for j in range(0, 9):
                box = self.boxList[column.boxList[j]]
                if (box.color == "black"):
                    columnPresent.append(box.value)
                box = self.boxList[row.boxList[j]]
                if (box.color == "black"):
                    rowPresent.append(box.value)
            columnMissing = list(set(standard) - set(columnPresent))
            rowMissing = list(set(standard) - set(rowPresent))
            for j in range(0, 9):
                bloc = self.blocList[j]
                
                if (self.blocPartOfColumn(j, i)):
                    blocPresent = []
                    for k in range(0, 9):
                        box = self.boxList[bloc.boxList[k]]
                        if (box.color == "black"):
                            blocPresent.append(box.value)
                    intersection = self.intersect(blocPresent, columnMissing)
                    outsideBlocEmpty = []
                    for k in range(0, 9):
                        box = self.boxList[column.boxList[k]]
                        if (box.value == 0 and not self.boxInBloc(box.index, bloc.index)):
                            outsideBlocEmpty.append(box.index)
                    if (len(outsideBlocEmpty) == len(intersection)):
                        values = list(set(columnMissing) - set(intersection))
                        for k in range(0, len(values)):
                            self.makeGridGrey(values[k])
                            for l in range(0, len(outsideBlocEmpty)):
                                box = self.boxList[outsideBlocEmpty[l]]
                                box.makeBoxGrey()
                            if (self.fillGrid(values[k])):
                                conti = True
                            
                if (self.blocPartOfRow(j, i)):
                    blocPresent = []
                    for k in range(0, 9):
                        box = self.boxList[bloc.boxList[k]]
                        if (box.color == "black"):
                            blocPresent.append(box.value)
                    intersection = self.intersect(blocPresent, rowMissing)
                    outsideBlocEmpty = []
                    for k in range(0, 9):
                        box = self.boxList[row.boxList[k]]
                        if (box.value == 0 and not self.boxInBloc(box.index, bloc.index)):
                            outsideBlocEmpty.append(box.index)
                    if (len(outsideBlocEmpty) == len(intersection)):
                        values = list(set(rowMissing) - set(intersection))
                        for k in range(0, len(values)):
                            self.makeGridGrey(values[k])
                            for l in range(0, len(outsideBlocEmpty)):
                                box = self.boxList[outsideBlocEmpty[l]]
                                box.makeBoxGrey()
                            if (self.fillGrid(values[k])):
                                conti = True
        return conti
    
    def intersect(self, a, b):
        return list(set(a) & set(b))
                    
    def blocPartOfColumn(self, blocID, columnID):
        if (blocID % 3 == int(columnID/3)): 
            return True
        else:
            return False
        
    def blocPartOfRow(self, blocID, rowID):
        if (int(blocID/3) == int(rowID/3)): 
            return True
        else:
            return False

    def boxInBloc(self, boxID, blocID):
        isIn = False
        for i in range(0, 9):
            if (boxID == self.blocList[blocID].boxList[i]):
                isIn = True
        return isIn

    def makeColumnGrey(self, id):
        for j in range(0, 9):
            self.boxList[self.columnList[id].boxList[j]].makeBoxGrey()
                    
    def makeColumnExcludeBlocGrey(self, columnID, blocID):
        for j in range(0, 9):
            boxID = self.columnList[columnID].boxList[j]
            if (not self.boxInBloc(boxID, blocID)):
                self.boxList[boxID].makeBoxGrey()

    def makeRowGrey(self, id):
        for j in range(0, 9):
            self.boxList[self.rowList[id].boxList[j]].makeBoxGrey()
                    
    def makeRowExcludeBlocGrey(self, rowID, blocID):
        for j in range(0, 9):
            boxID = self.rowList[rowID].boxList[j]
            if (not self.boxInBloc(boxID, blocID)):
                self.boxList[boxID].makeBoxGrey()

    def makeBlocGrey(self, id):
        for j in range(0, 9):
            self.boxList[self.blocList[id].boxList[j]].makeBoxGrey()
            
    def fillGrid(self, value):
        conti = False
        for j in range(0, 9):
            column = self.columnList[j]
            row = self.rowList[j]
            bloc = self.blocList[j]
            nColumnWhite = 0
            nRowWhite = 0
            nBlocWhite = 0
            columnBoxID = -1
            rowBoxID = -1
            blocBoxID = -1
            for k in range(0, 9):
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
                self.boxList[columnBoxID].setValue(value)
                self.makeColumnGrey(self.boxList[columnBoxID].column)
                self.makeRowGrey(self.boxList[columnBoxID].row)
                self.makeBlocGrey(self.boxList[columnBoxID].bloc)
                conti = True
            if (nRowWhite == 1):
                self.boxList[rowBoxID].setValue(value)
                self.makeColumnGrey(self.boxList[rowBoxID].column)
                self.makeRowGrey(self.boxList[rowBoxID].row)
                self.makeBlocGrey(self.boxList[rowBoxID].bloc)
                conti = True
            if (nBlocWhite == 1):
                self.boxList[blocBoxID].setValue(value)
                self.makeColumnGrey(self.boxList[blocBoxID].column)
                self.makeRowGrey(self.boxList[blocBoxID].row)
                self.makeBlocGrey(self.boxList[blocBoxID].bloc)
                conti = True

        self.reSet()
        return conti
        
    def solve(self):
        conti = True
        while (conti):
            conti = False
            for i in range(1, 10):
                self.makeGridGrey(i)
                if (self.fillGrid(i)):
                    conti = True
        if (self.algorithmOne()):
            self.solve()

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
grid.printGrid()
grid.solve()
grid.printGrid()
