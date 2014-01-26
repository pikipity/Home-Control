# -*- coding: cp936 -*-
import Tkinter
import ttk
import threading
import Queue
import tkMessageBox
import serial
import time
import sys
import os
import shutil
import tkFileDialog
import win32api
####################################################################
####################################################################
######################## 一些宏量 #################################
ProgramPath=sys.argv[0][0:sys.argv[0].rfind('\\')+1]

com_switch=Queue.Queue()
com_switch_byte=0
com_switch.put(com_switch_byte)

Configure_switch=Queue.Queue()
Configure_switch.put(0)

FileSwitch=Queue.Queue()
FileSwitch.put(0)
##################################################################
######################## file read and write part #############################
# Deivce向电脑发送一个八位2进制数，前7位是设备代号,最后一位是代表该设备的开关状态. 电脑
# 在指定位置建立两个个文件,文件名是设备代号,一个记录每天的打开情况,一个记录每天的关闭情况
# 文件要包括日期及下方时间
# 注意:打开是0,关闭是1
###############################################################################
def WriteToFile(Buf):
    global DeviceNum
    global DeviceState
    DeviceInfo=ord(Buf)
    DeviceInfo=bin(DeviceInfo)
    DeviceState=DeviceInfo[len(DeviceInfo)-1]
    if(DeviceState=='0'):
        DeviceState='on'
    else:
        DeviceState='off'
    DeviceNum=DeviceInfo[0:len(DeviceInfo)-1]
    DeviceNum=str(int(DeviceNum,2))
    global DeviceChangeDay
    DeviceChangeDay=time.strftime('%Y-%m-%d  %A')
    global DeviceChangeTime
    DeviceChangeTime=time.strftime('%H:%M:%S')
    FileName='%s-%s'%(DeviceNum,DeviceState)
    PathFileName=FileStorePath+FileName+'-DATA.txt'
    if(not os.path.isfile(PathFileName)):
       fp=open(PathFileName,'w')
       Content="""%s\n  %s\n"""%(DeviceChangeDay,DeviceChangeTime)
       fp.write(Content)
       fp.close()
    else:
       fp=open(PathFileName,'r')
       AllLines=fp.readlines()
       fp.close()
       LineMark=-1
       DayStart=-10
       DayStop=len(AllLines)
       insertmark=0
       for line in AllLines:
           LineMark=LineMark+1
           if(line=="%s\n"%DeviceChangeDay):
               DayStart=LineMark
       if(DayStart==-10):
           fp=open(PathFileName,'a')
           fp.write("""%s\n  %s\n"""%(DeviceChangeDay,DeviceChangeTime))
           fp.close()
       else:
           LineMark=0
           for line in AllLines[DayStart+1:DayStop]:
               LineMark=LineMark+1
               TimeNum=int(line[2:4])*60*60+int(line[5:7])*60+int(line[8:10])
               NowTimeNum=int(time.strftime('%H'))*60*60+\
                           int(time.strftime('%M'))*60+int(time.strftime('%S'))
               if(TimeNum>=NowTimeNum):
                   insertmark=LineMark-1
                   break
               else:
                   insertmark=LineMark
           AllLines.insert(insertmark+DayStart+1,"  %s\n"%DeviceChangeTime)
           fp=open(PathFileName,'w')
           fp.seek(0)
           fp.writelines(AllLines)
           fp.close()
###############################################################################
############# COM and file location 控制模块 ###############################################
def Wrong_window(wrong_message):
    tkMessageBox.showwarning("Wrong",wrong_message)

def Open_com():
    com_switch_byte=com_switch.get()
    com_switch_byte=1
    com_switch.put(com_switch_byte)
    while(com_switch_byte==1):
        x=ser.read()
        if(len(x)!=0):
            WriteToFile(x)
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
    Configure_switch_byte=Configure_switch.get()
    Configure_switch.put(Configure_switch_byte)
    if(Configure_switch_byte==0):
        Wrong_window("Please Configure first")
    else:
        if(ser.isOpen()):
            Close_com_process=threading.Thread(target=Close_com)
            Close_com_process.start()
        else:
            Wrong_window("This COM has been closed")

def com_start():
    checkwrong=0
    global Com_number
    Configure_switch_byte=Configure_switch.get()
    Configure_switch.put(Configure_switch_byte)
    if(Configure_switch_byte==0):
        Wrong_window("Please Configure first")
    else:
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
                DataSummary_threading=threading.Thread(target=DataSummary)
                DataSummary_threading.start()
            
def ConfigureCom_Open():
    global ConfigureCom
    ConfigureCom=Tkinter.Toplevel()
    ConfigureCom.title('Configuration')
    ConfigureCom.iconbitmap("bitmap\\home.ico")
    
    label_com=Tkinter.Label(ConfigureCom,text="Com Number: ").grid(row=0,\
                                                                   column=0)
    global com_number
    com_number=Tkinter.StringVar()
    com_number.set("COM 4")
    manul_com=ttk.Combobox(ConfigureCom,text=com_number,values=["COM 1",\
                                                                "COM 2",\
                                                                "COM 3",\
                                                                "COM 4",\
                                                                "COM 5"])\
                                                                .grid(row=0,\
                                                                      column=1)
    com_number_question=Tkinter.Button(ConfigureCom,bitmap="question",height=20,command=COM_help).grid(row=0,column=2)
    
    label_boudrate=Tkinter.Label(ConfigureCom,text="Boud rate: ").grid(row=1,\
                                                                       column=0)
    global boudrate
    boudrate=Tkinter.StringVar()
    boudrate.set("9600")
    manul_boudrate=ttk.Combobox(ConfigureCom,text=boudrate,values=["4800",\
                                                                   "9600",\
                                                                   "12900"])\
                                                                   .grid(row=1\
                                                                         ,column=1)
    boudrate_question=Tkinter.Button(ConfigureCom,bitmap="question",height=20,command=boudrate_help).grid(row=1,column=2)

    global ser
    ser=serial.Serial()

    label_location=Tkinter.Label(ConfigureCom,text="Data location: ")
    label_location.grid(row=2,column=0)
    global NowLocation
    NowLocation=Tkinter.Entry(ConfigureCom,width=23)
    NowLocation.grid(row=2,column=1)
    NowLocation.insert('end',ProgramPath+'DataStore\\')
    location_question=Tkinter.Button(ConfigureCom,text="...",command=datastore_help).grid(row=2,column=2)

    ConfigureOKButton=Tkinter.Button(ConfigureCom,text="OK",\
                                     command=turn_on_configure,\
                                     width=10)
    ConfigureOKButton.grid(row=3,column=0,columnspan=2)
    #ConfigureCom.mainloop()

def turn_on_configure():
    global FileStorePath
    FileStorePath=NowLocation.get()
    if(not os.path.exists(FileStorePath[0:len(FileStorePath)-1])):
        os.makedirs(FileStorePath[0:len(FileStorePath)-1])
        fp=open(FileStorePath+"ReadMe.txt",'w')
        fp.write("""This File will teach you how to edit the Data that the program collected.

Note: Before you want to edit the Data, please read this file. After you read this file, you should not edit anything if you cannot understant this file.

1. All Data is stored in the file whose name is like this form -- "aa-nn-DATA.txt". You can edit these files.
2. You should not edit the Data that is stored in the file whose name is like this form -- "aa-nn-Control".
3. For a file whose name is like this form -- "aa-nn-DATA.txt", in this name, "aa" means the device number. "nn" means the device state.
4. In the file that you can edit, you can find the day that you control the device and the time that you control the device.
Note: One Time, One Line. At the time line, the start two characteristics must be two blank.""")
        fp.close()
    else:
        if(not os.path.isfile(FileStorePath+"ReadMe.txt")):
            fp=open(FileStorePath+"ReadMe.txt",'w')
            fp.write("""This File will teach you how to edit the Data that the program collected.

Note: Before you want to edit the Data, please read this file. After you read this file, you should not edit anything if you cannot understant this file.

1. All Data is stored in the file whose name is like this form -- "aa-nn-DATA.txt". You can edit these files.
2. You should not edit the Data that is stored in the file whose name is like this form -- "aa-nn-Control".
3. For a file whose name is like this form -- "aa-nn-DATA.txt", in this name, "aa" means the device number. "nn" means the device state.
4. In the file that you can edit, you can find the day that you control the device and the time that you control the device.
Note: One Time, One Line. At the time line, the start two characteristics must be two blank.""")
            fp.close()
    while(not Configure_switch.empty()):
        Configure_switch.get()
    Configure_switch.put(1)
###############################################################################
######################## COM and file location 设置模块结束 #########################################
###############################################################################
################# 数据总结进程###################################################
# 在数据保存位置看是否有文件,没有,sleep然后进程循环,有,进入for对文件名的循环,检测文件名是不是
# 最后以DATA.txt结尾,不是,跳出,进入循环,是,打开这个文件,读取全部时间(不是年月),写入到一个
# summary中,继续for循环,for循环结束后,进程循环
##############################################################################
def DataSummary():
    com_switch_byte=com_switch.get()
    com_switch_byte=1
    com_switch.put(com_switch_byte)
    while(com_switch_byte==1):
        AllFiles=os.listdir(FileStorePath)
        if(len(AllFiles)==0):
            time.sleep(2)
        else:
            for i in range(2):
                if(i==0):
                    AllFiles=os.listdir(FileStorePath)
                    for FileName in AllFiles:
                        if(FileName[len(FileName)-8:len(FileName)-4]=="DATA"):
                            NowFileName=FileStorePath+FileName
                            NewFileName=FileStorePath+FileName[0:len(FileName)-8]+"Summary"
                            fr=open(NowFileName,'r')
                            AllLines=fr.readlines()
                            fr.close()
                            for Line in AllLines:
                                if(Line[0]==" "):
                                    fw=open(NewFileName,'a')
                                    fw.write(Line)
                                    fw.close()
                else:
                    AllFiles=os.listdir(FileStorePath)
                    for FileName in AllFiles:
                        if(FileName[len(FileName)-7:len(FileName)]=="Summary"):
                            NowFileName=FileStorePath+FileName
                            fr=open(NowFileName,'r')
                            AllLines=fr.readlines()
                            fr.close()
                            NewAllLines=sorted(AllLines,key=lambda Line:int(Line[2:4])*60*60+int(Line[5:7])*60+int(Line[8:10]))
                            fw=open(NowFileName,'w')
                            fw.writelines(NewAllLines)
                            fw.close()
                            #将Summary中的东西进一步总结，总结为具体的某个时间，存入
                            #Control文件中。规定，某个时间上下5分钟是一样的。总结完
                            #后，删除Summary文件
                            ControlFileName=NowFileName[0:len(NowFileName)-7]+"Control"
                            ControlContent=[]
                            Group=[]
                            fr=open(NowFileName,'r')
                            CalLines=fr.readlines()
                            fr.close()
                            #一个for对于CalLines的循环，将5分钟以内的时间放入一个Group之中
                            #计算一个group的平均数，放入ControlContent中
                            for line in CalLines:
                                Group.insert(len(Group),int(line[2:4])*60*60+int(line[5:7])*60+int(line[8:10]))
                                if(len(Group)>1):
                                    if(Group[len(Group)-1]>(Group[0]+5*60)):
                                        Mean=Group[0:len(Group)-1]
                                        if(len(Mean)>=20):
                                            Mean=int(reduce((lambda x,y:x+y),Mean)/len(Mean))
                                            Mean=GetTwoWord(str(int(Mean/3600)))+":"+GetTwoWord(str(int((Mean%3600)/60)))+":"+GetTwoWord(str(int((Mean%3600)%60)))
                                            ControlContent.insert(len(ControlContent),Mean+"\n")
                                            del Group[0:len(Group)-1]
                                    else:
                                        if(line==CalLines[len(CalLines)-1]):
                                            Mean=Group[0:len(Group)]
                                            if(len(Mean)>=20):
                                                Mean=int(reduce((lambda x,y:x+y),Mean)/len(Mean))
                                                Mean=GetTwoWord(str(int(Mean/3600)))+":"+GetTwoWord(str(int((Mean%3600)/60)))+":"+GetTwoWord(str(int((Mean%3600)%60)))
                                                ControlContent.insert(len(ControlContent),Mean+"\n")
                                                del Group[0:len(Group)]
                            fw=open(ControlFileName,'w')
                            fw.writelines(ControlContent)
                            fw.close()
                            ControlContent=[]
                            os.remove(NowFileName)
        SendControl()
        com_switch_byte=com_switch.get()
        com_switch.put(com_switch_byte)
    while(not com_switch.empty()):
        com_switch.get()
    com_switch.put(0)

def GetTwoWord(Word):
    if(len(Word)==1):
        return "0"+Word
    else:
        return Word
##############################################################################
############### About Button #################################################
def AboutUs_Open():
    AboutUs=Tkinter.Toplevel()
    AboutUs.title("About us")
    AboutUs.iconbitmap("bitmap\\home.ico")

    TitleLabel=Tkinter.Label(AboutUs,text="Intelligent Home Control System Sofeware",\
                         font="Times 23 bold",fg="red")
    TitleLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

    VersionLabel=Tkinter.Label(AboutUs,text="Version: 1.0",font="Times 20 bold",\
                           fg="blue")
    VersionLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

   #BitLabel=Tkinter.Label(AboutUs,image="bitmap\\home.ico")
   #BitLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

    HardwareLabel=Tkinter.Message(AboutUs,text="""Hareware Team:
Wang Ze                                      
DB029068                                    
DB02906@umac.mo                                                 """\
                        ,font="Times 15 bold",\
                           fg="#228B22",width=600)
    HardwareLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

    SoftwareLabel=Tkinter.Message(AboutUs,text="""Software Team:
Wang Ze                                                                      
DB029068                                                                
DB02906@umac.mo                                       """\
                        ,font="Times 15 bold",\
                           fg="#D2691E",width=600)
    SoftwareLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

    DesignLabel=Tkinter.Message(AboutUs,text="""Peripheral Design Team:
Zhou Yingsi                                  Tian Liang
DB129302                                    SB123229  
DB12930@umac.mo                   SB12322@umac.mo"""\
                        ,font="Times 15 bold",\
                           fg="#FF69B4",width=600)
    DesignLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

    ContentLabel=Tkinter.Message(AboutUs,text="""If you find some bugs or problems, please content us.
                                        Thank you""",font="Times 13 bold",fg="#CD5C5C",width=600)
    ContentLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

    #AboutUs.mainloop()
##############################################################################
##################### Question Button ########################################
######### 改为从文档直接读取 ###################################################
def GetContent(path):
    fr=open(path,'r')
    lines=fr.readlines()
    fr.close()
    GetContent=""
    for line in lines:
        GetContent=GetContent+line
    return GetContent

def Main_Question():
    MainHelp=GetContent("help\\main_help.txt")
    Main_help=Tkinter.Toplevel()
    Main_help.title("Main Help")
    Main_help.iconbitmap("bitmap\\home.ico")
    Main_help_content=Tkinter.Message(Main_help,text=MainHelp\
                                      ,font="12",width=400).pack()
    Main_help.mainloop()

def COM_help():
    ComHelp=GetContent("help\\COM_help.txt")
    COMHelp=Tkinter.Toplevel()
    COMHelp.title("COM port configure help")
    COMHelp.iconbitmap("bitmap\\home.ico")
    COMHelp_content=Tkinter.Message(COMHelp,text=ComHelp\
                                    ,font="12",width=400).pack()
    COMHelp.mainloop()

def boudrate_help():
    Boudrate_Help=GetContent("help\\boudrate_help.txt")
    BoudrateHelp=Tkinter.Toplevel()
    BoudrateHelp.title("Boudrate configure help")
    BoudrateHelp.iconbitmap("bitmap\\home.ico")
    BoudrateHelp_content=Tkinter.Message(BoudrateHelp,text=Boudrate_Help\
                                         ,font="12",width=400).pack()
    BoudrateHelp.mainloop()

def datastore_help():
    datastorePATH=tkFileDialog.askdirectory(initial=NowLocation.get(),title="Choose Data Store Path",parent=ConfigureCom)
##############################################################################
############### Auto Control Windows #########################################
def AutoControlWindow_Open():
    AutoControlWindow=Tkinter.Tk()
    AutoControlWindow.title("Automatic Control Configuration")
    AutoControlWindow.iconbitmap("bitmap\\home.ico")

    AutoControlWindowContent=Tkinter.Label(AutoControlWindow,text="Please fill the device number, turn on time and turn off time that you want. Then click \"Add\"")
    AutoControlWindowContent.pack(side="top")
    
    DeviceNumberFrame=Tkinter.Frame(AutoControlWindow)
    DeviceNumberFrame.pack()
    AutoDeviceNumberLabel=Tkinter.Label(DeviceNumberFrame,text="Device Number: ")
    AutoDeviceNumberLabel.pack(side="left")
    global AutoDeviceNumberEntry
    AutoDeviceNumberEntry=Tkinter.Entry(DeviceNumberFrame)
    AutoDeviceNumberEntry.pack(side="left")

    TurnOnFrame=Tkinter.Frame(AutoControlWindow)
    TurnOnFrame.pack()
    AutoTurnOnLabel=Tkinter.Message(TurnOnFrame,\
                                    text="      Turn on time\n(like 2011-01-01,13:23:34)",width=180).pack(\
        side="left")
    global AutoTurnOnEntry
    AutoTurnOnEntry=Tkinter.Entry(TurnOnFrame)
    AutoTurnOnEntry.pack(side="left")
    
    TurnOffFrame=Tkinter.Frame(AutoControlWindow)
    TurnOffFrame.pack()
    AutoTurnOffLabel=Tkinter.Message(TurnOffFrame,text="      Turn off time\n(like 2011-01-01,13:23:35)",width=180).pack(side="left")
    global AutoTurnOffEntry
    AutoTurnOffEntry=Tkinter.Entry(TurnOffFrame)
    AutoTurnOffEntry.pack(side="left")

    AddButton=Tkinter.Button(AutoControlWindow,text="Add",width=40,height=2,command=AddAutoControl)
    AddButton.pack()
    
    AutoControlWindow.mainloop()

def AddAutoControl():
    Configure_switch_byte=Configure_switch.get()
    Configure_switch.put(Configure_switch_byte)
    if(Configure_switch_byte==0):
        Wrong_window("Please Configure first")
    else:
        DeviceNumberAuto=AutoDeviceNumberEntry.get()
        TurnOnAuto=AutoTurnOnEntry.get()
        TurnOffAuto=AutoTurnOffEntry.get()
        if(len(DeviceNumberAuto)==0):
            tkMessageBox.showwarning("Wrong","Please fill a Device Number")
        elif(len(TurnOnAuto)==0 and len(TurnOffAuto)==0):
            tkMessageBox.showwarning("Wrong","Please fill turn on time or turn off time")
        else:
            if(not len(TurnOnAuto)==0):
                AutoFileName=FileStorePath+DeviceNumberAuto+"-on-AutoControl"
                Error=0
                try:
                    TurnOnAuto[2]
                except IndexError:
                    Error=1
                try:
                    TurnOnAuto[4]
                except IndexError:
                    Error=1
                if(Error==1):
                    tkMessageBox.showwarning("Wrong","The format of turn on time is wrong.")
                elif((not TurnOnAuto[2]==":") and (not TurnOnAuto[4]=="-")):
                    tkMessageBox.showwarning("Wrong","The format of turn on time is wrong.")
                elif(TurnOnAuto[2]==":"):
                    TurnOnAutoTime="  "+TurnOnAuto
                    if(not os.path.isfile(AutoFileName)):
                        fw=open(AutoFileName,'w')
                        fw.write(TurnOnAutoTime+"\n")
                        fw.close()
                    else:
                        fr=open(AutoFileName,'r')
                        lines=fr.readlines()
                        fr.close()
                        dontadd=0
                        for line in lines:
                            if(line==TurnOnAutoTime+"\n"):
                                dontadd=1
                        if(dontadd==0):
                            fw=open(AutoFileName,'a')
                            fw.write(TurnOnAutoTime+"\n")
                            fw.close()
                elif(TurnOnAuto[4]=="-"):
                    TurnOnAutoTime=TurnOnAuto[(TurnOnAuto.rfind(',')+1):len(TurnOnAuto)]
                    TurnOnAutoDay=TurnOnAuto[0:TurnOnAuto.rfind(',')]
                    if(not os.path.isfile(AutoFileName)):
                        fw=open(AutoFileName,'w')
                        fw.write(TurnOnAutoDay+","+TurnOnAutoTime+"\n")
                        fw.close()
                    else:
                        fr=open(AutoFileName,'r')
                        lines=fr.readlines()
                        fr.close()
                        dontadd=0
                        for line in lines:
                            if(line==TurnOnAutoDay+","+TurnOnAutoTime+"\n"):
                                dontadd=1
                        if(dontadd==0):
                            fw=open(AutoFileName,'a')
                            fw.write(TurnOnAutoDay+","+TurnOnAutoTime+"\n")
                            fw.close()
            if(not len(TurnOffAuto)==0):
                AutoFileName=FileStorePath+DeviceNumberAuto+"-off-AutoControl"
                Error=0
                try:
                    TurnOffAuto[2]
                except IndexError:
                    Error=1
                try:
                    TurnOffAuto[4]
                except IndexError:
                    Error=1
                if(Error==1):
                    tkMessageBox.showwarning("Wrong","The format of turn off time is wrong.")
                elif((not TurnOffAuto[2]==":") and (not TurnOffAuto[4]=="-")):
                    tkMessageBox.showwarning("Wrong","The format of turn off time is wrong.")
                elif(TurnOffAuto[2]==":"):
                    TurnOffAutoTime="  "+TurnOffAuto
                    if(not os.path.isfile(AutoFileName)):
                        fw=open(AutoFileName,'w')
                        fw.write(TurnOffAutoTime+"\n")
                        fw.close()
                    else:
                        fr=open(AutoFileName,'r')
                        lines=fr.readlines()
                        fr.close()
                        dontadd=0
                        for line in lines:
                            if(line==TurnOffAutoTime+"\n"):
                                dontadd=1
                        if(dontadd==0):
                            fw=open(AutoFileName,'a')
                            fw.write(TurnOffAutoTime+"\n")
                            fw.close()
                elif(TurnOffAuto[4]=="-"):
                    TurnOffAutoTime=TurnOffAuto[(TurnOffAuto.rfind(',')+1):len(TurnOffAuto)]
                    TurnOffAutoDay=TurnOffAuto[0:TurnOffAuto.rfind(',')]
                    if(not os.path.isfile(AutoFileName)):
                        fw=open(AutoFileName,'w')
                        fw.write(TurnOffAutoDay+","+TurnOffAutoTime+"\n")
                        fw.close()
                    else:
                        fr=open(AutoFileName,'r')
                        lines=fr.readlines()
                        fr.close()
                        dontadd=0
                        for line in lines:
                            if(line==TurnOffAutoDay+","+TurnOffAutoTime+"\n"):
                                dontadd=1
                        if(dontadd==0):
                            fw=open(AutoFileName,'a')
                            fw.write(TurnOffAutoDay+","+TurnOffAutoTime+"\n")
                            fw.close()    
##############################################################################
################ Edit Data Button ############################################
def EditDataFun():
    global ReadMe
    ReadMe=Tkinter.Toplevel()
    ReadMeContent=Tkinter.Message(ReadMe,text="""Read me First.

This File will teach you how to edit the Data that the program collected.

Note: Before you want to edit the Data, please read this file. After you read this file, you should not edit anything if you cannot understant this file.

1. All Data is stored in the file whose name is like this form -- "aa-nn-DATA.txt". You can edit these files.
2. You should not edit the Data that is stored in the file whose name is like this form -- "aa-nn-Control".
3. For a file whose name is like this form -- "aa-nn-DATA.txt", in this name, "aa" means the device number. "nn" means the device state.
4. In the file that you can edit, you can find the day that you control the device and the time that you control the device.
Note: One Time, One Line. At the time line, the start two characteristics must be two blank.""")
    ReadMeContent.pack()
        
    FileNameFrame=Tkinter.Frame(ReadMe)
    FileNameFrame.pack()

    FileNameEntryLabel=Tkinter.Label(FileNameFrame,text="Choose File:")
    FileNameEntryLabel.pack(side="left")

    global FileNameEntry
    FileNameEntry=Tkinter.Entry(FileNameFrame)
    FileNameEntry.pack(side="left")

    ChooseFileButton=Tkinter.Button(FileNameFrame,text="...",command=ChooseFileButtonfun)
    ChooseFileButton.pack(side="left")

    OKChooseButton=Tkinter.Button(ReadMe,text="OK",width=40,height=2,command=OKButtonFunction)
    OKChooseButton.pack(side="top")

def ChooseFileButtonfun():
    Configure_switch_byte=Configure_switch.get()
    Configure_switch.put(Configure_switch_byte)
    if(Configure_switch_byte==0):
        Wrong_window("Please Configure first")
    else:
        FileNameEntry.delete(0,"end")
        ChooseFileEdit=tkFileDialog.askopenfilename(initialdir=FileStorePath,\
                                                    parent=ReadMe,\
                                                    title="Choose File")
        FileNameEntry.insert("end",ChooseFileEdit)
def OKButtonFunction():
    Configure_switch_byte=Configure_switch.get()
    Configure_switch.put(Configure_switch_byte)
    if(Configure_switch_byte==0):
        Wrong_window("Please Configure first")
    else:
        ChooseFileEdit=FileNameEntry.get()
        win32api.ShellExecute(0,'open','notepad.exe',ChooseFileEdit,'',1)
##############################################################################
############# 发送进程 ########################################################
# 检查目录下面的文件,对两种文件进行读取,一个是末尾是Control的文件,对该文件读取,并一
# 一核对,找到时间一样的就进行发送.一个是末尾是AutoControl的文件,对文件读取,并一一核对,
# 但是注意,分两种,只有时间的行,和有时间也有年份的行
def SendControl():
    AllFiles=os.listdir(FileStorePath)
    if(len(AllFiles)==0):
        time.sleep(2)
    else:
        NowYear=time.strftime('%Y-%m-%d')
        NowTime=time.strftime('%H:%M:%S')
        for FileNameCheck in AllFiles:
            if(FileNameCheck[len(FileNameCheck)-11:len(FileNameCheck)]=="AutoControl"):
                fr=open(FileStorePath+FileNameCheck,'r')
                ContentCheck=fr.readlines()
                fr.close()
                for line in ContentCheck:
                    if(line[4]==":"):
                        if((int(line[2:4])*3600+int(line[5:7])*60+int(line[8:10])+30>=int(NowTime[0:2])*3600+int(NowTime[3:5])*60+int(NowTime[6:8]) and int(line[2:4])*3600+int(line[5:7])*60+int(line[8:10])-30<=int(NowTime[0:2])*3600+int(NowTime[3:5])*60+int(NowTime[6:8]))):
                            SendingDeviceNum=FileNameCheck[0:FileNameCheck.rfind('-')]
                            SendingDeviceNum=SendingDeviceNum[0:SendingDeviceNum.rfind('-')]
                            SendingDeviceState=FileNameCheck[\
                                (FileNameCheck[0:FileNameCheck.rfind('-')]\
                                 .rfind('-')+1):FileNameCheck.rfind('-')]
                            if(SendingDeviceState=="off"):
                                SendingDeviceState='1'
                            elif(SendingDeviceState=="on"):
                                SendingDeviceState='0'
                            SendingDeviceNum=bin(int(SendingDeviceNum))
                            SendingDeviceInfo=SendingDeviceNum+SendingDeviceState
                            #已经整理为二进制码,现在要将二进制码通过ser发送出去
                            SendingDeviceInfo=SendingDeviceInfo[SendingDeviceInfo.rfind('b')+1:len(SendingDeivceInfo)]
                            SendingDeviceInfo=SendingDeviceInfo[::-1]
                            SendingDeviceInfo+="00000000"[0:8-len(SendingDeivceInfo)]
                            SendingDeviceInfo=SendingDeviceInfo[::-1]
                            SendingDeviceInfo=hex(int(SendingDeviceInfo,2))
                            ser.write(SendingDeviceInfo)
                    elif(line[4]=="-"):
                        if(NowYear==line[0:line.rfind(',')]):
                            if((int(line[11:13])*3600+int(line[14:16])*60+int(line[17:19])+30>=int(NowTime[0:2])*3600+int(NowTime[3:5])*60+int(NowTime[6:8]) and int(line[11:13])*3600+int(line[14:16])*60+int(line[17:19])-30<=int(NowTime[0:2])*3600+int(NowTime[3:5])*60+int(NowTime[6:8]))):
                                SendingDeviceNum=FileNameCheck[0:FileNameCheck.rfind('-')]
                                SendingDeviceNum=SendingDeviceNum[0:SendingDeviceNum.rfind('-')]
                                SendingDeviceState=FileNameCheck[\
                                    (FileNameCheck[0:FileNameCheck.rfind('-')]\
                                     .rfind('-')+1):FileNameCheck.rfind('-')]
                                if(SendingDeviceState=="off"):
                                    SendingDeviceState='1'
                                elif(SendingDeviceState=="on"):
                                    SendingDeviceState='0'
                                SendingDeviceNum=bin(int(SendingDeviceNum))
                                SendingDeviceInfo=SendingDeviceNum+SendingDeviceState
                                #已经整理为二进制码,现在要将二进制码通过ser发送出去
                                SendingDeviceInfo=SendingDeviceInfo[SendingDeviceInfo.rfind('b')+1:len(SendingDeivceInfo)]
                                SendingDeviceInfo=SendingDeviceInfo[::-1]
                                SendingDeviceInfo+="00000000"[0:8-len(SendingDeivceInfo)]
                                SendingDeviceInfo=SendingDeviceInfo[::-1]
                                SendingDeviceInfo=hex(int(SendingDeviceInfo,2))
                                ser.write(SendingDeviceInfo)
            elif(FileNameCheck[FileNameCheck.rfind('-')+1:len(FileNameCheck)]=="Control"):
                fr=open(FileStorePath+FileNameCheck,'r')
                ContentCheck=fr.readlines()
                fr.close()
                for line in ContentCheck:
                    if((int(line[0:2])*3600+int(line[3:5])*60+int(line[6:8])+30>=int(NowTime[0:2])*3600+int(NowTime[3:5])*60+int(NowTime[6:8]) and int(line[0:2])*3600+int(line[3:5])*60+int(line[6:8])-30<=int(NowTime[0:2])*3600+int(NowTime[3:5])*60+int(NowTime[6:8]))):
                        SendingDeviceNum=FileNameCheck[0:FileNameCheck.rfind('-')]
                        SendingDeviceNum=SendingDeviceNum[0:SendingDeviceNum.rfind('-')]
                        SendingDeviceState=FileNameCheck[\
                                (FileNameCheck[0:FileNameCheck.rfind('-')]\
                                 .rfind('-')+1):FileNameCheck.rfind('-')]
                        if(SendingDeviceState=="off"):
                            SendingDeviceState='1'
                        elif(SendingDeviceState=="on"):
                            SendingDeviceState='0'
                        SendingDeviceNum=bin(int(SendingDeviceNum))
                        SendingDeviceInfo=SendingDeviceNum+SendingDeviceState
                        #已经整理为二进制码,现在要将二进制码通过ser发送出去
                        SendingDeviceInfo=SendingDeviceInfo[SendingDeviceInfo.rfind('b')+1:len(SendingDeivceInfo)]
                        SendingDeviceInfo=SendingDeviceInfo[::-1]
                        SendingDeviceInfo+="00000000"[0:8-len(SendingDeivceInfo)]
                        SendingDeviceInfo=SendingDeviceInfo[::-1]
                        SendingDeviceInfo=hex(int(SendingDeviceInfo,2))
                        ser.write(SendingDeviceInfo)
##############################################################################


root=Tkinter.Tk()
root.title('Intelligent Home Control System')
root.iconbitmap("bitmap\\home.ico")

MainFrame=Tkinter.Frame(root,borderwidth=2,width=200,height=300)
MainFrame.pack(fill='y',expand=1,padx=15,pady=5,ipadx=5,ipady=9)

ConfigureButton=Tkinter.Button(MainFrame,borderwidth=1,\
                               text="Configuration",\
                               font="Times 23 bold",\
                               command=ConfigureCom_Open)
ConfigureButton.pack(fill='both',expand=1,padx=2,pady=1,ipadx=2,ipady=1)

HabitButton=Tkinter.Button(MainFrame,borderwidth=1,text="Little Housekeeper",\
                           font="Times 23 bold")#,state="disabled")
HabitButton.pack(fill='both',expand=1,padx=2,pady=1,ipadx=2,ipady=1)

ConfigureAutoButton=Tkinter.Button(MainFrame,borderwidth=1,\
                                   text="Configure Automatic Switch",\
                                   font="Times 23 bold",command=AutoControlWindow_Open)
ConfigureAutoButton.pack(fill='both',expand=1,padx=2,pady=1,ipadx=2,ipady=1)

ShowDataButton=Tkinter.Button(MainFrame,borderwidth=1,text="Edit data",\
                              font="Times 23 bold",command=EditDataFun)
ShowDataButton.pack(fill='both',expand=1,padx=2,pady=1,ipadx=2,ipady=1)

AboutButton=Tkinter.Button(MainFrame,borderwidth=1,text="About"\
                           ,font="Times 23 bold",command=AboutUs_Open)
AboutButton.pack(fill='both',expand=1,padx=2,pady=1,ipadx=2,ipady=1)

SwitchFrame=Tkinter.Frame(root)
SwitchFrame.pack()

button_on=Tkinter.Button(SwitchFrame,text="Start Control",\
                         font="Times 15 bold",\
                         command=com_start).pack(side='left',padx=2,\
                                                 pady=1,ipadx=1,\
                                                 ipady=1)
button_off=Tkinter.Button(SwitchFrame,text="Stop Control",\
                          font="Times 15 bold",\
                          command=com_stop).pack(side='left',padx=2,\
                                                 pady=1,ipadx=1,\
                                                 ipady=1)
button_help=Tkinter.Button(SwitchFrame,bitmap="question",command=Main_Question).pack(side='left',\
                                                               padx=2,\
                                                               pady=1,ipadx=1,\
                                                               ipady=1)
root.mainloop()
