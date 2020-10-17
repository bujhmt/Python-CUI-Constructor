#https://github.com/bujhmt/utils for suggestions and corrections

import os
import sys

#console utils:
def printBold(str):
    BOLD = '\33[7m'
    CEND = '\033[0m'
    print(BOLD + str + CEND)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def readChar():
    import tty
    import termios
    tty.setcbreak(sys.stdin)
    x = sys.stdin.read(1)[0]
    return x

def getch():
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch()
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


#Tree Node 
class Node(object):

    def __init__(self, title, on_press):
        self.title = title
        self.on_press = on_press
        self.childs = []
        self.root = None


    def append(self, *args):
        try:
            if len(args) == 1 and isinstance(args[0], Node):
                args[0].root = self
                self.childs.append(args[0])
            if len(args) == 2 and isinstance(args[0], str):
                newNode = Node(args[0], args[1])
                newNode.root = self
                self.childs.append(newNode)
        except Exception as err:
            print("Error! ", err)

#CUI class
class CUI(object):
    #support:
    __EXIT_NODE = Node("EXIT", lambda: exit(1))
    __EMPTY_NODE = Node("", lambda: 0)

    #private fields:
    __currentNode = __EMPTY_NODE
    __currentPos = 1

    def __init__(self, mainMenuTitle = 'Main menu'):
        self.root = Node(mainMenuTitle, lambda: None)
        self.__currentNode = self.root

    def __print(self):
        clear()
        #custom items
        print(f'-------{self.__currentNode.title}-------')
        for i in range(len(self.__currentNode.childs)):
            if i == self.__currentPos - 1:
                printBold(f'[{self.__currentNode.childs[i].title}]')
            else:
                print(f'[{self.__currentNode.childs[i].title}]')

    def __inputController(self):
        if os.name == 'nt':
            return getch()
        else:
            return  readChar()

    def __stepController(self, char):
        upperLimit: int = len(self.__currentNode.childs)
        charCode: int = ord(char.lower())
        if charCode == 119 and self.__currentPos > 1: self.__currentPos -= 1
        if charCode == 115 and self.__currentPos < upperLimit: self.__currentPos += 1
        if charCode == 10 or charCode == 13:  self.__currentNode.childs[self.__currentPos - 1].on_press()

    def __goToCurrentNode(self):
        self.__currentNode = self.__currentNode.childs[self.__currentPos - 1]
        self.__currentPos = 1

    def __goToParent(self):
        self.__currentNode = self.__currentNode.root
        self.__currentPos = 1

    #public fields:
    def run(self, *args):
        if len(args) == 0 or args[0] == True:
            self.root.append(self.__EXIT_NODE)
            self.__currentNode = self.root
        while True:
            self.__print()
            self.__stepController(self.__inputController())

    def addField(self, title, *args):
        if len(args) > 0:
            self.__currentNode.append(title, args[0])
        else:
            self.__currentNode.append(title, lambda: 0)

    def addMenu(self, title):
        newNode = Node(title, lambda: self.__goToCurrentNode())
        newNode.append("Return to prev Menu", lambda: self.__goToParent())
        self.__currentNode.append(newNode)
        self.__currentNode = newNode

    def finishMenu(self):
        if self.__currentNode.root != None:
            self.__goToParent()
