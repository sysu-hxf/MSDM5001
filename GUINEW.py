# -*- coding: utf-8 -*-
"""
Created on Tue May 17 07:49:59 2022

@author: DELL
"""

#from mpl_toolkits.basemap import Basemap
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget,QMainWindow,QLineEdit,QLabel,QPushButton,QHBoxLayout,QVBoxLayout,QFileDialog  
from one import *
import matplotlib.pyplot as plt
#import numpy as np
from PyQt5 import QtWidgets ,QtGui
from PLOT import plot
#from PyQt5.QtCore import QObject , pyqtSignal 
from qt_material import apply_stylesheet
from PyQt5.QtGui import QIcon,QPalette, QBrush, QPixmap

class App(QWidget):
    #signal_1 = pyqtSignal(str) 
    def __init__(self):
        super().__init__()
        
        #self.title = '可视化软件'
        self.left = 200
        self.top = 200
        self.width = 900
        self.height = 700
        #self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.myButton = QtWidgets.QPushButton(self)
        self.myButton.setObjectName("myButton")
        self.myButton.setText("Choose HDF")
        self.myButton.move(120,630)
        self.myButton.clicked.connect(self.msg)
        self.textbox = QLineEdit(self)
        self.textbox.setObjectName("text")
        self.textbox.setText('file')
        self.textbox.move(120, 680)
        self.textbox.resize(900, 60)
        self.textbox.textChanged.connect(self.pr)
        
        
        self.label = QLabel(self)
        self.label.setText(" 当此处显示出数据路径时，可点击加载图像进行预览")
        self.label.setFixedSize(600, 400)
        self.label.move(120, 120)

        self.label.setStyleSheet("QLabel{background-color:rgb(200,200,200);}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;}"
                                 )

        btn = QPushButton(self)
        btn.setText("加载图像")
        btn.move(330, 630)
        btn.setStyleSheet("background-color:pink;color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;")
        btn.clicked.connect(self.openimage)
        
        #self.form2 = plot() 
        #self.signal_1.connect(self.form2.drawit)
        #self.pushbutton = QtWidgets.QPushButton(self)
        #self.pushbutton.setObjectName("pushbutton")
        #self.pushbutton.setText("向绘制界面传递数据")
        #self.pushbutton.move(20,550)
        #self.pushbutton.clicked.connect(self.open_form2)
        

    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", self.label.text(), "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)

    def msg(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,"选取文件","./", "All Files (*);;Excel Files (*.xls)")  #设置文件扩展名过滤,注意用双分号间隔
        print(fileName1,filetype)
        self.textbox.setText(fileName1) 
    def pr(self):
        a = self.textbox.text()
        print(a)
        lon,lat,ref10,ref12,ref13= get_refs(a, file1)
        print('ok')
        clon,clat,tbb,ref12 = get_cloud(lat,lon,ref10,ref12,ref13)
        print('ok')
        drive_picture(lat, lon, clat, clon, ref12, tbb)
        listf = a.split('_')
        timeini = listf[9]
        timefin = listf[10]
        dpi = listf[11]
        name = timeini +'——'+timefin+'——'+dpi+'深对流云'
        plt.title(name,fontsize=14)
        path = 'D:/'+name+'.jpg'
        plt.savefig(path)
        plt.show()
        self.label.setText('D:/'+name) 
        #return path
    '''
    def open_form2(self): #传递信号
       
        self.signal_1.emit(self.label.text())
   '''     

if __name__ == '__main__':
    import sys 
    import os
    import time    
    def get(relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    file1 ='GEO.FengYun-4A.xxxcgms.4000M.104DEG.HDF5'
    file1 = get(file1)
    print(file1)



    app = QtWidgets.QApplication(sys.argv)
    
# 创建启动界面，支持png透明图片
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap(get('ini.jpg')))
    splash.show()

# 可以显示启动信息
    splash.showMessage('正在加载……')
    time.sleep(2)
# 关闭启动画面
    splash.close() 
    mainWin = QMainWindow()
    
    mainWin.setGeometry(300, 300, 800, 800)
    mainWin.setWindowTitle("4KM级FY-4A深对流云可视化平台")
    
    mainWin.setWindowIcon(QIcon(get("yun.ico")))
    #import ctypes
    #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    
    #apply_stylesheet(mainWin, theme='dark_amber.xml')
    
    # 右侧的widget 默认初始是win1 点击button切换
    win1 = App()
    #win1.setStyleSheet("background-color:dark;")
    win2 = plot() 

    apply_stylesheet(win1, theme='light_cyan.xml')
    apply_stylesheet(win2, theme='light_cyan.xml')
    # centralWidget用来对mainWin进行布局
    centralWidget = QWidget()
    # 水平布局 用来放左侧菜单栏与可变的widget
    hbox = QHBoxLayout()
    # 垂直布局 用来放置切换widget的button
    vboxLeft = QVBoxLayout()
    # 两个button 用来切换右侧的 widget
    btn1 = QPushButton("数据选择和预览", centralWidget)
    btn1.setStyleSheet("font-size:20px;font-weight:bold;font-family:宋体;")
    btn2 = QPushButton("绘制界面", centralWidget)
    btn2.setStyleSheet("font-size:20px;font-weight:bold;font-family:宋体;")
    apply_stylesheet(btn1, theme='light_cyan.xml')
    apply_stylesheet(btn2, theme='light_cyan.xml')
    # 将两个button放入垂直布局中
    vboxLeft.addWidget(btn1)
    vboxLeft.addWidget(btn2)
 
    # hbox中加入垂直布局vboxLeft
    hbox.addLayout(vboxLeft)
    # hbox中加入默认的win1
    hbox.addWidget(win1)
 
    # btn1 btn2绑定点击事件
    # 点击btn1 先将hbox中的第二个(下标为1)的控件的parent设置为None 再将hbox的下标1处插入一个我们希望显示的控件
    btn1.clicked.connect(lambda :(hbox.itemAt(1).widget().setParent(None), hbox.insertWidget(1, win1)))
    btn2.clicked.connect(lambda :(hbox.itemAt(1).widget().setParent(None), hbox.insertWidget(1, win2)))
    # 将hbox布局设给centralWidget
    centralWidget.setLayout(hbox)
    # 将centralWidget设给mainWin
    mainWin.setCentralWidget(centralWidget)
 
    
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap(get("bg.jpg"))))
    mainWin.setPalette(palette)   
    
    mainWin.show()
    sys.exit(app.exec_())