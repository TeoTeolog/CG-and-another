import math
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
    def __init__(self, cords, mode='rec'):
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

    def clicked(self, event):
        print(event)

    def setColor(self, color, time=1):
        setFill(_root.canvas, time, self.rectangle, color)


class ButtonField(MyCanvas):

    def addObject(self, object):
        self.objectArray[object.name] = object

    def clicked(self, event):
        for i in self.objectArray.values():
            if self.checkCords(event, i.cords):
                i.clicked(event)

GRID_STEP = 20

class DrowingCanvas(ButtonField):

    def __init__(self, cords):
        super().__init__(cords)
        self.onClickEvent = None
        self.rectangle = createRectangle(_root.canvas, cords, '#eeeeee')
        # рисуем сетку
        for i in range(cords.width//GRID_STEP):
            createLine(_root.canvas, Cords([cords.x + GRID_STEP * i, cords.y, 0, cords.height]),
                       fill='#bcbcbc')
            _root.canvas.create_text(cords.x + GRID_STEP * i + 5, cords.y1 - GRID_STEP//2, text=i-1)

        for i in range(cords.height//GRID_STEP):
            createLine(_root.canvas, Cords([cords.x, cords.y1 - GRID_STEP * i, cords.width,0]),
                       fill='#bcbcbc')
            _root.canvas.create_text(cords.x + GRID_STEP//2, cords.y1 - GRID_STEP * i + 5, text=i - 1)

        self.Oy = createLine(_root.canvas,
                             Cords([cords.x + GRID_STEP, cords.y + GRID_STEP, 0, cords.height - GRID_STEP]),
                             fill='black', arrow=FIRST)
        self.Ox = createLine(_root.canvas, Cords([cords.x, cords.y1 - GRID_STEP, cords.width - GRID_STEP, 0]),
                             fill='black', arrow=LAST)

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

    def calculateCords(self, x, y):
        resX = (x + 1) * GRID_STEP + self.cords.x - 2
        resY = self.cords.y1 - (y + 1) * GRID_STEP - 2
        return [resX,resY]

    def calculateNearCords(self, x, y):
        resX = round((x - self.cords.x) / GRID_STEP) - 1
        resY = round((self.cords.y + self.cords.height - y) / GRID_STEP) - 1
        return self.calculateCords(resX, resY)

    def calculateXYbyCords(self, x, y):
        resX = (x - self.cords.x) / GRID_STEP - 1
        resY = (self.cords.y + self.cords.height - y) / GRID_STEP - 1
        return [resX,resY]

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


class MyEdit:

    def __init__(self, cords, textvariable):
        self.editObject = Entry(textvariable=textvariable)
        _root.canvas.create_window(cords.x + cords.width // 2, cords.y + cords.height // 2,
                                    window=self.editObject, height=cords.height, width=cords.width)

    # maybe I will imagen some functional for this
    def pack(self):
        pass