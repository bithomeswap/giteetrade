#【需要在指定文件夹下面执行】
# pip install PyQt5
# pip install pdf2docx
# pip install -r C:\Users\Administrator\gitee\trade\【应用】\【格式转换、压缩、解压缩】\pdf2word\requirements.txt
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_MainWindow import Ui_MainWindow
from MainWindow import MainWindow
import sys

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  app.setStyle("Fusion")  # 设置窗口风格
  MainWindow = MainWindow() # 创建窗体对象
  MainWindow.show() # 显示窗体
  sys.exit(app.exec_())
