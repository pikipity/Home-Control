import Tkinter
import ttk
import serial
import threading
import Queue
import tkMessageBox

condition=threading.RLock()
com_switch=Queue.Queue()
com_switch_byte=0
com_switch.put(com_switch_byte)


def Wrong_window(wrong_message):
    tkMessageBox.showwarning("Wrong",wrong_message)

def Open_com():
    com_switch_byte=com_switch.get()
    com_switch_byte=1
    com_switch.put(com_switch_byte)
    while(com_switch_byte==1):
        x=ser.read()
        if(len(x)!=0):
            x=ord(x)
            text_display.insert('1.end','%02X'%x+' ')
        com_switch_byte=com_switch.get()
        com_switch.put(com_switch_byte)
    ser.close()
    while(not com_switch.empty()):
        com_switch.get()
    com_switch.put(0)

def Close_com():
    com_switch_byte=com_switch.get()
    com_switch_byte=0
    com_switch.put(com_switch_byte)

def com_stop():
    if(ser.isOpen()):
        Close_com_process=threading.Thread(target=Close_com)
        Close_com_process.start()
    else:
        Wrong_window("This COM has been closed")

def com_start():
    checkwrong=0
    global Com_number
    Com_number=com_number.get()
    if(ser.isOpen()):
        Wrong_window("This COM has been opened")
    else:
        Com_number=int(Com_number[4])-1
        boudrate_num=boudrate.get()
        boudrate_num=int(boudrate_num)
        ser.baudrate=boudrate_num
        ser.port=Com_number
        ser.timeout=1
        try:
            ser.open()
        except serial.SerialException:
            Wrong_window("There is something wrong for your %s"%com_number.get())
            checkwrong=1
        if(checkwrong==0):
            Open_com_process=threading.Thread(target=Open_com)
            Open_com_process.start()
            


if(__name__=="__main__"):
    root=Tkinter.Tk()
    
    text_display=Tkinter.Text(root,width=80,height=24,border=5)
    text_display.grid(row=0,column=2,columnspan=200,rowspan=200)
    
    label_com=Tkinter.Label(root,text="Com Number: ").grid(row=0,column=0)
    com_number=Tkinter.StringVar()
    com_number.set("COM 4")
    manul_com=ttk.Combobox(root,text=com_number,values=["COM 1","COM 2","COM 3","COM 4","COM 5"]).grid(row=0,column=1)
    
    label_boudrate=Tkinter.Label(root,text="Boud rate: ").grid(row=1,column=0)
    boudrate=Tkinter.StringVar()
    boudrate.set("9600")
    manul_boudrate=ttk.Combobox(root,text=boudrate,values=["4800","9600","12900"]).grid(row=1,column=1)
    
    ser=serial.Serial()
    button_on=Tkinter.Button(root,text="Open Com",command=com_start).grid(row=2,column=0)
    button_off=Tkinter.Button(root,text="Close Com",command=com_stop).grid(row=2,column=1)
    
    root.mainloop()

