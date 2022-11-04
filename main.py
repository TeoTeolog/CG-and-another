import random
import numpy as np
from myKinter import *

root = Tk()
SPACE = 22


class State:

    def __init__(self):
        self.pointQueue = ['first', 'second', 'third', 'center']
        self.existPointList = []
        self.curPointNum = 0
        self.curPoint = self.pointQueue[self.curPointNum]
        self.linesList = []
        self.textCorner = StringVar()
        self.xValue = StringVar()
        self.yValue = StringVar()
        self.pointList = None

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


def firstLab():
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


    def getRandomColor():
        n = hex(random.randrange(0, 256 * 256 * 256 - 1)).replace('0x', '#')
        if len(n) < 7:
            n = n[0] + '0' * (7 - len(n)) + n[1:]
        print('color:',n)
        return n


    state = State()
    c = Canvas(root, width=30 * SPACE + 100, height=500, bg='white')
    myRoot = Root(root, c)
    myRoot.setRoot()

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
        for j in range(n):
            for i in MAINPOINT:
                myDC.objectArray[i].moveIt(
                    rotateCords(math.radians(1), myDC.objectArray[i].cords, myDC.objectArray['center'].cords), j
                )
            for i in state.linesList:
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
        if myRoot.getTimeStep() > 5:
            myRoot.setTimeStep(myRoot.getTimeStep() - 5)


    def SpeedDown(event):
        myRoot.setTimeStep(myRoot.getTimeStep() + 5)


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

        rotateControlEdit = MyEdit(cords=Cords([30, 210, 100, 30]), textvariable=state.textCorner)

        def key(event):
            print("pressed", repr(event.char))

        def callback(event):
            myBtnField.clicked(event)

        c.bind("<Key>", key)
        c.bind("<Button-1>", callback)

    c.focus_set()
    c.pack()

    App()


def secondLab():

    c = Canvas(root, width=30 * SPACE + 100, height=500, bg='white')
    myRoot = Root(root, c)
    myRoot.setRoot()

    myBtnField = ButtonField(Cords([0, 0, 30 * SPACE + 100, 500]))
    myDC = DrowingCanvas(Cords([0, 200, 30 * SPACE + 100, 300]))
    myBtnField.addObject(myDC)

    def createDot(x, y, color='red', width=5):
        myRoot.canvas.create_oval(x, y, x + width, y + width, width=0,
                                  fill=color)

    def createPoint(x, y, color='red', width=5):
        cords = myDC.calculateCords(x, y)
        createDot(cords[0], cords[1], color, width)
        return [x, y]

    def calculate(step, points):
        for t in step:
            pointCords = calculatePoint(t, points)
            print('{\npointCords, pointCords[0], pointCords[1] :\n', pointCords,
                  pointCords[0], pointCords[1], '\n}\n', 't :', t)
            createPoint(pointCords[0], pointCords[1], width=1, color='#9fc5e8')

    def calculatePoint(t, points):
        newPoints = points
        while len(newPoints) > 1:
            newPoints = Casteljo(t, newPoints)
        return newPoints[0]

    def Casteljo(t, points):
        newPoints = []
        for i in range(0, len(points) - 1):
            point = (1 - t) * points[i] + t * points[i + 1]
            newPoints += [point]
        return newPoints

    state = State()
    step = np.arange(0, 1, 0.001)
    state.pointList = np.array([[0, 0], [3, 5], [4, 10]])
    for i in state.pointList:
        createPoint(i[0], i[1])

    calculate(step, state.pointList)

    def clickHandler(event):
        newPoint = myDC.calculateNearCords(event.cords.x, event.cords.y)
        createDot(newPoint[0], newPoint[1], 'green')
        temp = [myDC.calculateXYbyCords(newPoint[0], newPoint[1])]
        tempPointList = np.append(state.pointList, temp, axis=0)
        state.pointList = tempPointList
        state.xValue.set('')
        state.yValue.set('')
        calculate(step, state.pointList)

    def addHandler(event):
        temp = [createPoint(int(state.xValue.get()), int(state.yValue.get()))]
        tempPointList = np.append(state.pointList, temp, axis=0)
        state.pointList = tempPointList
        state.xValue.set('')
        state.yValue.set('')
        calculate(step, state.pointList)

    def App():

        XLable = Lable(Cords([30, 70, 100, 30]), 'input x:')
        EditXCord = MyEdit(cords=Cords([30, 100, 100, 30]), textvariable=state.xValue)

        YLable = Lable(Cords([160, 70, 100, 30]), 'input y:')
        EditYCord = MyEdit(cords=Cords([160, 100, 100, 30]), textvariable=state.yValue)

        buttonAdd = Button(Cords([360, 100, 50, 30]), 'downBtn', 'Down')
        buttonAdd.onClick(addHandler)
        myBtnField.addObject(buttonAdd)

        myDC.setOnClick(clickHandler)

        def key(event):
            print("pressed", repr(event.char))

        def callback(event):
            myBtnField.clicked(event)

        c.bind("<Key>", key)
        c.bind("<Button-1>", callback)

    App()

    c.focus_set()
    c.pack()


secondLab()
root.mainloop()
