import Tkinter

AboutUs=Tkinter.Tk()
AboutUs.title("About us")

TitleLabel=Tkinter.Label(AboutUs,text="Intelligent Home Control System Sofeware",\
                         font="Times 23 bold",fg="red")
TitleLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

VersionLabel=Tkinter.Label(AboutUs,text="Version: 1.0",font="Times 20 bold",\
                           fg="blue")
VersionLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

HardwareLabel=Tkinter.Message(AboutUs,text="""Hareware Team:
Wang Ze                                     Zeng Tao
DB029068                                    DB??????
DB02906@umac.mo                 DB?????@umac.mo"""\
                        ,font="Times 15 bold",\
                           fg="#87CEFA",width=600)
HardwareLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

SoftwareLabel=Tkinter.Message(AboutUs,text="""Software Team:
Wang Ze                                                                      
DB029068                                                                
DB02906@umac.mo                                       """\
                        ,font="Times 15 bold",\
                           fg="#D2691E",width=600)
SoftwareLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

DesignLabel=Tkinter.Message(AboutUs,text="""Peripheral Design Team:
Zhou Yingsi                                 Tian Liang
DB129302                                    SB123229  
DB12930@umac.mo                 SB12322@umac.mo"""\
                        ,font="Times 15 bold",\
                           fg="#FF69B4",width=600)
DesignLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

ContentLabel=Tkinter.Message(AboutUs,text="""If you find some bugs or problems, please content us.
                                        Thank you""",font="Times 13 bold",fg="#CD5C5C",width=600)
ContentLabel.pack(side="top",padx=2,pady=1,ipadx=1,ipady=1)

AboutUs.mainloop()
