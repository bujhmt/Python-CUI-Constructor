import os
import sys


# console utils:
def printBold(str):
    BOLD = '\33[7m'
    CEND = '\033[0m'
    print(BOLD + str + CEND)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


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


# Tree Node
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


# CUI class
class CUI(object):
    def __setBreakStatus(self, status: bool):
        self.__isBreakON = status

    def __init__(self, mainMenuTitle='Main menu'):
        self.root = Node(mainMenuTitle, lambda: 0)
        self.__currentNode = self.root

        # support:
        self.__BREAK_NODE = Node("EXIT", lambda: self.__setBreakStatus(False))
        self.__EMPTY_NODE = Node("", lambda: 0)

        # private fields:
        self.__currentPos = 1
        self.__isBreakON = True
        self.__msg = ''

    def __print(self):
        clear()
        # custom items
        print(f'-------{self.__currentNode.title}-------' + self.__msg)
        for i in range(len(self.__currentNode.childs)):
            if i == self.__currentPos - 1:
                printBold(f'[{self.__currentNode.childs[i].title}]')
            else:
                print(f'[{self.__currentNode.childs[i].title}]')

    def __inputController(self):
        return getch()

    def __stepController(self, char):
        upperLimit: int = len(self.__currentNode.childs)
        charCode: int = ord(char.lower())
        if (charCode == 119 or charCode == 97) and self.__currentPos > 1: self.__currentPos += -1
        if (charCode == 115 or charCode == 98) and self.__currentPos < upperLimit: self.__currentPos += 1
        try:
            if charCode == 10 or charCode == 13:  self.__currentNode.childs[self.__currentPos - 1].on_press()
        except Exception as err:
            self.setMsg(' Invalid operation! ' + str(err)[0:70])

    def __goToCurrentNode(self):
        self.__currentNode = self.__currentNode.childs[self.__currentPos - 1]
        self.__currentPos = 1

    def __goToParent(self):
        self.__currentNode = self.__currentNode.root
        self.__currentPos = 1

    # public fields:
    def run(self, *args):
        self.__currentNode = self.root
        exit_str = "EXIT"
        if len(args) > 0 and isinstance(args[0], str): exit_str = args[0]
        if not (len(args) > 0 and isinstance(args[0], bool) and args[0] is False):
            self.__currentNode.append(exit_str, lambda: self.__setBreakStatus(False))


        while (self.__isBreakON):
            self.__print()
            self.__stepController(self.__inputController())
        clear()

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

    def renameField(self, current: str, new: str):
        try:
            if len(current) > 0 and len(new) > 0:
                if self.__currentNode.title == current:
                    self.__currentNode.title = new

                for i in range(len(self.__currentNode.childs)):
                    if self.__currentNode.childs[i].title == current:
                        self.__currentNode.childs[i].title = new
            else:
                raise Exception('Invalid title')
        except Exception as err:
            print("Error! ", err)

    def deleteField(self, title: str):
        try:
            if len(title) > 0:
                for i in range(len(self.__currentNode.childs)):
                    if self.__currentNode.childs[i].title == title:
                        del self.__currentNode.childs[i]
            else:
                raise Exception('Invalid title')
        except Exception as err:
            print("Error! ", err)

    def setMsg(self, msg: str):
        if len(msg) > 105:
            msg = msg[0:msg.find('\n')]
        self.__msg = msg

    def stop(self):
        self.__setBreakStatus(False)