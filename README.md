家庭自动控制系统
======================

用 Arduino 和 8051 单片机构建一个简单的家庭控制系统。主要实现以下两点功能：
1、实现单片机将控制信息传输到PC，由PC根据收集的数据运算得到进行操作的时间，实现自动根据用户习惯进行控制
2、用户通过PC输入希望执行操作的时间，PC到时自动向单片机发送信息，实现操作

--------------------------------------------------------------------------------------------------------

项目主要包括三个部分：

1. 硬件设计：
   包括红外遥控器控制部分和以电脑为中心的两种控制方式。红外遥控器控制以 8051 单片机为核心进行编码和解码以及控制的实现。以电脑为中心的控制以 Arduino UNO 为核心，使用 NRF24L01+ 模块进行无线传输控制。

   下面是以电脑为中心的发射和接受装置的电路图
   
   ![从机的接受装置](https://lh3.googleusercontent.com/-SA0oif-C_R0/UueIUWH-9jI/AAAAAAAABdM/Ae4aOc2kgAE/s576/client_bb.png)
   ![主机的发射装置](https://lh3.googleusercontent.com/-rtq3Msab1jI/UueIUbXiXQI/AAAAAAAABdI/fQ3Yztsff-I/s576/server_board.png)
2. 软件设计：
   使用Python脚本语言，使用Tkinter模块制作图形化界面，方便用户操作。将 [Little Mr.](https://github.com/pikipity/Little_Mr.git) 加入了进来，作为一个附属程序，另名为 "Little Housekeeper"，你可以通过它直接进行控制。

--------------------------------------------------------------------------------------------------------

现已包括：

1. Home Control Software 文件夹：主要包括现已基本完成的软件部分，需要硬件搭配使用，包括 Python 编写的 GUI 和改进之后的 "Little Housekeeper"。
2. Red\_communication\_test 文件夹：STC89C52RC编程部分。
3. arduino_control 文件夹：Arduino UNO 的编程部分及电路图。
4. datasheet 文件夹：可能会用到的 datasheet

--------------------------------------------------------------------------------------------------------

演示视频：

1. [GUI 使用演示](http://v.youku.com/v_show/id_XNjY2NzcwMzcy.html)
2. [Little Housekeeper 使用演示](http://v.youku.com/v_show/id_XNjY2NzcwNzIw.html)
3. [Arduino 演示](http://v.youku.com/v_show/id_XNjY2NzcxMjY0.html)
