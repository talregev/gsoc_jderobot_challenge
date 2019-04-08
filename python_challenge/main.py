import gol
import numpy as np


def test1():
    b = gol.Board()
    b.read("tests/02.txt")
    b.steps(10)
    if(np.array_equal(b.board, np.array([[0, 0, 1, 0, 0],
                                         [0, 0, 1, 0, 0],
                                         [0, 0, 1, 0, 0]]
                                       ))):
        print("Test1 Pass")
    else:
        print("Test1 Fail")


def test2():
    b = gol.Board()
    b.read("tests/02.txt")
    b.steps(11)
    if(np.array_equal(b.board, np.array([[0, 0, 0, 0, 0],
                                         [0, 1, 1, 1, 0],
                                         [0, 0, 0, 0, 0]]
                                       ))):
        print("Test2 Pass")
    else:
        print("Test2 Fail")


def test3():
    b = gol.Board()
    b.load("console.json")
    b.steps(10)
    if(np.array_equal(b.board, np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                                         [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                                         [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                                       ))):
        print("Test3 Pass")
    else:
        print("Test3 Fail")


def test4():
    b = gol.Board()
    b.load("console.json")
    b.steps(11)
    if(np.array_equal(b.board, np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                                       ))):
        print("Test4 Pass")
    else:
        print("Test4 Fail")


test1()
test2()
test3()
test4()
b = gol.Board()
b.is_print = True
b.read("tests/02.txt")
b.step()
b.load("gui.json")
