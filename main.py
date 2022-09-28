import random
import math
from tkinter import *

root = Tk()

TIME_STEP = 50
SPACE = 22


def getRandomColor():
    n = hex(random.randrange(0, 256 * 256 * 256 - 1)).replace('0x', '#')
    if len(n) < 7:
        n = n[0] + '0' * (7 - len(n)) + n[1:]
    return n


def createLine(cords, color):
    return c.create_line(cords.x0y0x1y1, fill=color)


def createRectangle(cords, color):
    return c.create_rectangle(cords.x0y0x1y1,
                              fill=color)


def deleteObjFromCanvas(obj):
    c.delete(obj)


def updateCanvas(time, event, *arg):
    c.after(TIME_STEP * time, event, *arg)


def setCords(target, place):
    c.coords(target, place)


def moveFigeure(time, figure, cords):
    updateCanvas(time, setCords, figure, cords)


def setFill(time, rectangle, color):
    updateCanvas(time, lambda: c.itemconfig(rectangle, fill=color))


def rotateCords(t, pointCords, centerCords, mode='rect'):
    if mode == 'rect':
        newX = centerCords.x + (pointCords.x - centerCords.x) * math.cos(t) - \
               (pointCords.y - centerCords.y) * math.sin(t)
        newY = centerCords.y + (pointCords.x - centerCords.x) * math.sin(t) + \
               (pointCords.y - centerCords.y) * math.cos(t)
        return Cords([newX, newY, pointCords.width, pointCords.height])
    elif mode == 'x0y0':
        newX = centerCords.x + (pointCords.x - centerCords.x) * math.cos(t) - \
               (pointCords.y - centerCords.y) * math.sin(t)
        newY = centerCords.y + (pointCords.x - centerCords.x) * math.sin(t) + \
               (pointCords.y - centerCords.y) * math.cos(t)
        return Cords([newX, newY, pointCords.x1, pointCords.y1], 'x1y1')
    elif mode == 'x1y1':
        newX = centerCords.x + (pointCords.x1 - centerCords.x) * math.cos(t) - \
               (pointCords.y1 - centerCords.y) * math.sin(t)
        newY = centerCords.y + (pointCords.x1 - centerCords.x) * math.sin(t) + \
               (pointCords.y1 - centerCords.y) * math.cos(t)
        return Cords([pointCords.x, pointCords.y, newX, newY], 'x1y1')


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


class Button:

    def __init__(self, cords, name, text=None, color='green'):
        self.onClickEvent = None
        if text is None:
            text = f'Button {name}'
        self.name = name
        self.color = color
        self.cords = cords
        self.rectangle = createRectangle(cords, color)
        self.text = c.create_text(cords.x + cords.width / 2, cords.y + cords.height / 2, text=text)
        self.childList = []

    def addChild(self, name):
        self.childList.append(name)

    def removeChild(self, name):
        self.childList.remove(name)

    def clearChildList(self):
        self.childList = []

    def onClick(self, event):
        self.onClickEvent = event

    def moveIt(self, cords, time=1):
        self.cords = cords
        moveFigeure(time, self.rectangle, self.cords.x0y0x1y1)
        moveFigeure(time, self.text, [self.cords.x + self.cords.width // 2, self.cords.y + self.cords.height // 2])

    def clicked(self, e):
        event = Event(e)
        event.btnPressed = self
        setFill(1, self.rectangle, 'yellow')
        setFill(4, self.rectangle, self.color)
        if self.onClickEvent:
            self.onClickEvent(event)

    def __del__(self):
        self.clearChildList()
        deleteObjFromCanvas(self.rectangle)
        deleteObjFromCanvas(self.text)


class Line:

    def __init__(self, cords, name, color='green'):
        self.onClickEvent = None
        self.name = name
        self.color = color
        self.cords = cords
        self.line = createLine(cords, color)

    def onClick(self, event):
        self.onClickEvent = event

    def clicked(self, e):
        event = Event(e)
        event.btnPressed = self
        if self.onClickEvent:
            self.onClickEvent(event)

    def moveIt(self, cords, time=1):
        self.cords = cords
        moveFigeure(time, self.line, self.cords.x0y0x1y1)

    def __del__(self):
        deleteObjFromCanvas(self.line)


class MyCanvas:

    def __init__(self, cords):
        self.cords = cords
        self.objectArray = {}
        self.rectangle = createRectangle(cords, "gray")
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
        setFill(time, self.rectangle, color)


class ButtonField(MyCanvas):

    def addObject(self, object):
        self.objectArray[object.name] = object

    def clicked(self, event):
        for i in self.objectArray.values():
            if self.checkCords(event, i.cords):
                i.clicked(event)


class DrowingCanvas(ButtonField):

    def __init__(self, cords):
        super().__init__(cords)
        self.onClickEvent = None

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


class State:

    def __init__(self):
        self.pointQueue = ['first', 'second', 'third', 'center']
        self.existPointList = []
        self.curPointNum = 0
        self.curPoint = self.pointQueue[self.curPointNum]
        self.linesList = []
        self.textCorner = StringVar()

    def addLine(self, lineName):
        self.linesList.append(lineName)

    def removeLine(self, lineName):
        if lineName in self.linesList:
            self.linesList.remove(lineName)

    def nextPoint(self):
        self.curPointNum = (self.curPointNum + 1) % len(self.pointQueue)
        self.existPointList.append(self.curPoint)
        self.curPoint = self.pointQueue[self.curPointNum]

    def setCurPoint(self, name):
        self.curPoint = name
        self.curPointNum = self.pointQueue.index(name)


state = State()
c = Canvas(root, width=30 * SPACE + 100, height=500, bg='white')
myBtnField = ButtonField(Cords([0, 0, 30 * SPACE + 100, 500]))
myDC = DrowingCanvas(Cords([15 * SPACE, 0, 15 * SPACE + 100, 500]))
myBtnField.addObject(myDC)
MAINPOINT = ['first', 'second', 'third']


def btnClick(event):
    state.setCurPoint(event.btnPressed.name)


def deleteLine(firstPoint, secondPoint):
    try:
        for i in firstPoint.childList:
            for j in secondPoint.childList:
                if j == i:
                    state.removeLine(i)
                    myDC.objectArray.pop(i)
                    del j
                    del i
                    return 0
    finally:
        return 0


def addNewLine(firstPoint, secondPoint):
    deleteLine(firstPoint, secondPoint)
    newLine = Line(Cords([secondPoint.cords.x, secondPoint.cords.y, firstPoint.cords.x, firstPoint.cords.y], 'x1y1'),
                   firstPoint.name + secondPoint.name,
                   'red')
    state.addLine(newLine.name)
    firstPoint.addChild(newLine.name)
    secondPoint.addChild(newLine.name)

    return newLine


def deletePointWithChild(pointName):
    if pointName in myDC.objectArray:
        for k in myDC.objectArray[pointName].childList:
            state.removeLine(k)
            myDC.objectArray.pop(k, None)
        state.existPointList.remove(pointName)
        myDC.objectArray.pop(pointName)
        del pointName


def newClick(event):
    n = 0
    try:
        n = int(state.textCorner.get())
    except:
        n = 90

    for i in MAINPOINT:
        for j in range(n):
            myDC.objectArray[i].moveIt(
                rotateCords(math.radians(1), myDC.objectArray[i].cords, myDC.objectArray['center'].cords), j
            )
    for i in state.linesList:
        for j in range(n):
            myDC.objectArray[i].moveIt(
                rotateCords(math.radians(1), myDC.objectArray[i].cords, myDC.objectArray['center'].cords, 'x0y0'), j
            )
            myDC.objectArray[i].moveIt(
                rotateCords(math.radians(1), myDC.objectArray[i].cords, myDC.objectArray['center'].cords, 'x1y1'), j
            )


def clickHandler(event):
    deletePointWithChild(state.curPoint)
    newPoint = Button(event.cords, state.curPoint, color=getRandomColor())
    state.nextPoint()

    for i in state.existPointList:
        if (i in MAINPOINT) and newPoint.name in MAINPOINT and i != newPoint.name:
            myDC.addObject(addNewLine(myDC.objectArray[i], newPoint))

    newPoint.onClick(btnClick)
    myDC.addObject(newPoint)


def SpeedUP(event):
    global TIME_STEP
    if TIME_STEP > 5:
        TIME_STEP = TIME_STEP - 5


def SpeedDown(event):
    global TIME_STEP
    TIME_STEP = TIME_STEP + 5

def App():
    myDC.setOnClick(clickHandler)

    buttonRotate = Button(Cords([30, 30, 100, 50]), 'rotator', 'Rotate')
    buttonRotate.onClick(newClick)
    myBtnField.addObject(buttonRotate)

    buttonUp = Button(Cords([30, 130, 40, 30]), 'upBtn', 'Up')
    buttonUp.onClick(SpeedUP)
    myBtnField.addObject(buttonUp)

    buttonDown = Button(Cords([90, 130, 40, 30]), 'downBtn', 'Down')
    buttonDown.onClick(SpeedDown)
    myBtnField.addObject(buttonDown)

    rotateControlEdit = Entry(width=50, textvariable=state.textCorner)
    rotateControlEdit.pack()

    def key(event):
        print("pressed", repr(event.char))

    def callback(event):
        myBtnField.clicked(event)

    c.bind("<Key>", key)
    c.bind("<Button-1>", callback)


c.focus_set()
c.pack()

App()

root.mainloop()