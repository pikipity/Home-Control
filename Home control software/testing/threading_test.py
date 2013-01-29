import threading
import time
import Tkinter

def Testing_1():
    print "A"
    print "B"
    print "C"
def Testing_2():
    print 1
    print 2
    print 3


Testing_1_threading=threading.Thread(target=Testing_1)
Testing_1_threading.start()
Testing_2_threading=threading.Thread(target=Testing_2)
Testing_2_threading.start()

