#https://github.com/bujhmt/utils for suggestions and corrections

import os
import sys
import console 
import menuTree as tree

class CUI(object):
    #support:
    __EXIT_NODE = tree.Node("EXIT", lambda: exit(1))
    __EMPTY_NODE = tree.Node("", lambda: 0)

    #private fields:
    __currentNode = __EMPTY_NODE
    __currentPos = 1

    def __init__(self, mainMenuTitle = 'Main menu'):
        self.root = tree.Node(mainMenuTitle, lambda: None)
        self.__currentNode = self.root

    def __print(self):
        console.clear()
        #custom items
        print(f'-------{self.__currentNode.title}-------')
        for i in range(len(self.__currentNode.childs)):
            if i == self.__currentPos - 1:
                console.printBold(f'[{self.__currentNode.childs[i].title}]')
            else:
                print(f'[{self.__currentNode.childs[i].title}]')

    def __inputController(self):
        if os.name == 'nt':
            return console.getch()
        else:
            return  console.readChar()

    def __stepController(self, char):
        upperLimit: int = len(self.__currentNode.childs)
        charCode: int = ord(char.lower())
        if charCode == 119 and self.__currentPos > 1: self.__currentPos += -1
        if charCode == 115 and self.__currentPos < upperLimit: self.__currentPos += 1
        if charCode == 10:  self.__currentNode.childs[self.__currentPos - 1].on_press()

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
        newNode = tree.Node(title, lambda: self.__goToCurrentNode())
        newNode.append("Return to prev Menu", lambda: self.__goToParent())
        self.__currentNode.append(newNode)
        self.__currentNode = newNode

    def finishMenu(self):
        if self.__currentNode.root != None:
            self.__goToParent()

