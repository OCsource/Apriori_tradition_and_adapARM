# !/usr/bin/python3
# -*- coding : UTF-8 -*-
# @author   : 关宅宅
# @time     : 2018-10-13 18:01
# @file     : window.py
# @Software : PyCharm Community Edition
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLineEdit,QLabel,QTextEdit,QMessageBox,QFileDialog,QComboBox
sys.path.append('D:/Python3.6-32/python 0_1/BusinessIntelligence')
import dealData

#创建窗口
class Window(QWidget):

    # 全局变量,TXT为文档路径,METHOD为方法选择
    TXT = "0"
    METHOD = True

    def __init__(self):
        super().__init__()
        self.initUI()

    # 界面布局
    def initUI(self):
        global TXT
        TXT = "defaultTxt.txt"

        self.minSup = QLabel("最小支持度：",self)
        self.minCon = QLabel("最小置信度：", self)
        self.combobox = QComboBox(self)
        self.conLine = QLineEdit(self)
        self.supLine = QLineEdit(self)
        self.runing = QPushButton("运行", self)
        self.empty = QPushButton("清空",self)
        self.cent1 = QLabel("%",self)
        self.cent2 = QLabel("%", self)
        self.listLb = QLabel("购物清单：",self)
        self.importing = QPushButton("导入",self)
        self.linkLb1 = QLabel("候选项集：",self)
        self.linkLb2 = QLabel("频繁项集：", self)
        self.resultLb = QLabel("关联规则：",self)
        self.goodsList = QTextEdit(self)
        self.goodsLink1 = QTextEdit(self)
        self.goodsLink2 = QTextEdit(self)
        self.result = QTextEdit(self)
        self.ins = QPushButton("添加",self)
        self.sure = QPushButton("确定",self)
        self.cancel = QPushButton("取消",self)
        self.insList = QLineEdit(self)

        # 设置各控件事件
        self.ins.clicked.connect(self.insert)
        self.cancel.clicked.connect(self.redo)
        self.sure.clicked.connect(self.do)
        self.runing.clicked.connect(self.start)
        self.empty.clicked.connect(self.setEmpty)
        self.importing.clicked.connect(self.choose)
        self.combobox.currentIndexChanged[str].connect(self.changeComBox)

        # 设置控件属性
        self.combobox.resize(72,20)
        self.supLine.resize(35,20)
        self.conLine.resize(35,20)
        self.goodsList.resize(160,260)
        self.goodsLink1.resize(180,380)
        self.goodsLink2.resize(180, 380)
        self.result.resize(560,130)
        self.combobox.addItems(['传统算法', 'ARM算法'])
        self.goodsList.setReadOnly(True)
        self.goodsLink1.setReadOnly(True)
        self.goodsLink2.setReadOnly(True)
        self.result.setReadOnly(True)
        self.sure.setVisible(False)
        self.cancel.setVisible(False)
        self.goodsList.setText(self.getTxt(TXT))
        self.insList.resize(160,20)
        self.insList.setVisible(False)

        # 设置控件位置
        self.combobox.move(0, 0)
        self.minSup.move(20, 28)
        self.minCon.move(170,28)
        self.supLine.move(90, 24)
        self.conLine.move(240, 24)
        self.cent1.move(130,28)
        self.cent2.move(280,28)
        self.runing.move(340,24)
        self.empty.move(460,24)
        self.listLb.move(20,60)
        self.importing.move(106,54)
        self.goodsList.move(20,80)
        self.linkLb1.move(200,60)
        self.linkLb2.move(400, 60)
        self.goodsLink1.move(200,80)
        self.goodsLink2.move(400, 80)
        self.ins.move(60,360)
        self.insList.move(20, 400)
        self.sure.move(20,440)
        self.cancel.move(106,440)
        self.resultLb.move(20,480)
        self.result.move(20, 500)

        self.resize(600,650)
        self.setWindowTitle('关联规则计算')

    # 下拉列表事件
    def changeComBox(self, str):
        global METHOD
        METHOD = False if str == 'ARM算法' else True
        if METHOD == False:
            self.conLine.setReadOnly(True)
            self.conLine.setStyleSheet("QLineEdit{background-color: #CCCCFF}")
            self.supLine.setReadOnly(True)
            self.supLine.setStyleSheet("QLineEdit{background-color: #CCCCFF}")
        else:
            self.conLine.setReadOnly(False)
            self.conLine.setStyleSheet("QLineEdit{background-color: #FFFFFF}")
            self.supLine.setReadOnly(False)
            self.supLine.setStyleSheet("QLineEdit{background-color: #FFFFFF}")

    # 设置按钮runing事件
    def start(self):
        x = self.supLine.text()
        y = self.conLine.text()
        z = self.goodsList.toPlainText()
        if (x and y and z) or not METHOD:
            self.goodsLink1.clear()
            self.goodsLink2.clear()
            self.result.clear()
            if METHOD:
                sup = float(x) / 100
                con = float(y) / 100
                data = dealData.getResultByTrad(TXT, sup, con)
            else:
                data = dealData.getResultByARM(TXT)
            self.textAppend(data[0], self.goodsLink1)
            self.textAppend(data[1], self.goodsLink2)
            self.resultAppend(data[2], self.result)
        else:
            QMessageBox.about(self, "ERROR", "请确保最小置信度,最小支持度和购物清单都有值！")

    # 设置按钮empty事件
    def setEmpty(self):
        self.supLine.clear()
        self.conLine.clear()
        self.goodsLink1.clear()
        self.goodsLink2.clear()
        self.result.clear()

    # 设置按钮importing事件
    def choose(self):
        global TXT
        filename = QFileDialog.getOpenFileName(self)
        TXT = (list(filename)[0]).split("/")[-1]
        if TXT:
            pass
        else:
            TXT = "defaultTxt.txt"
        self.goodsList.clear()
        self.goodsList.setText(self.getTxt(TXT))
        QMessageBox.about(self, "OK", "导入文件" + TXT + "成功")

    # 设置按钮mod事件
    def insert(self):
       self.insList.setVisible(True)
       self.sure.setVisible(True)
       self.cancel.setVisible(True)

    # 设置按钮sure事件
    def do(self):
        msg = self.insList.text()
        if self.checkMsg(msg,TXT):
            QMessageBox.about(self, "ERROR", "清单列表中已有该项！")
        else:
            self.setTxt(msg,TXT)
            self.goodsList.setText(self.getTxt(TXT))
        self.insList.setText("")
        self.insList.setVisible(False)
        self.sure.setVisible(False)
        self.cancel.setVisible(False)

    # 设置按钮cancel事件
    def redo(self):
        self.goodsList.setText(self.getTxt(TXT))
        self.insList.setVisible(False)
        self.sure.setVisible(False)
        self.cancel.setVisible(False)

    # 得到清单数据
    def getTxt(self,txt):
        data = ''
        if txt == "0":
            txt = "defaultTxt.txt"
        else:
            pass
        fout = open(txt, 'r')
        lines = fout.readlines()
        for line in lines:
            data = data + line
        fout.close()
        return data

    #修改清单数据
    def setTxt(self,msg,txt):
        if txt == "0":
            txt = "defaultTxt.txt"
        else:
            pass
        fin = open(txt, "a")
        fin.write(msg + '\n')
        fin.close()

    #检查清单是否已有该项
    def checkMsg(self, msg,txt):
        if txt == "0":
            txt = "defaultTxt.txt"
        else:
            pass
        check = True
        fout = open(txt, 'r')
        lines = fout.readlines()
        if lines:
            for line in lines:
                # print(line.strip(),msg.strip(),line.strip()==msg.strip())
                if msg.strip() in line.strip():
                    check = True
                    break
                else:
                    check = False
        else:
            check = False
        fout.close()
        # print(check)
        return check

    # 添加候选项集和频繁项集的函数
    def textAppend(self,data,widget):
        i = 0
        if widget == self.goodsLink1:
            s = "候选项集C"
        else :
            s = "频繁项集L"
        for k in data:
            if len(k.split(',')) != i:
                if i != 0:
                    widget.append("- - - - - - - - - - - - -")
                widget.append(s + str(len(k.split(','))) + "\n")
                i = len(k.split(','))
            if data[k] != 0 :widget.append(k + " : " + str(data[k]))

    # 添加结果集
    def resultAppend(self,data,widget):
        i = 1
        s = ""
        widget.append("最终的关联规则为：\n")
        for m in data:
            s = s + m + "=" + str(round(data[m],2) * 100) + "%  "
            if i % 3 == 0 or i == len(data):
                widget.append(s)
                s = ""
            i += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())