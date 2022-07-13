from cProfile import run
from concurrent.futures import process
from tkinter import BUTT
from communication import connect 
from multiprocessing import Process

BUTTON_PRESSED = False

def getInput(BUTTON_PRESSED):
    while True:
        x = input("Enter")
        if x:
            BUTTON_PRESSED = not BUTTON_PRESSED

def runCode(BUTTON_PRESSED):
    while True:
        if BUTTON_PRESSED:
            print("True")
        else:
            pass
            # print("False")
    

if __name__ == "__main__":
    # mqtt = connect()
    # mqtt.loop_start()


    p = Process(target=runCode, args=(BUTTON_PRESSED, ))
    # getInput(BUTTON_PRESSED)
    q = Process(target=getInput, args=(BUTTON_PRESSED, ))
    p.start()
    p.join()
    q.start()
    q.join()
