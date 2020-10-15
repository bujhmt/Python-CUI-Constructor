#https://github.com/bujhmt/utils for suggestions and corrections

import os
import tty
import sys
import termios

def printBold(str):
    BOLD = '\33[7m'
    CEND = '\033[0m'
    print(BOLD + str + CEND)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def readChar():
    tty.setcbreak(sys.stdin)
    x = sys.stdin.read(1)[0]
    return x

def getch():
    if (os.name == 'nt'):
        import msvcrt
        return msvcrt.getch()
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch