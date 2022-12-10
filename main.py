import random
import time
from myKinter import *

root = Tk()
SPACE = 22


class State:

    def __init__(self):
        self.pointQueue = ['first', 'second', 'third', 'center']
        self.dotList = []
        self.existPointList = []
        self.curPointNum = 0
        # self.curPoint = self.pointQueue[self.curPointNum]
        self.curPoint = None
        self.linesList = []
        self.textCorner = StringVar()
        self.xValue = StringVar()
        self.yValue = StringVar()
        self.x1Value = StringVar()
        self.y1Value = StringVar()
        self.zValue = StringVar()
        self.pointList = np.array([])
        self.linePoints = []
        self.lastPoint = []

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
        return n

    state = State()
    c = Canvas(root, width=30 * SPACE + 100, height=500, bg='white')
    myRoot = Root(root, c)
    myRoot.setRoot()

    myBtnField = ButtonField(Cords([0, 0, 30 * SPACE + 100, 500]))
    myDC = DrowingCanvas(Cords([15 * SPACE, 0, 15 * SPACE + 100, 500]))
    myDC.displayGrid()
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
        newLine = Line(Cords([secondPoint.cords.x, secondPoint.cords.y, firstPoint.cords.x, firstPoint.cords.y],
                             'x1y1'),
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
    myDC.displayGrid()
    myBtnField.addObject(myDC)

    def createDotLine(first, second):
        if first:
            return Line(Cords([first[0], first[1], second[0], second[1]], 'x1y1'),
                        'line' + str(first[0]) + str(second[0]), 'red')
        else:
            return None

    def calculate(step, points):
        pointCords = myDC.calculateCordsByXY(points[-1][0], points[-1][1])
        state.linesList.append(createDotLine(state.lastPoint, pointCords))
        state.lastPoint = pointCords

        for i in state.linePoints:
            myRoot.canvas.delete(i)
        for t in step:
            pointCords = calculatePoint(t, points)
            state.linePoints.append(myDC.createPoint(pointCords[0], pointCords[1], width=1, color='#9fc5e8'))

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

    def addPoint(temp, color):
        myDC.createPoint(temp[0], temp[1], color=color)
        if state.pointList.size:
            state.pointList = np.append(state.pointList, [temp], axis=0)
        else:
            state.pointList = np.array([temp])
        calculate(steps, state.pointList)

    state = State()
    steps = np.arange(0, 1, 0.001)
    tempPointList = np.array([[0, 0], [3, 5], [4, 10]])
    for tempPoint in tempPointList:
        addPoint(tempPoint, 'blue')

    def clickHandler(event):
        addPoint(myDC.calculateXYbyCords(event.cords.x, event.cords.y), 'green')

    def addHandler(event):
        addPoint([int(state.xValue.get()), int(state.yValue.get())], 'red')
        state.xValue.set('')
        state.yValue.set('')

    def App():

        XLable = Lable(Cords([30, 70, 100, 30]), 'input x:')
        EditXCord = MyEdit(cords=Cords([30, 100, 100, 30]), textvariable=state.xValue)

        YLable = Lable(Cords([160, 70, 100, 30]), 'input y:')
        EditYCord = MyEdit(cords=Cords([160, 100, 100, 30]), textvariable=state.yValue)

        buttonAdd = Button(Cords([300, 100, 50, 30]), 'addButton', 'Add')
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


def thirdLab():

    c = Canvas(root, width=40 * SPACE, height=800, bg='white')
    myRoot = Root(root, c)
    myRoot.setRoot()

    quadrilateral = [] #фигура

    myBtnField = ButtonField(Cords([0, 0, 40 * SPACE, 800]))
    myDC = DrowingCanvas(Cords([1 * SPACE, 200, 25 * SPACE, 550]))
    myDC.displayGrid3D()
    myBtnField.addObject(myDC)

    def createDotLine(first, second):
        if first:
            return Line(Cords([first[0], first[1], second[0], second[1]], 'x1y1'),
                        'line' + str(first[0]) + str(second[0]), 'red')
        else:
            return None

    def calculate(step, points):
        pointCords = myDC.calculateCordsByXY(points[-1][0], points[-1][1])
        state.linesList.append(createDotLine(state.lastPoint, pointCords))
        state.lastPoint = pointCords

        for i in state.linePoints:
            myRoot.canvas.delete(i)
        for t in step:
            pointCords = calculatePoint(t, points)
            state.linePoints.append(myDC.createPoint(pointCords[0], pointCords[1], width=1, color='#9fc5e8'))

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

    def addPoint(temp, color):
        myDC.create3DPoint(np.array(temp), color=color)
        if state.pointList.size:
            state.pointList = np.append(state.pointList, [temp], axis=0)
        else:
            state.pointList = np.array([temp])
        # calculate(steps, state.pointList)

    def editPoint(cords, color):
        temp = [cords[0], cords[1]]
        dot = myDC.createPointNew(cords[0], cords[1], pointCords=cords)
        print('dot', dot)
        print(dot.pointCords)
        displayPointList(dot)
        state.dotList.append(dot)

    def setEditMode(event):
        print('[setEditMode] event.btnPressed.pointCords', event.btnPressed.pointCords)

    STEP = 30

    # def displayPointList(point):
    #     print('point {dot}', point)
    #     print(point.pointCords)
    #     lable = Lable(Cords([20 * SPACE, 20 + STEP * len(state.existPointList), 100, 10]), str(len(state.existPointList))+str(point.pointCords))
    #     lable.pointCords = point.pointCords
    #     lable.connectedPoint = point
    #     lable.onClick(setEditMode)
    #     myBtnField.addObject(lable)
    #     state.existPointList.append(lable)

    state = State()
    steps = np.arange(0, 1, 0.001)
    for i in range(16):
        state.existPointList.append([random.randrange(1, i+2), random.randrange(9, 15), random.randrange(1, i+2)])
        addPoint(state.existPointList[i], 'red')
    flag = True
    jopa = []
    for i in range(1, 15, 2):
        if flag:
            myDC.create3DLine(np.array(state.existPointList[i]), np.array(state.existPointList[i + 1]), 'green')
            myDC.create3DLine(np.array(state.existPointList[i]), np.array(state.existPointList[i - 1]), 'blue')
            flag = False
            jopa = [i+1, i-1]
        else:
            myDC.create3DLine(np.array(state.existPointList[i]), np.array(state.existPointList[jopa[0]]), 'green')
            myDC.create3DLine(np.array(state.existPointList[i]), np.array(state.existPointList[jopa[1]]), 'blue')
            flag = True


    def displayPointList():
        for i in range(len(state.existPointList)):
            print('[display]', i, ':', state.existPointList[i])
            lable = Lable(Cords([30 * SPACE, 70 + STEP * i, 100, STEP - 5]), str(i)+' : '+str(state.existPointList[i]))

    def clickHandler(event):
        # addPoint(myDC.calculateXYbyCords(event.cords.x, event.cords.y), 'green')
        displayPointList()

    def addHandler(event):
        editPoint([float(state.xValue.get()), float(state.yValue.get()), 0], 'red')
        state.xValue.set('')
        state.yValue.set('')

    def App():

        NumLable = Lable(Cords([1 * SPACE, 70, 3 * SPACE, 30]), 'number of point:')
        EditNumber = MyEdit(cords=Cords([1 * SPACE, 100, 3 * SPACE, 30]), textvariable=state.xValue)

        XLable = Lable(Cords([5 * SPACE, 70, 3 * SPACE, 30]), 'input x:')
        EditXCord = MyEdit(cords=Cords([5 * SPACE, 100, 3 * SPACE, 30]), textvariable=state.xValue)

        YLable = Lable(Cords([9 * SPACE, 70, 3 * SPACE, 30]), 'input y:')
        EditYCord = MyEdit(cords=Cords([9 * SPACE, 100, 3 * SPACE, 30]), textvariable=state.yValue)

        ZLable = Lable(Cords([13 * SPACE, 70, 3 * SPACE, 30]), 'input z:')
        EditZCord = MyEdit(cords=Cords([13 * SPACE, 100, 3 * SPACE, 30]), textvariable=state.zValue)

        buttonAdd = Button(Cords([17 * SPACE, 100, 4 * SPACE, 30]), 'addButton', 'Add')
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

    # i can concatinate dots into figure and figure into dificult stucture


def forthLab():
    c = Canvas(root, width=30 * SPACE + 100, height=500, bg='white')
    myRoot = Root(root, c)
    myRoot.setRoot()

    state = State()
    # steps = np.arange(0, 1, 0.001)

    myBtnField = ButtonField(Cords([0, 0, 30 * SPACE + 100, 500]))
    myDC = DrowingCanvas(Cords([0, 240, 30 * SPACE + 100, 260]))
    myDC.displayGrid()
    myBtnField.addObject(myDC)

    def createRandomLine(name):
        return Line(Cords([random.randrange(myDC.cords.x, myDC.cords.x1), random.randrange(myDC.cords.y, myDC.cords.y1),
                           random.randrange(myDC.cords.x, myDC.cords.x1), random.randrange(myDC.cords.y, myDC.cords.y1)],
                          'x1y1'),
                    name, 'red')

    def addLine(temp):
        tempLine = createRandomLine(str(temp))
        rect = state.curPoint
        state.linesList.append(tempLine)
        k = 4
        while k:
            if not(rect.checkCords(tempLine.cords.x0y0) + rect.checkCords(tempLine.cords.x1y1)):
                print('Ks & Ke тривиально виден')
                state.linesList.append(Line(Cords([tempLine.cords.x, tempLine.cords.y,
                                                   tempLine.cords.x1, tempLine.cords.y1], 'x1y1'), 'name', 'blue'))
                break
            elif rect.checkCords(tempLine.cords.x0y0) & rect.checkCords(tempLine.cords.x1y1):
                print('Ks & Ke тривиально не виден')
                break
            else:
                if not(rect.checkCords(tempLine.cords.x0y0)):
                    tempLine.cords = Cords([tempLine.cords.x1, tempLine.cords.y1, tempLine.cords.x, tempLine.cords.y],
                                           'x1y1')
                if rect.checkCords(tempLine.cords.x0y0) & 8:
                    tempLine.cords.y = formulaY(tempLine, rect.cords[0])
                    tempLine.cords.x = rect.cords[0]
                elif rect.checkCords(tempLine.cords.x0y0) & 4:
                    tempLine.cords.y = formulaY(tempLine, rect.cords[2])
                    tempLine.cords.x = rect.cords[2]
                elif rect.checkCords(tempLine.cords.x0y0) & 2:
                    tempLine.cords.x = formulaX(tempLine, rect.cords[1])
                    tempLine.cords.y = rect.cords[1]
                else:
                    tempLine.cords.x = formulaX(tempLine, rect.cords[3])
                    tempLine.cords.y = rect.cords[3]
            tempLine.cords = Cords([tempLine.cords.x, tempLine.cords.y, tempLine.cords.x1, tempLine.cords.y1], 'x1y1')
            k -= 1

    def formulaY(line, X):
        t = (X - line.cords.x) / line.cords.width
        return line.cords.y + t * line.cords.height

    def formulaX(line, Y):
        t = (Y - line.cords.y) / line.cords.height
        return line.cords.x + t * line.cords.width

    def addRectangle(temp):
        sP = myDC.calculateCordsByXY(temp[0], temp[1])
        eP = myDC.calculateCordsByXY(temp[2], temp[3])
        state.curPoint = Rectangle([sP[0], sP[1], eP[0], eP[1]])  #сборщик мусора удалит старый объект со всем внутри

    def clickHandler(event):
        addLine(myDC.calculateXYbyCords(event.cords.x, event.cords.y))

    def addHandler(event):
        addRectangle([float(state.xValue.get()), float(state.yValue.get()),
                      float(state.x1Value.get()), float(state.y1Value.get())])
        state.xValue.set('')
        state.yValue.set('')
        state.x1Value.set('')
        state.y1Value.set('')

    def App():

        XLable = Lable(Cords([30, 70, 100, 30]), 'input x:')
        EditXCord = MyEdit(cords=Cords([30, 100, 100, 30]), textvariable=state.xValue)

        YLable = Lable(Cords([160, 70, 100, 30]), 'input y:')
        EditYCord = MyEdit(cords=Cords([160, 100, 100, 30]), textvariable=state.yValue)

        X1Lable = Lable(Cords([30, 130, 100, 30]), 'input x:')
        EditX1Cord = MyEdit(cords=Cords([30, 170, 100, 30]), textvariable=state.x1Value)

        Y1Lable = Lable(Cords([160, 130, 100, 30]), 'input y:')
        EditY1Cord = MyEdit(cords=Cords([160, 170, 100, 30]), textvariable=state.y1Value)

        buttonAdd = Button(Cords([300, 100, 50, 30]), 'addButton', 'Add')
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


def fifthLab():

    cubePoint = np.array([[-5, -5, -5], [5, -5, -5], [5, 5, -5], [-5, 5, -5],
                          [-5, -5, 5], [5, -5, 5], [5, 5, 5], [-5, 5, 5]], np.float)  # figure

    faces = np.array([[0, 1, 2, 3], [5, 4, 7, 6], [4, 0, 3, 7], [1, 5, 6, 2], [4, 5, 1, 0], [3, 2, 6, 7]])

    def cross(a, b):
        return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

    def createDotLine(first, second):
        return myDC.create3DLine(first, second, color='red', width=3)

    def createFace(points):
        b, a, d, c = points[0], points[1], points[2], points[3]
        state.linesList.append(createDotLine(a, b))
        state.linesList.append(createDotLine(b, c))
        state.linesList.append(createDotLine(c, d))
        state.linesList.append(createDotLine(a, d))

    def createOutline(points):
        a, b, c, d = points[0], points[1], points[2], points[3]

        v1 = b[0] - a[0], b[1] - a[1], b[2] - a[2]
        v2 = c[0] - a[0], c[1] - a[1], c[2] - a[2]
        n = cross(v1, v2)
        if n[2] < 0:
            return
        else:
            coords = np.array([b, a, d, c])
            createFace(coords)

    def render(points, faces):
        clearFigure()
        coords = []
        for point in points:
            coords.append(point)
        for face in faces:
            createOutline((coords[face[0]], coords[face[1]], coords[face[2]], coords[face[3]]))

    def clearFigure():
        for i in state.linesList:
            myDC.deleteLine(i)
        state.linesList.clear()

    #///////////////////////////////////////////////////////////////////////////

    c = Canvas(root, width=40 * SPACE, height=800, bg='white')
    myRoot = Root(root, c)
    myRoot.setRoot()

    myBtnField = ButtonField(Cords([0, 0, 40 * SPACE, 800]))
    myDC = DrowingCanvas(Cords([1 * SPACE, 200, 25 * SPACE, 550]))
    myDC.displayGrid3D(0, mode='hide')
    myBtnField.addObject(myDC)
    state = State()

    def clickHandler(event):
        render(cubePoint, faces)

    def specHandler(event):
        for i in range(len(cubePoint)):
            cubePoint[i] = rotate3D(cubePoint[i], float(state.xValue.get()), 'x')
            cubePoint[i] = rotate3D(cubePoint[i], float(state.yValue.get()), 'y')
            cubePoint[i] = rotate3D(cubePoint[i], float(state.zValue.get()), 'z')
        render(cubePoint, faces)


    def App():

        XLable = Lable(Cords([5 * SPACE, 70, 3 * SPACE, 30]), 'input x:')
        EditXCord = MyEdit(cords=Cords([5 * SPACE, 100, 3 * SPACE, 30]), textvariable=state.xValue)

        YLable = Lable(Cords([9 * SPACE, 70, 3 * SPACE, 30]), 'input y:')
        EditYCord = MyEdit(cords=Cords([9 * SPACE, 100, 3 * SPACE, 30]), textvariable=state.yValue)

        ZLable = Lable(Cords([13 * SPACE, 70, 3 * SPACE, 30]), 'input z:')
        EditZCord = MyEdit(cords=Cords([13 * SPACE, 100, 3 * SPACE, 30]), textvariable=state.zValue)

        buttonAdd = Button(Cords([17 * SPACE, 100, 4 * SPACE, 30]), 'addButton', 'Add')
        buttonAdd.onClick(specHandler)

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

fifthLab()
root.mainloop()
