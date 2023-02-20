import json

import requests
from PyQt5.QtCore import Qt
from qtpy import QtCore
from PyQt5 import QtGui
import login
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from UI import zhujiemianui
from UI.guofenshiandsheMain import guofenshiandsheMain
from UI.logintest import loginMain
from UI.shexiangtoutest import shixiangtouMain
from UI.zhujiemianui import Ui_MainWindow


class zhujiemainMain(QMainWindow):
    def __init__(self,username):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget_3.hide()
        # self.ui.widget_5.hide()
        self.ui.widget_6.hide()
        self.username=username
        self.time=0
        self.list1=[]
        self.ui.yonghuminglb.setText(username)
        self.slots_init()

    def slots_init(self):
        self.ui.functionBT.clicked.connect(self.change_widget)
        self.ui.gerenBT.clicked.connect(self.change_widget3)
        # self.ui.guofenBT.clicked.connect(self.change_widget5)
        self.ui.zuheydBT.clicked.connect(self.change_widget6)
        self.ui.shendunBT.clicked.connect(self.shendunBT)
        self.ui.fuwochengBT.clicked.connect(self.fuwochengBT)
        self.ui.yintiBT.clicked.connect(self.yintiBT)
        self.ui.yalingBT.clicked.connect(self.yalingBT)
        self.ui.zzyalingBT.clicked.connect(self.zzyalingBT)
        self.ui.cetaituiBT.clicked.connect(self.cetaituiBT)
        self.ui.tunqiaoBT.clicked.connect(self.tunqiaoBT)
        self.ui.yangwoqizuoBT.clicked.connect(self.yangwoqizuoBT)
        self.ui.chexiangkaiheBT.clicked.connect(self.chexiangkaiheBT)
        self.ui.xiaduntingBT.clicked.connect(self.xiaduntingBT)
        self.ui.juanfuBT.clicked.connect(self.juanfuBT)
        # 哑铃硬拉
        self.ui.pushButton_14.clicked.connect(self.pushButton_14)
        self.ui.tuichuBT.clicked.connect(self.tuichuBT)
        self.ui.fanhuiBT.clicked.connect(self.fanhuiBT)
        self.ui.gerenBT.clicked.connect(self.gerenBT)

        # self.ui.jianzicaoBT.clicked.connect(self.jianzicaoBT)
        # self.ui.baduanjinBT.clicked.connect(self.baduanjinBT)
        # self.ui.yijinjingBT.clicked.connect(self.yijinjingBT)
        # self.ui.gboticaoBT.clicked.connect(self.gboticaoBT)
        # self.ui.taijiquanBT.clicked.connect(self.taijiquanBT)
        # self.ui.wuqinxiBT.clicked.connect(self.wuqinxiBT)
        self.ui.qinglingBT.clicked.connect(self.qingling)


        self.ui.querenBT.clicked.connect(self.querenBT)
    def gerenBT(self):
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setHorizontalHeaderLabels(["序号","日期","运动名称","运动计数","运动评分","运动时长"])
        try:
            data = {"suid": self.username}
            url = "http://43.136.75.221:8085/sportdata"
            r = requests.post(url, data)
            jsonStr = json.dumps(r.json())
            res = json.loads(jsonStr)
            for i, item in enumerate(res):
                self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)
                # print(str(item['sid']))
                sid=QTableWidgetItem(str(item['sid']))
                sid.setTextAlignment(Qt.AlignCenter)  # 设置文字显示居中
                sid.setFlags(Qt.ItemIsEnabled)  # 设置表格不可编辑模式
                self.ui.tableWidget.setItem(
                    self.ui.tableWidget.rowCount() - 1, 0, sid)

                stime = QTableWidgetItem(str(item['stime']))
                stime.setTextAlignment(Qt.AlignCenter)  # 设置文字显示居中
                stime.setFlags(Qt.ItemIsEnabled)  # 设置表格不可编辑模式
                self.ui.tableWidget.setItem(
                    self.ui.tableWidget.rowCount() - 1, 1, stime)

                sname = QTableWidgetItem(str(item['sname']))
                sname.setTextAlignment(Qt.AlignCenter)  # 设置文字显示居中
                sname.setFlags(Qt.ItemIsEnabled)  # 设置表格不可编辑模式
                self.ui.tableWidget.setItem(
                    self.ui.tableWidget.rowCount() - 1, 2, sname)

                scount = QTableWidgetItem(str(item['scount']))
                scount.setTextAlignment(Qt.AlignCenter)  # 设置文字显示居中
                scount.setFlags(Qt.ItemIsEnabled)  # 设置表格不可编辑模式
                self.ui.tableWidget.setItem(
                    self.ui.tableWidget.rowCount() - 1, 3, scount)

                sscore = QTableWidgetItem(str(item['sscore']))
                sscore.setTextAlignment(Qt.AlignCenter)  # 设置文字显示居中
                sscore.setFlags(Qt.ItemIsEnabled)  # 设置表格不可编辑模式
                self.ui.tableWidget.setItem(
                    self.ui.tableWidget.rowCount() - 1, 4, sscore)

                syundongtime = QTableWidgetItem(str(item['syundongtime']))
                syundongtime.setTextAlignment(Qt.AlignCenter)  # 设置文字显示居中
                syundongtime.setFlags(Qt.ItemIsEnabled)  # 设置表格不可编辑模式
                self.ui.tableWidget.setItem(
                    self.ui.tableWidget.rowCount() - 1, 5, syundongtime)
        except Exception as e:
            print(e)



    def tuichuBT(self):
        self.close()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.clear()
        self.login = loginMain()
        self.login.show()
    def fanhuiBT(self):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.clear()
        self.change_widget()

    def shendunBT(self):
        self.hide()
        self.shendun = shixiangtouMain("shendunCSV", "down",self.username,"深蹲")
        self.shendun.show()


    def fuwochengBT(self):
        self.hide()
        self.fuwocheng = shixiangtouMain("fowoshenCSV", "down", self.username,"俯卧撑")
        self.fuwocheng.show()

    def yintiBT(self):
        self.hide()
        self.yinti = shixiangtouMain("yintiCSV", "down", self.username,"引体")
        self.yinti.show()

    def yalingBT(self):
        self.hide()
        self.yaling = shixiangtouMain("yalingCsv_out", "down", self.username,"哑铃")
        self.yaling.show()

    def zzyalingBT(self):
        self.hide()
        self.zzyaling = shixiangtouMain("zhanziyalingCsv_out", "down", self.username,"站姿哑铃")
        self.zzyaling.show()

    def tunqiaoBT(self):
        self.hide()
        self.tunqiao = shixiangtouMain("tunqiaoCSV_out", "down", self.username,"臀桥")
        self.tunqiao.show()
# 未完成
    def yangwoqizuoBT(self):
        self.hide()
        self.yangwoqizuo = shixiangtouMain("shendunCSV", "down", self.username,"仰卧起坐")
        self.yangwoqizuo.show()

    def cetaituiBT(self):
        self.hide()
        self.cetaitui = shixiangtouMain("cetaituiCSV_out", "down", self.username,"侧抬腿")
        self.cetaitui.show()

    def chexiangkaiheBT(self):
        self.hide()
        self.shendun = shixiangtouMain("cetaituiCSV_out", "down", self.username,"侧向开合")
        self.shendun.show()
# 未完成
    def xiaduntingBT(self):
        self.hide()
        self.shendun = shixiangtouMain("shendunCSV", "down", self.username,"下蹲挺")
        self.shendun.show()

    # 未完成
    def juanfuBT(self):
        self.hide()
        self.shendun = shixiangtouMain("shendunCSV", "down", self.username,"卷腹")
        self.shendun.show()

    # 未完成
    def pushButton_14(self):
        self.hide()
        self.shendun = shixiangtouMain("shendunCSV", "down", self.username,"哑铃硬拉")
        self.shendun.show()
    # def jianzicaoBT(self):
    #     self.hide()
    #     self.jianzicao=guofenshiandsheMain(self.username,"毽子操",r"D:\pythonProject1\UI\shiping\毽子操.mp4")
    #     self.jianzicao.show()
    # def baduanjinBT(self):
    #     self.hide()
    #     self.baduanjin = guofenshiandsheMain(self.username, "八段锦", r"D:\pythonProject1\UI\shiping\八段锦.mp4")
    #     self.baduanjin.show()
    # def yijinjingBT(self):
    #     self.hide()
    #     self.yijinjing = guofenshiandsheMain(self.username, "易筋经", r"D:\pythonProject1\UI\shiping\易筋经.mp4")
    #     self.yijinjing.show()
    # def gboticaoBT(self):
    #     self.hide()
    #     self. gboticao = guofenshiandsheMain(self.username, "广播体操", r"D:\pythonProject1\UI\shiping\广播体操.mp4")
    #     self. gboticao.show()
    # def taijiquanBT(self):
    #     self.hide()
    #     self.taijiquan = guofenshiandsheMain(self.username, "太极拳", r"D:\pythonProject1\UI\shiping\太极拳.mp4")
    #     self.taijiquan.show()
    # def wuqinxiBT(self):
    #     self.hide()
    #     self.wuqinxi = guofenshiandsheMain(self.username, "五禽戏", r"D:\pythonProject1\UI\shiping\五禽戏.mp4")
    #     self.wuqinxi.show()

    def change_widget3(self):
        self.ui.widget.hide()
        # self.ui.widget_5.hide()
        self.ui.widget_6.hide()
        self.ui.widget_3.show()

    def change_widget(self):
        self.ui.widget_3.hide()
        # self.ui.widget_5.hide()
        self.ui.widget_6.hide()
        self.ui.widget.show()

    # def change_widget5(self):
    #     self.ui.widget_3.hide()
    #     self.ui.widget.hide()
    #     self.ui.widget_6.hide()
    #     self.ui.widget_5.show()


    def change_widget6(self):
        self.ui.widget_3.hide()
        self.ui.widget.hide()
        # self.ui.widget_5.hide()
        self.ui.widget_6.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    def querenBT(self):
        if self.ui.spinBox.value()==0:
            print("不对劲")
        else:
            self.list1.clear()
            self.time=self.ui.spinBox.value()
            print(self.time)
            if self.ui.shendunCB.isChecked():
                self.list1.append("深蹲")
                self.list1.append("shendunCSV")
            if self.ui.fuwochengCB.isChecked():
                self.list1.append("俯卧撑")
                self.list1.append("fowoshenCSV")
            if self.ui.yintiCB.isChecked():
                self.list1.append("引体向上")
                self.list1.append("yintiCSV")
            if self.ui.yalingCB.isChecked():
                self.list1.append("哑铃")
                self.list1.append("yalingCsv_out")
            if self.ui.zzyalingCB.isChecked():
                self.list1.append("站姿哑铃")
                self.list1.append("zhanziyalingCsv_out")
            if self.ui.cetaituiCB.isChecked():
                self.list1.append("侧抬腿")
                self.list1.append("cetaituiCSV_out")
            if self.ui.tunqiaoCB.isChecked():
                self.list1.append("臀桥")
                self.list1.append("tunqiaoCSV_out")
            if self.ui.yangwoqizuoCB.isChecked():
                self.list1.append("仰卧起坐")
                self.list1.append("tunqiaoCSV_out")
            if self.ui.cexiangkaiheCB.isChecked():
                self.list1.append("侧向开合")
                self.list1.append("cetaituiCSV_out")
            if self.ui.xiaduntingCB.isChecked():
                self.list1.append("下蹲挺")
                self.list1.append("cetaituiCSV_out")
            if self.ui.juanfuCB.isChecked():
                self.list1.append("卷腹")
                self.list1.append("cetaituiCSV_out")
            if self.ui.yalingyinglaCB.isChecked():
                self.list1.append("哑铃硬拉")
                self.list1.append("cetaituiCSV_out")
            print(self.list1)
            self.hide()
            from UI.jishiyundongMain import jishuyundongMain
            self.jishijiemian=jishuyundongMain(self.list1,self.time,self.username)
            self.jishijiemian.show()
    def qingling(self):
        self.ui.spinBox.setValue(0)
        listcb=[self.ui.shendunCB,self.ui.fuwochengCB,self.ui.yintiCB,self.ui.yalingCB,self.ui.zzyalingCB,self.ui.cetaituiCB,
                self.ui.tunqiaoCB,self.ui.yangwoqizuoCB,self.ui.cexiangkaiheCB,self.ui.xiaduntingCB,self.ui.juanfuCB,self.ui.yalingyinglaCB]
        for i in listcb:
            i.setChecked(False)




# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = zhujiemainMain()
#     win.show()
#     sys.exit(app.exec_())
