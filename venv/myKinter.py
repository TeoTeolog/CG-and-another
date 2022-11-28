import math
import numpy as np
from tkinter import *

_root = None

class Root:
    def __init__(self, root, mainCanvas):
        self.root = root
        self.canvas = mainCanvas
        self.TIME_STEP = 50

    def setRoot(self):
        global _root
        _root = self
        print(_root)

    def setTimeStep(self, n):
        self.TIME_STEP = n

    def getTimeStep(self):
        return self.TIME_STEP

    def createDot(self, x, y, color='red', width=5):
        print('[root.createDot] crods:', x, y)
        return self.canvas.create_oval(x, y, x + width, y + width, width=0,
                                         fill=color)

# _root = Root(None, None)
#
def createLine(canvas, cords, **options):
    return canvas.create_line(cords.x0y0x1y1, options)

#
def createRectangle(canvas, cords, color):
    return canvas.create_rectangle(cords.x0y0x1y1,
                              fill=color)

#
def deleteObjFromCanvas(canvas, obj):
    canvas.delete(obj)

#
def updateCanvas(canvas, time, event, *arg):
    canvas.after(_root.TIME_STEP * time, event, *arg)

#
def setCords(canvas, target, place):
    canvas.coords(target, place)

#
def moveFigeure(canvas, time, figure, cords):
    updateCanvas(canvas, time, setCords, canvas, figure, cords)

#
def setFill(canvas, time, rectangle, color):
    updateCanvas(canvas, time, lambda: canvas.itemconfig(rectangle, fill=color))

class Event:
    def __init__(self, event):
        self.e = event
        self.cords = Cords([self.e.x, self.e.y, 40, 40])


class Cords:
    def __init__(self, cords, mode='rec'): #mode='x1y1'
        self.x = cords[0]
        self.y = cords[1]
        if mode == 'rec':
            self.width = cords[2]
            self.height = cords[3]
        else:
            self.width = cords[2] - cords[0]
            self.height = cords[3] - cords[1]
        self.x1 = self.x + self.width
        self.y1 = self.y + self.height
        self.x0y0x1y1 = [self.x, self.y, self.x1, self.y1]
        self.all = [self.x, self.y, self.width, self.height]
        self.x0y0 = [self.x, self.y]
        self.x1y1 = [self.x1, self.y1]


class MyCanvas:

    def __init__(self, cords):
        self.cords = cords
        self.objectArray = {}
        self.rectangle = createRectangle(_root.canvas, cords, "gray")
        self.name = str(cords.x)

    @staticmethod
    def checkCords(cords, rectangleCords):
        if rectangleCords.x + rectangleCords.width > cords.x > rectangleCords.x \
                and rectangleCords.y + rectangleCords.height > cords.y > rectangleCords.y:
            return True
        return False

    # def clicked(self, event):
    #     print(event)

    def setColor(self, color, time=1):
        setFill(_root.canvas, time, self.rectangle, color)


class ButtonField(MyCanvas):

    def addObject(self, object):
        self.objectArray[object.name] = object

    def clicked(self, event):
        for i in self.objectArray.values():
            if self.checkCords(event, i.cords):
                i.clicked(event)

def xRotateMatrix(a):
    return np.array([
        [1, 0, 0],
        [0, math.cos(math.radians(a)), -1 * math.sin(math.radians(a))],
        [0, math.sin(math.radians(a)), math.cos(math.radians(a))]
    ])

def yRotateMatrix(a):
    return np.array([
        [math.cos(math.radians(a)), 0, math.sin(math.radians(a))],
        [0, 1, 0],
        [-1 * math.sin(math.radians(a)), 0, math.cos(math.radians(a))]
    ])

def zRotateMatrix(a):
    return np.array([
        [math.cos(math.radians(a)), -1 * math.sin(math.radians(a)), 0],
        [math.sin(math.radians(a)), math.cos(math.radians(a)), 0],
        [0, 0, 1]
    ])

def calculatePlotCords(cords):
    a = 35
    temp = cords.dot(yRotateMatrix(a))
    temp = temp.dot(xRotateMatrix(-1 * a))
    return [temp[0],temp[1]]

GRID_STEP = 20

class DrowingCanvas(ButtonField):

    def __init__(self, cords):
        super().__init__(cords)
        self.onClickEvent = None
        self.cords = cords
        self.rectangle = createRectangle(_root.canvas, cords, '#eeeeee')
        self.startDot = [cords.x, cords.y1]

    def displayGrid(self):
        cords = self.cords
        endPoint = [cords.width//GRID_STEP, cords.height//GRID_STEP]
        for i in range(cords.width//GRID_STEP):
            createLine(_root.canvas, Cords([self.startDot[0] + GRID_STEP * i, self.startDot[1],
                                            self.startDot[0] + GRID_STEP * i, self.startDot[1] - GRID_STEP * endPoint[1]],
                                           'x1y1'),
                       fill='#bcbcbc')
            _root.canvas.create_text(self.startDot[0] + GRID_STEP * i - GRID_STEP//3, self.startDot[1] - GRID_STEP + GRID_STEP//2, text=i-1)

        for i in range(cords.height//GRID_STEP):
            createLine(_root.canvas, Cords([self.startDot[0], self.startDot[1] - GRID_STEP * i,
                                            self.startDot[0] + GRID_STEP * endPoint[0], self.startDot[1] - GRID_STEP * i],
                                           'x1y1'),
                       fill='#bcbcbc')
            _root.canvas.create_text(self.startDot[0] + 2 * GRID_STEP//3, self.startDot[1] - GRID_STEP * i - GRID_STEP + GRID_STEP//2, text=i - 1)

        self.Oy = createLine(_root.canvas,
                             Cords([cords.x + GRID_STEP, cords.y + GRID_STEP//2, 0, cords.height]),
                             fill='black', arrow=FIRST)
        _root.canvas.create_text(cords.x + GRID_STEP + 5, cords.y + GRID_STEP - 5, text='Y')

        self.Ox = createLine(_root.canvas, Cords([cords.x, cords.y1 - GRID_STEP, cords.width - GRID_STEP, 0]),
                             fill='black', arrow=LAST)
        _root.canvas.create_text(cords.x + cords.width - GRID_STEP + 5, cords.y1 - GRID_STEP - 5, text='X')


    def getColor(self, a):
        n = hex(a * 255 * 124).replace('0x', '#')
        if len(n) < 7:
            n = n[0] + '0' * (7 - len(n)) + n[1:]
        return n

    def create3DLine(self, start_point, end_point, color='black', arrow=None):
        plotCordsB = calculatePlotCords(start_point)
        plotCordsE = calculatePlotCords(end_point)
        return  createLine(_root.canvas,
                   Cords([self.startDot[0] + plotCordsB[0] * GRID_STEP, self.startDot[1] - plotCordsB[1] * GRID_STEP,
                          self.startDot[0] + plotCordsE[0] * GRID_STEP, self.startDot[1] - plotCordsE[1] * GRID_STEP],
                         mode='x1y1'),
                   fill=color, arrow=arrow)

    def displayGrid3D(self):
        cords = self.cords
        endpoint = 15
        XYZ = np.array([[endpoint, 0, 0], [0, endpoint, 0], [0, 0, endpoint]])
        self.startDot=[cords.x + GRID_STEP * 12, cords.y1 - GRID_STEP * 13]
        sample = [[1,0,0],[0,1,0],[0,0,1]]
        for k in sample:
            for j in sample:
                for i in range(1, endpoint):
                    if j!=k:
                        tempB = np.array([i * j[0], i * j[1], i * j[2]])
                        tempE = np.array([i * j[0] + k[0] * endpoint, i * j[1] + k[1] * endpoint, i * j[2] + k[2] * endpoint])
                        self.create3DLine(tempB, tempE, color='#bcbcbc')
        for i in XYZ:
            plotCords = calculatePlotCords(i)
            self.create3DLine(np.array([0, 0, 0]), i, arrow=LAST)
            _root.canvas.create_text(self.startDot[0] + plotCords[0] * GRID_STEP, self.startDot[1] - plotCords[1] * GRID_STEP, text=i)

    def setOnClick(self, event):
        self.onClickEvent = event

    def clicked(self, e):
        for i in self.objectArray.values():
            if self.checkCords(e, i.cords) and i.onClickEvent:
                i.clicked(e)
                return i
        event = Event(e)
        event.canvasPressed = self
        if self.onClickEvent:
            self.onClickEvent(event)
        return None

    def calculateCordsByXY(self, x, y):
        resX = (x + 1) * GRID_STEP  + self.startDot[0]
        resY = self.startDot[1] - (y + 1) * GRID_STEP
        return [resX,resY]

    def calculateNearCords(self, x, y):
        resX = round((x - self.cords.x) / GRID_STEP) - 1
        resY = round((self.cords.y + self.cords.height - y) / GRID_STEP) - 1
        return self.calculateCords(resX, resY)

    def calculateXYbyCords(self, x, y):
        resX = (x - self.cords.x) / GRID_STEP - 1
        resY = (self.cords.y + self.cords.height - y) / GRID_STEP - 1
        return [resX,resY]

    def createDot(self, x, y, color='red', width=5):
        return _root.createDot(x, y, color, width)

    def createPoint(self, x, y, color='red', width=5):
        cords = self.calculateCordsByXY(x, y)
        return self.createDot(cords[0], cords[1], color, width)

    def create3DPoint(self, cords, color='red', width=5):
        res_cords = calculatePlotCords(cords)
        return self.createPoint(res_cords[0], res_cords[1], color, width)

class Button:

    def __init__(self, cords, name, text=None, color='green'):
        self.onClickEvent = None
        if text is None:
            text = f'Button {name}'
        self.name = name
        self.color = color
        self.cords = cords
        self.rectangle = createRectangle(_root.canvas, cords, color)
        self.text = _root.canvas.create_text(cords.x + cords.width / 2, cords.y + cords.height / 2, text=text)
        self.childList = []

    def addChild(self, name):
        self.childList.append(name)

    def removeChild(self, name):
        self.childList.remove(name)

    def clearChildList(self):
        self.childList = []

    def onClick(self, event, **eventArgs):
        self.onClickEvent = event
        self.eventArgs = eventArgs

    def moveIt(self, cords, time=1):
        self.cords = cords
        moveFigeure(_root.canvas, time, self.rectangle, self.cords.x0y0x1y1)
        moveFigeure(_root.canvas, time, self.text, [self.cords.x + self.cords.width // 2, self.cords.y + self.cords.height // 2])

    def clicked(self, e):
        event = Event(e)
        event.btnPressed = self
        setFill(_root.canvas, 1, self.rectangle, 'yellow')
        setFill(_root.canvas, 4, self.rectangle, self.color)
        print( self.eventArgs)
        if self.onClickEvent:
            if self.eventArgs:
                self.onClickEvent(event, self.eventArgs)
            else:
                self.onClickEvent(event)

    def __del__(self):
        self.clearChildList()
        deleteObjFromCanvas(_root.canvas, self.rectangle)
        deleteObjFromCanvas(_root.canvas, self.text)


class Line:

    def __init__(self, cords, name, color='green'):
        self.onClickEvent = None
        self.name = name
        self.color = color
        self.cords = cords
        self.line = createLine(_root.canvas, cords, fill=color)

    def onClick(self, event):
        self.onClickEvent = event

    def clicked(self, e):
        event = Event(e)
        event.btnPressed = self
        if self.onClickEvent:
            self.onClickEvent(event)

    def moveIt(self, cords, time=1):
        self.cords = cords
        moveFigeure(_root.canvas, time, self.line, self.cords.x0y0x1y1)

    def __del__(self):
        deleteObjFromCanvas(_root.canvas, self.line)


class Lable:

    def __init__(self, cords, text, name=None, color='black'):
        self.onClickEvent = None
        self.name = name
        self.color = color
        self.cords = cords
        self.text = _root.canvas.create_text(cords.x + cords.width / 2, cords.y + cords.height / 2, text=text, fill=color)

    def onClick(self, event):
        self.onClickEvent = event

    def clicked(self, e):
        event = Event(e)
        event.btnPressed = self
        if self.onClickEvent:
            self.onClickEvent(event)

    def moveIt(self, cords, time=1):
        self.cords = cords
        moveFigeure(_root.canvas, time, self.text, self.cords.x0y0x1y1)

    # def __del__(self):
    #     deleteObjFromCanvas(_root.canvas, self.text)

class Rectangle:

    def __init__(self, cords, color='black'): #cords = [x,y,z]
        self.color = color
        self.cords = cords
        self.lines = []
        n = 4
        points = [[cords[0], cords[1]], [cords[0], cords[3]], [cords[2], cords[3]], [cords[2], cords[1]]]
        for i in range(0, n, 2):
            self.lines.append(
                Line(Cords([points[i][0], points[i][1], points[(n + i + 1) % n][0], points[(n + i + 1) % n][1]],
                           'x1y1'), str(i)+'-'+str((n + i + 1) % n), color))
            self.lines.append(
                Line(Cords([points[i][0], points[i][1], points[(n + i - 1) % n][0], points[(n + i - 1) % n][1]],
                           'x1y1'), str(i)+'-'+str((n + i - 1) % n), color))


    def checkCords(self, cords): # cords = [x,y]
        vis = 0
        if cords[0] < self.cords[0]:
            vis += 8
        if cords[0] > self.cords[2]:
            vis += 4
        if cords[1] > self.cords[1]:
            vis += 2
        if cords[1] < self.cords[3]:
            vis += 1
        return vis

class Dot:

    def __init__(self, cords, color='black', width=5, mode='dot', pointCords=None): #cords = [x,y,z]
        print('[Dot/init] pointCords:', pointCords)
        self.pointCords = pointCords
        self.width = width
        self.color = color
        self.cords = cords
        self.point = _root.createDot(cords[0], cords[1], color, width)
        self.visability = True

    def setVisability(self, value):
        self.visability = False
        if self.visability:
            deleteObjFromCanvas(_root.canvas, self.point)
        else:
            self.point = _root.createDot(cords[0], cords[1], color, width)

    def onClick(self, event):
        self.onClickEvent = event

    def clicked(self, e):
        event = Event(e)
        event.btnPressed = self
        if self.onClickEvent:
            self.onClickEvent(event)

    def moveIt(self, cords, time=1):
        self.cords = cords
        moveFigeure(_root.canvas, time, self.text, self.cords.x0y0x1y1)

    def __del__(self):
        deleteObjFromCanvas(_root.canvas, self.text)


class MyEdit:

    def __init__(self, cords, textvariable):
        self.editObject = Entry(textvariable=textvariable)
        _root.canvas.create_window(cords.x + cords.width // 2, cords.y + cords.height // 2,
                                    window=self.editObject, height=cords.height, width=cords.width)

    # maybe I will imagen some functional for this
    def pack(self):
        pass