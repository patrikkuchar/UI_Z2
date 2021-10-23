import random
import time

global finished, sizeX, sizeY, backTrackLock

class Node:
    ##stav
    ##posledny pohyb
    ##hlbka
    ##rodic node
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

def generateStartStage(): #funkcia vytvorí náhodny string (stav) podľa veľkosti plochy
    global sizeX, sizeY

    ##ak je veľkosť plochy väčšia ako 36, vypnem program pretože mám znaky pripravené maximálne na 36
    if sizeX * sizeY > 36:
        print("\n\n\t\t!!Príliš veľká plocha!!\n\n")
        exit()

    array = list(range(10))[1:] + list(range(ord('a'),ord('z')+1)) #list čísel od 1 po 9 a čísel od 97 po 122 (ascii hodnoty písmen 'a' až 'z')

    for i in range(len(array)):
        if i < 9: #čísla 1 - 9 premení na string čísla
            array[i] = str(array[i])
        else: #čísla 97 - 122 premení na znaky podľa ascii
            array[i] = chr(array[i])

    array_stage = array[:sizeX*sizeY-1] #z listu si zoberiem potrebný počet znakov (podľa veľkosti plochy) s jedným voľným miesto pre 0 (prázdne miesto)
    array_stage.append("0") #pridám 0
    random.shuffle(array_stage) #funkcia náhodne pomieša znaky v liste

    return "".join(array_stage) #z listu vytvorí string a vráti ho





def generator(moves, startStage): #funkcia podľa počiatočného stavu a počtu opakovaní vytvára náhodné pohyby a vďaka tomu vytvorí vylidný konečný stav
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
    return startStage #vráti vygenerovaný konečný stav

def writeAllMoves():
    ##funkcia prehľadáva cesty všetkých 4 algoritmov (ak existujú), z nich si vytvorí stavy a zobrazí ich v konzole (každý algoritmus spolu s pohybom v "jednom riadku")
    for i in range(4):
        if allPaths[i] == []:
            break
        print("\n" + str(i+1) + ". algoritmus")
        lines = []
        for y in range(sizeY):
            lines.append([])

        searching_stage = stageOnStart.replace("0", " ")
        for paths in allPaths[i]:
            for y in range(sizeY):
                lines[y].append(searching_stage[sizeX*y : sizeX*(y+1)])

            if paths == 1: #UP
                searching_stage = UP(searching_stage.replace(" ", "0")).replace("0", " ")
            elif paths == -1: #DOWN
                searching_stage = DOWN(searching_stage.replace(" ", "0")).replace("0", " ")
            elif paths == -2: #LEFT
                searching_stage = LEFT(searching_stage.replace(" ", "0")).replace("0", " ")
            else: #RIGHT
                searching_stage = RIGHT(searching_stage.replace(" ", "0")).replace("0", " ")

        for y in range(sizeY):
            lines[y].append(searching_stage[sizeX * y: sizeX * (y + 1)])

        ##vypis
        for y in range(sizeY):
            print(lines[y][0], end="")

            for n, line in enumerate(lines[y]):
                if n == 0:
                    continue
                if y == sizeY // 2:
                    print("  " + printMove(allPaths[i][n-1]) + "\t", end="")
                    if printMove(allPaths[i][n-1]) == "UP":
                        print("\t", end="")
                else:
                    print("\t\t\t", end="")



                print(line, end="")

            print()







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

    ##podmienka aby ak sa omylom zavolá táto funkcia 2-krát tak sa spracuje len raz
    if not finished:
        if nodeFrom_finish == None: #prehľadávanie do šírky
            nodeFrom_start.writeDepth(2) #funkcia vypíše informácie o hĺbke uzla
        else: #obojsmerné hľadanie
            nodeFrom_start.writeDepth(0)
            nodeFrom_finish.writeDepth(1)

        ##cyklus prehľadáva 1. strom od nájdeného uzla, po rodičoch až ku koreňu uzla a pri tom si zapisuje cestu (lastMove)
        searchingNode = nodeFrom_start
        while searchingNode.getParentNode() != None:
            pathS.append(searchingNode.getLastMove())
            searchingNode = searchingNode.getParentNode()

        ##ak nie je uzol None (obojsmerné hľadanie), tak prehľadáva 2. strom a taktiež si zapisuje cestu ale zapisuje ju naopak (* -1)
        if nodeFrom_finish != None:
            searchingNode = nodeFrom_finish
            while searchingNode.getParentNode() != None:
                pathF.append(-searchingNode.getLastMove())
                searchingNode = searchingNode.getParentNode()

        allPaths.append(pathS[-1::-1] + pathF) #cesty sa zapíšu do allPath (prvá sa zapisuje naopak aby bola v správnom poradí)

    finished = True #indikátor najdenia zhody



def check2(node, mode, edge): #kontroluje či nie je zhoda medzi uzlami
    stage = node.getStage()
    ##cyklus prechádza všetky uzly opačného stromu a hľadá zhodu v stave
    for searchingNode in edge[mode][0]:
        if searchingNode.getStage() == stage: #zhoda sa našla, zavolá sa funkcia makePath(), ktorá vytvorí cestu; parametre pošle tak aby, prvý bol z prvého stromu a 2. z 2.
            if mode == 1:
                makePath(node, searchingNode)
            else:
                makePath(searchingNode, node)
            break

def check1(node): #kontroluje či uzol nie je v koncovom stave
    if node.getStage() == stageOnFinish: #jedná sa o koncový stav, zavolá sa funkcia makePath(), ktorá vytvorí cestu; druhý parameter je None pretože máme len 1 strom
        makePath(node, None)


def tree2(mode, edge): #rekurzívna funkcia, ktorá vytvára 2 stromy = obojsmerné hľadanie
    modeR = (mode + 1) % 2 #určuje či sa prehľadáva 1. alebo 2. strom (hodnoty 0|1)

    if len(edge[mode]) == 1: #ak sa nová hĺbka začína prehľadávať - vytvorenie listu
        edge[mode].append([])
    while edge[mode][0] != []: #cyklus beží až kým sa nespracuje každý uzol v liste
        parentNode = edge[mode][0].pop(0) #získa uzol na index 0 a vymaže ho z listu

        ##získame si všetky možné pohyby
        leftMove = LEFT(parentNode.getStage())
        rightMove = RIGHT(parentNode.getStage())
        upMove = UP(parentNode.getStage())
        downMove = DOWN(parentNode.getStage())


        ##ak sú splnené všetky podmienky tak sa vytvori nový uzol a pošle sa do funkcie check2()
        ##podmienky:
        ## a) možný pohyb - nesmie byť prázdny string
        ## b) ak je zamedzenie duplikácie tak novým pohybom sa nesmieme dostať do predchadzajúceho stavu
        ## c) nesmie byť najdená zhoda (urýchlenie programu, ak sa našla zhoda)
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

    edge[mode].pop(0) #po prejdení všetkých uzlov (jednej hĺbky) vymažeme prázdny list

   # print(str(len(edge[mode][0])))

    ##zápis počtu uzlov (pre štatistiku neskôr)
    if backTrackLock:
        numOfAllNodes[0][mode] += len(edge[mode][0])
    else:
        numOfAllNodes[1][mode] += len(edge[mode][0])

    ##ak nie je nájdená zhoda, zavolá sa znova táto funckia s druhým módom (spracovanie opačného stromu)
    if not finished:
        tree2(modeR, edge)

def tree1(edge): #rekurzívna funkcia, ktorá vytvára strom = prehľadávanie do šírky
    if len(edge) == 1: #ak sa nová hĺbka začína prehľadávať - vytvorenie listu
        edge.append([])
    while edge[0] != []: #cyklus beží až kým sa nespracuje každý uzol v liste
        parentNode = edge[0].pop(0) #získa uzol na index 0 a vymaže ho z listu

        ##získame si všetky možné pohyby
        leftMove = LEFT(parentNode.getStage())
        rightMove = RIGHT(parentNode.getStage())
        upMove = UP(parentNode.getStage())
        downMove = DOWN(parentNode.getStage())

        ##ak sú splnené všetky podmienky tak sa vytvori nový uzol a pošle sa do funkcie check1()
        ##podmienky:
        ## a) možný pohyb - nesmie byť prázdny string
        ## b) ak je zamedzenie duplikácie tak novým pohybom sa nesmieme dostať do predchadzajúceho stavu
        ## c) nesmie byť najdená zhoda (urýchlenie programu, ak sa našla zhoda)
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

    edge.pop(0) #po prejdení všetkých uzlov (jednej hĺbky) vymažeme prázdny list

    ##zápis počtu uzlov (pre štatistiku neskôr)
    if backTrackLock:
        numOfAllNodes[2] += len(edge[0])
    else:
        numOfAllNodes[3] += len(edge[0])

    ##ak nie je nájdená zhoda, zavolá sa znova táto funckia - prehľadávanie ďalšej hĺbky
    if not finished:
        tree1(edge)







##pohyb vľavo
def LEFT(stage):
    index = stage.index('0')
    if index%sizeX == sizeX-1: #ak je prázdne miesto na ľavej hranici plochy - nie je možný pohyb, vracia sa prázdny string
        return ""

    c = stage[index+1]
    return stage[:index] + c + "0" + stage[index+2:] #výmena 0 so znakom, na index na ktorom má byť 0

##pohyb vpravo
def RIGHT(stage):
    index = stage.index('0')
    if index % sizeX == 0: #ak je prázdne miesto na pravej hranici plochy - nie je možný pohyb, vracia sa prázdny string
        return ""

    c = stage[index - 1]
    return stage[:index-1] + "0" + c  + stage[index+1:] #výmena 0 so znakom, na index na ktorom má byť 0

##pohyb hore
def UP(stage):
    index1 = stage.index('0')
    if index1 >= sizeX*(sizeY-1): #ak je prázdne miesto na hornej hranici plochy - nie je možný pohyb, vracia sa prázdny string
        return ""

    index2 = index1 + sizeX
    c = stage[index2]
    return stage[:index1] + c + stage[index1+1:index2] + "0" + stage[index2+1:] #výmena 0 so znakom, na index na ktorom má byť 0

##pohyb dole
def DOWN(stage):
    index1 = stage.index('0')
    if index1 < sizeX: #ak je prázdne miesto na spodnej hranici plochy - nie je možný pohyb, vracia sa prázdny string
        return ""

    index2 = index1 - sizeX
    c = stage[index2]
    return stage[:index2] + "0" + stage[index2+1:index1] + c + stage[index1+1:] #výmena 0 so znakom, na index na ktorom má byť 0


##init pre obojsmerné prehľadávanie
def init2(startStage, finishStage):
    edge = [[], []] #list novovytvorených uzlov, ktoré sa pudú ďalej spracovávavať (index 0 - 1. strom; index 1 - 2. strom)
    startNode = Node(startStage,0,0,None)
    finishNode = Node(finishStage,0,0,None)
    edge[0].append([startNode])
    edge[1].append([finishNode])
    tree2(0, edge)

##init pre prehľadávanie do šírky
def init1(startStage):
    edge = [] #list novovytvorených uzlov, ktoré sa pudú ďalej spracovávavať
    startNode = Node(startStage,0,0,None)
    edge.append([startNode])
    tree1(edge)


def testing1():
    global finished, backTrackLock
    finished = False
    backTrackLock = True
    print("\nObojsmerné hľadanie so zakázaným krokom späť (čiastočné zamedzenie duplicity):")
    start_timer = time.time()
    init2(stageOnStart, stageOnFinish)
    end_timer = time.time()
    print("Počet uzlov v 1. strome: " + str(numOfAllNodes[0][0]))
    print("Počet uzlov v 2. strome: " + str(numOfAllNodes[0][1]))
    print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
    print("Počet krokov k cieľu: " + str(len(allPaths[0])))

def testing2():
    global finished, backTrackLock
    finished = False
    backTrackLock = False
    print("\nObojsmerné hľadanie s možným krokom späť (duplicita):")
    start_timer = time.time()
    init2(stageOnStart, stageOnFinish)
    end_timer = time.time()
    print("Počet uzlov v 1. strome: " + str(numOfAllNodes[1][0]))
    print("Počet uzlov v 2. strome: " + str(numOfAllNodes[1][1]))
    print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
    print("Počet krokov k cieľu: " + str(len(allPaths[1])))

def testing3():
    global finished, backTrackLock
    finished = False
    backTrackLock = True
    print("\nHľadanie do šírky so zakázaným krokom späť (čiastočné zamedzenie duplicity):")
    start_timer = time.time()
    init1(stageOnStart)
    end_timer = time.time()
    print("Počet uzlov v strome: " + str(numOfAllNodes[2]))
    print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
    print("Počet krokov k cieľu: " + str(len(allPaths[2])))

def testing4():
    global finished, backTrackLock
    finished = False
    backTrackLock = False
    print("\nHľadanie do šírky s možným krokom späť (duplicita):")
    start_timer = time.time()
    init1(stageOnStart)
    end_timer = time.time()
    print("Počet uzlov v strome: " + str(numOfAllNodes[3]))
    print("Čas prebehnutia algoritmu: " + str(round(((end_timer - start_timer) * 1000), 2)) + "ms")
    print("Počet krokov k cieľu: " + str(len(allPaths[3])))


##--------------testovanie--------------
allPaths = [] #list pohybov všetkých algoritmov (pre štatistiku na konci)
numOfAllNodes = [[0,0],[0,0],0,0] #počítadlo všetkých uzlov v algoritmoch (pre štatistiku na konci)
sizeX = 3 #x-ovy rozmer plochy
sizeY = 3 #y-ovy rozmer plochy
##veľkosť plochy (x*y) musí mať menej ako 36 dlaždíc (kvôli nedostatku znakov)
stageOnStart = generateStartStage() #počiatočny stav
stageOnFinish = generator(10, stageOnStart) #konečny stav

print("Začiatočný stav: " + stageOnStart)
print("Konečný stav: " + stageOnFinish)

testing1() #Obojsmerné hľadanie s redukciou krokov
testing2() #Obojsmerné hľadanie bez redukcie krokov
testing3() #Prehľadavanie do šírky s redukciou krokov
testing4() #Prehľadávanie do šírky bez redukcie krokov

writeAllMoves() #Vypíše jednotlivé stavy a kroky všetkých 4 testov


