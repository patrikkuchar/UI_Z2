import random
import time

global finished

class Node:
    ##pozicia
    ##posledny pohyb
    ##hlbka
    ##pozicia prazdneho miesta
    ##rodic node
    ##pole deti
    def __init__(self, stage, lastMove, depth, parent):
        self.stage = stage
        self.lastMove = lastMove #1=hore | -1=dole | -2=vlavo | 2=vpravo
        self.depth = depth
        self.parent = parent

    def setStage(self, stage):
        self.stage = stage

    def writeDepth(self, mode):
        if mode == 0:
            print("Rovnaký uzol v 1. strome nájdený v hĺbke: " + str(self.depth))
        elif mode == 1:
            print("Rovnaký uzol v 2. strome nájdený v hĺbke: " + str(self.depth))
        elif mode == 2:
            print("Výsledný uzol nájdený v hĺbke: " + str(self.depth))

    def getStage(self):
        return self.stage

    def getLastMove(self):
        return self.lastMove

    def getDepth(self):
        return self.depth

    def getParentNode(self):
        return self.parent


def generator(moves, startStage):
    for i in range(moves):
        r = random.randrange(4)
        if r == 0:
            stage = LEFT(startStage)
        elif r == 1:
            stage = RIGHT(startStage)
        elif r == 2:
            stage = UP(startStage)
        else:
            stage = DOWN(startStage)

        if stage != "":
            startStage = stage
    return startStage

def writeMove(moves):
    searching_stage = stageOnStart
    for move in moves:
        print(searching_stage[:3].replace("0", " "))
        print(searching_stage[3:6].replace("0", " ") + "  " + printMove(move))
        print(searching_stage[6:].replace("0", " ") + "\n")

        if move == 1:
            searching_stage = UP(searching_stage)
        elif move == -1:
            searching_stage = DOWN(searching_stage)
        elif move == -2:
            searching_stage = LEFT(searching_stage)
        elif move == 2:
            searching_stage = RIGHT(searching_stage)

    print(searching_stage[:3].replace("0", " "))
    print(searching_stage[3:6].replace("0", " "))
    print(searching_stage[6:].replace("0", " "))


def printMove(move):
    if move == 1:
        return "UP"
    if move == -1:
        return "DOWN"
    if move == -2:
        return "LEFT"
    if move == 2:
        return "RIGHT"
    return ""

def makePath(nodeFrom_start, nodeFrom_finish):
    global finished
    pathS = []
    pathF = []

    if nodeFrom_finish == None:
        nodeFrom_start.writeDepth(2)
    else:
        nodeFrom_start.writeDepth(0)
        nodeFrom_finish.writeDepth(1)


    searchingNode = nodeFrom_start
    while searchingNode.getParentNode() != None:
        pathS.append(searchingNode.getLastMove())
        searchingNode = searchingNode.getParentNode()

    if nodeFrom_finish != None:
        searchingNode = nodeFrom_finish
        while searchingNode.getParentNode() != None:
            pathF.append(-searchingNode.getLastMove())
            searchingNode = searchingNode.getParentNode()

    allPaths.append(pathS[-1::-1] + pathF)

    finished = True



def check2(node, mode, edge):
    stage = node.getStage()
    for searchingNode in edge[mode][0]:
        if searchingNode.getStage() == stage:
            if mode == 1:
                makePath(node, searchingNode)
            else:
                makePath(searchingNode, node)
            break

def check1(node):
    if node.getStage() == stageOnFinish:
        makePath(node, None)


def tree2(mode, edge):
    modeR = (mode + 1) % 2

    if len(edge[mode]) == 1:
        edge[mode].append([])
    while edge[mode][0] != []:
        parentNode = edge[mode][0].pop(0)

        leftMove = LEFT(parentNode.getStage())
        rightMove = RIGHT(parentNode.getStage())
        upMove = UP(parentNode.getStage())
        downMove = DOWN(parentNode.getStage())


        if leftMove != "" and not (backTrackLock and parentNode.getLastMove() == 2) and not finished:
            leftNode = Node(leftMove, -2, parentNode.getDepth() + 1, parentNode)
            edge[mode][1].append(leftNode)
            check2(leftNode, modeR, edge)
        if rightMove != "" and not (backTrackLock and parentNode.getLastMove() == -2) and not finished:
            rightNode = Node(rightMove, 2, parentNode.getDepth() + 1, parentNode)
            edge[mode][1].append(rightNode)
            check2(rightNode, modeR, edge)
        if upMove != "" and not (backTrackLock and parentNode.getLastMove() == -1) and not finished:
            upNode = Node(upMove, 1, parentNode.getDepth() + 1, parentNode)
            edge[mode][1].append(upNode)
            check2(upNode, modeR, edge)
        if downMove != "" and not (backTrackLock and parentNode.getLastMove() == 1) and not finished:
            downNode = Node(downMove, -1, parentNode.getDepth() + 1, parentNode)
            edge[mode][1].append(downNode)
            check2(downNode, modeR, edge)

    edge[mode].pop(0)

    if backTrackLock:
        numOfAllNodes[0][mode] += len(edge[mode][0])
    else:
        numOfAllNodes[1][mode] += len(edge[mode][0])

    if not finished:
        tree2(modeR, edge)

def tree1(edge):
    if len(edge) == 1:
        edge.append([])
    while edge[0] != []:
        parentNode = edge[0].pop(0)

        leftMove = LEFT(parentNode.getStage())
        rightMove = RIGHT(parentNode.getStage())
        upMove = UP(parentNode.getStage())
        downMove = DOWN(parentNode.getStage())

        if leftMove != "" and not (backTrackLock and parentNode.getLastMove() == 2):
            leftNode = Node(leftMove, -2, parentNode.getDepth() + 1, parentNode)
            edge[1].append(leftNode)
            check1(leftNode)
        if rightMove != "" and not (backTrackLock and parentNode.getLastMove() == -2):
            rightNode = Node(rightMove, 2, parentNode.getDepth() + 1, parentNode)
            edge[1].append(rightNode)
            check1(rightNode)
        if upMove != "" and not (backTrackLock and parentNode.getLastMove() == -1):
            upNode = Node(upMove, 1, parentNode.getDepth() + 1, parentNode)
            edge[1].append(upNode)
            check1(upNode)
        if downMove != "" and not (backTrackLock and parentNode.getLastMove() == 1):
            downNode = Node(downMove, -1, parentNode.getDepth() + 1, parentNode)
            edge[1].append(downNode)
            check1(downNode)

    edge.pop(0)

    if backTrackLock:
        numOfAllNodes[2] += len(edge[0])
    else:
        numOfAllNodes[3] += len(edge[0])


    if not finished:
        tree1(edge)








def LEFT(stage):
    index = stage.index('0')
    if index%3 == 2:
        return ""

    c = stage[index+1]
    return stage[:index] + c + "0" + stage[index+2:]

def RIGHT(stage):
    index = stage.index('0')
    if index % 3 == 0:
        return ""

    c = stage[index - 1]
    return stage[:index-1] + "0" + c  + stage[index+1:]

def UP(stage):
    index1 = stage.index('0')
    if index1 > 5:
        return ""

    index2 = index1 + 3
    c = stage[index2]
    return stage[:index1] + c + stage[index1+1:index2] + "0" + stage[index2+1:]

def DOWN(stage):
    index1 = stage.index('0')
    if index1 < 3:
        return ""

    index2 = index1 - 3
    c = stage[index2]
    return stage[:index2] + "0" + stage[index2+1:index1] + c + stage[index1+1:]



def init2(startStage, finishStage):
    edge = [[], []]
    startNode = Node(startStage,0,0,None)
    finishNode = Node(finishStage,0,0,None)
    edge[0].append([startNode])
    edge[1].append([finishNode])
    tree2(0, edge)

def init1(startStage):
    edge = []
    startNode = Node(startStage,0,0,None)
    edge.append([startNode])
    tree1(edge)




##--------------testovanie-----------
allPaths = []
numOfAllNodes = [[0,0],[0,0],0,0]
stageOnStart = "123456780"
stageOnFinish = generator(50, stageOnStart)

print("Začiatočný stav: " + stageOnStart)
print("Konečný stav: " + stageOnFinish)

finished = False
backTrackLock = True
print("\nObojsmerné hľadanie so zakázaným krokom späť (čiastočné zamedzenie duplicity):")
start_timer = time.time()
init2(stageOnStart,stageOnFinish)
end_timer = time.time()
print("Počet uzlov v 1. strome: " + str(numOfAllNodes[0][0]))
print("Počet uzlov v 2. strome: " + str(numOfAllNodes[0][1]))
print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
print("Počet krokov k cieľu: " + str(len(allPaths[0])))


finished = False
backTrackLock = False
print("\nObojsmerné hľadanie s možným krokom späť (duplicita):")
start_timer = time.time()
init2(stageOnStart,stageOnFinish)
end_timer = time.time()
print("Počet uzlov v 1. strome: " + str(numOfAllNodes[1][0]))
print("Počet uzlov v 2. strome: " + str(numOfAllNodes[1][1]))
print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
print("Počet krokov k cieľu: " + str(len(allPaths[1])))


finished = False
backTrackLock = True
print("\nHľadanie do šírky so zakázaným krokom späť (čiastočné zamedzenie duplicity):")
start_timer = time.time()
init1(stageOnStart)
end_timer = time.time()
print("Počet uzlov v strome: " + str(numOfAllNodes[2]))
print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
print("Počet krokov k cieľu: " + str(len(allPaths[2])))



finished = False
backTrackLock = False
print("\nHľadanie do šírky s možným krokom späť (duplicita):")
start_timer = time.time()
init1(stageOnStart)
end_timer = time.time()
print("Počet uzlov v strome: " + str(numOfAllNodes[3]))
print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
print("Počet krokov k cieľu: " + str(len(allPaths[3])))