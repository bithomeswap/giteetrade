# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTextBrowser, QTextEdit, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(738, 593)
        MainWindow.setMaximumSize(QSize(750, 593))
        icon = QIcon()
        icon.addFile(u":/images/images/music.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(2.000000000000000)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_9 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.widget.setStyleSheet(u"QWidget#widget{\n"
"	background:rgb(255, 250, 232);\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"    border-top-left-radius:10px;\n"
"    border-bottom-left-radius:10px;\n"
"}\n"
"\n"
"QListWidget{\n"
"	font: 9pt \"LXGW WenKai\";\n"
"	background:rgb(255, 250, 232);\n"
"}\n"
"\n"
"QScrollBar:vertical{\n"
"    width:8px;\n"
"    border:none;\n"
"    background:rgba(0,0,0,0%);\n"
"    margin:0px,0px,0px,0px;\n"
"    padding-top:9px;\n"
"    padding-bottom:9px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,25%);\n"
"    border-radius:4px;\n"
"    min-height:20;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover\n"
"{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,50%);\n"
"    border-radius:4px;\n"
"    min-height:20;\n"
"}\n"
"QScrollBar::add-page:vertical{\n"
"    background-color:rgb(255, 250, 232);\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::sub-page:vertical{\n"
"    background-color:rgb(255, 250, 232);\n"
"}\n"
"QScrollBar::add-lin"
                        "e:vertical\n"
"{\n"
"    height:9px;width:8px;\n"
"	image: url(:/icon/images/arrow-down-bold.png);\n"
"    subcontrol-position:bottom;\n"
"}\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"    height:9px;width:8px;\n"
"    image: url(:/icon/images/arrow-up-bold.png);\n"
"    subcontrol-position:top;\n"
"}")
        self.verticalLayout_5 = QVBoxLayout(self.widget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.widget_top = QWidget(self.widget)
        self.widget_top.setObjectName(u"widget_top")
        self.widget_top.setMinimumSize(QSize(0, 28))
        self.widget_top.setMaximumSize(QSize(16777215, 28))
        self.widget_top.setMouseTracking(False)
        self.widget_top.setStyleSheet(u"QWidget#widget_top{\n"
"    background:rgb(245, 36, 67);\n"
"	border-top-right-radius:10px;\n"
"    border-top-left-radius:10px;\n"
"}")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_top)
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout_lights_btn = QHBoxLayout()
        self.horizontalLayout_lights_btn.setSpacing(6)
        self.horizontalLayout_lights_btn.setObjectName(u"horizontalLayout_lights_btn")
        self.pushButton_red = QPushButton(self.widget_top)
        self.pushButton_red.setObjectName(u"pushButton_red")
        self.pushButton_red.setMinimumSize(QSize(12, 12))
        self.pushButton_red.setMaximumSize(QSize(12, 12))
        self.pushButton_red.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_red.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_red.setStyleSheet(u"QPushButton{background:#F76677;border-radius:6px;}QPushButton:hover{background:red;}")

        self.horizontalLayout_lights_btn.addWidget(self.pushButton_red)

        self.pushButton_yellow = QPushButton(self.widget_top)
        self.pushButton_yellow.setObjectName(u"pushButton_yellow")
        self.pushButton_yellow.setMinimumSize(QSize(12, 12))
        self.pushButton_yellow.setMaximumSize(QSize(12, 12))
        self.pushButton_yellow.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_yellow.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_yellow.setStyleSheet(u"QPushButton{background:#F7D674;border-radius:6px;}\n"
"QPushButton:hover{background:yellow;}")

        self.horizontalLayout_lights_btn.addWidget(self.pushButton_yellow)

        self.pushButton_green = QPushButton(self.widget_top)
        self.pushButton_green.setObjectName(u"pushButton_green")
        self.pushButton_green.setMinimumSize(QSize(12, 12))
        self.pushButton_green.setMaximumSize(QSize(12, 12))
        self.pushButton_green.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_green.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_green.setStyleSheet(u"QPushButton{background:#6DDF6D;border-radius:6px;}QPushButton:hover{background:green;}")

        self.horizontalLayout_lights_btn.addWidget(self.pushButton_green)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_lights_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_update = QPushButton(self.widget_top)
        self.pushButton_update.setObjectName(u"pushButton_update")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_update.sizePolicy().hasHeightForWidth())
        self.pushButton_update.setSizePolicy(sizePolicy)
        self.pushButton_update.setMinimumSize(QSize(50, 0))
        self.pushButton_update.setMaximumSize(QSize(50, 16777215))
        self.pushButton_update.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_update.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_update.setStyleSheet(u"QPushButton{\n"
"	background:rgb(245, 36, 67);\n"
"	border-radius:8px;\n"
"	font: 9pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"	color: #ff7043;\n"
"}\n"
"QPushButton:hover{\n"
"	background:#e60039;\n"
"}\n"
"")

        self.horizontalLayout_3.addWidget(self.pushButton_update)


        self.verticalLayout_5.addWidget(self.widget_top)

        self.horizontalLayout_body = QHBoxLayout()
        self.horizontalLayout_body.setSpacing(5)
        self.horizontalLayout_body.setObjectName(u"horizontalLayout_body")
        self.horizontalLayout_body.setContentsMargins(10, 10, 10, 10)
        self.horizontalSpacer_2 = QSpacerItem(20, 100, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_body.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.horizontalLayout_body.addLayout(self.horizontalLayout_2)

        self.verticalLayout_musiclist = QVBoxLayout()
        self.verticalLayout_musiclist.setSpacing(4)
        self.verticalLayout_musiclist.setObjectName(u"verticalLayout_musiclist")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout_musiclist.addLayout(self.verticalLayout_2)

        self.label_list_name = QLabel(self.widget)
        self.label_list_name.setObjectName(u"label_list_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_list_name.sizePolicy().hasHeightForWidth())
        self.label_list_name.setSizePolicy(sizePolicy1)
        self.label_list_name.setStyleSheet(u"font: 10pt \"LXGW WenKai\";")

        self.verticalLayout_musiclist.addWidget(self.label_list_name)

        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_musiclist.addWidget(self.comboBox)

        self.checkBox_1 = QCheckBox(self.widget)
        self.checkBox_1.setObjectName(u"checkBox_1")
        self.checkBox_1.setEnabled(True)

        self.verticalLayout_musiclist.addWidget(self.checkBox_1)

        self.checkBox_2 = QCheckBox(self.widget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout_musiclist.addWidget(self.checkBox_2)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout_musiclist.addWidget(self.widget_2)

        self.comboBox_2 = QComboBox(self.widget)
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.verticalLayout_musiclist.addWidget(self.comboBox_2)

        self.checkBox_3 = QCheckBox(self.widget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout_musiclist.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.widget)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout_musiclist.addWidget(self.checkBox_4)

        self.comboBox_4 = QComboBox(self.widget)
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.verticalLayout_musiclist.addWidget(self.comboBox_4)

        self.checkBox_6 = QCheckBox(self.widget)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.verticalLayout_musiclist.addWidget(self.checkBox_6)

        self.checkBox_5 = QCheckBox(self.widget)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout_musiclist.addWidget(self.checkBox_5)

        self.comboBox_5 = QComboBox(self.widget)
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.verticalLayout_musiclist.addWidget(self.comboBox_5)

        self.checkBox_7 = QCheckBox(self.widget)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setCheckable(True)
        self.checkBox_7.setChecked(False)
        self.checkBox_7.setAutoRepeat(False)

        self.verticalLayout_musiclist.addWidget(self.checkBox_7)

        self.checkBox_8 = QCheckBox(self.widget)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.verticalLayout_musiclist.addWidget(self.checkBox_8)

        self.comboBox_3 = QComboBox(self.widget)
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.verticalLayout_musiclist.addWidget(self.comboBox_3)

        self.checkBox_9 = QCheckBox(self.widget)
        self.checkBox_9.setObjectName(u"checkBox_9")

        self.verticalLayout_musiclist.addWidget(self.checkBox_9)

        self.checkBox_10 = QCheckBox(self.widget)
        self.checkBox_10.setObjectName(u"checkBox_10")

        self.verticalLayout_musiclist.addWidget(self.checkBox_10)

        self.comboBox_6 = QComboBox(self.widget)
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.verticalLayout_musiclist.addWidget(self.comboBox_6)

        self.checkBox_11 = QCheckBox(self.widget)
        self.checkBox_11.setObjectName(u"checkBox_11")

        self.verticalLayout_musiclist.addWidget(self.checkBox_11)

        self.checkBox_12 = QCheckBox(self.widget)
        self.checkBox_12.setObjectName(u"checkBox_12")

        self.verticalLayout_musiclist.addWidget(self.checkBox_12)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(251, 0))
        self.pushButton.setMaximumSize(QSize(251, 16777215))

        self.verticalLayout_musiclist.addWidget(self.pushButton)


        self.horizontalLayout_body.addLayout(self.verticalLayout_musiclist)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")

        self.horizontalLayout_body.addLayout(self.horizontalLayout_5)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_body.addItem(self.horizontalSpacer_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.horizontalLayout_body.addLayout(self.horizontalLayout)

        self.verticalLayout_lrc = QVBoxLayout()
        self.verticalLayout_lrc.setObjectName(u"verticalLayout_lrc")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_lrc.addLayout(self.verticalLayout)

        self.label_name = QLabel(self.widget)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setEnabled(True)
        self.label_name.setStyleSheet(u"font: 10pt \"LXGW WenKai\";")

        self.verticalLayout_lrc.addWidget(self.label_name)

        self.comboBox_7 = QComboBox(self.widget)
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.verticalLayout_lrc.addWidget(self.comboBox_7)

        self.comboBox_8 = QComboBox(self.widget)
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.setObjectName(u"comboBox_8")

        self.verticalLayout_lrc.addWidget(self.comboBox_8)

        self.comboBox_9 = QComboBox(self.widget)
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.verticalLayout_lrc.addWidget(self.comboBox_9)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setStrikeOut(False)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_lrc.addWidget(self.label_4)

        self.spinBox = QSpinBox(self.widget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(999999999)

        self.verticalLayout_lrc.addWidget(self.spinBox)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setUnderline(True)
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_lrc.addWidget(self.label_6)

        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_lrc.addWidget(self.textBrowser)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei UI"])
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setUnderline(True)
        self.label_5.setFont(font2)
        self.label_5.setStyleSheet(u"")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setWordWrap(False)

        self.verticalLayout_lrc.addWidget(self.label_5)

        self.textBrowser_2 = QTextBrowser(self.widget)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_lrc.addWidget(self.textBrowser_2)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_lrc.addWidget(self.label_7)

        self.textBrowser_3 = QTextBrowser(self.widget)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        self.textBrowser_3.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_lrc.addWidget(self.textBrowser_3)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(350, 0))

        self.verticalLayout_lrc.addWidget(self.pushButton_2)

        self.listWidget_3 = QListWidget(self.widget)
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(True)
        font3.setItalic(True)
        font3.setUnderline(True)
        __qlistwidgetitem = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem.setTextAlignment(Qt.AlignCenter);
        __qlistwidgetitem.setFont(font3);
        font4 = QFont()
        font4.setPointSize(8)
        font4.setBold(True)
        font4.setItalic(False)
        font4.setUnderline(True)
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem1.setTextAlignment(Qt.AlignCenter);
        __qlistwidgetitem1.setFont(font4);
        font5 = QFont()
        font5.setPointSize(8)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setUnderline(True)
        font5.setStrikeOut(False)
        __qlistwidgetitem2 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem2.setTextAlignment(Qt.AlignCenter);
        __qlistwidgetitem2.setFont(font5);
        font6 = QFont()
        font6.setPointSize(8)
        font6.setBold(True)
        font6.setUnderline(True)
        __qlistwidgetitem3 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem3.setTextAlignment(Qt.AlignCenter);
        __qlistwidgetitem3.setFont(font6);
        self.listWidget_3.setObjectName(u"listWidget_3")
        self.listWidget_3.setEnabled(True)
        self.listWidget_3.setMinimumSize(QSize(0, 100))
        self.listWidget_3.setMaximumSize(QSize(16777215, 16777215))
        font7 = QFont()
        font7.setFamilies([u"LXGW WenKai"])
        font7.setPointSize(9)
        font7.setBold(False)
        font7.setItalic(False)
        self.listWidget_3.setFont(font7)
        self.listWidget_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.listWidget_3.setStyleSheet(u"QListView::item:hover {\n"
"	background-color: transparent;\n"
"	border-left: 3px solid #ff441a;\n"
"}\n"
"QListView::item:selected {\n"
"	background-color: transparent;\n"
"}")
        self.listWidget_3.setFrameShape(QFrame.Shape.NoFrame)
        self.listWidget_3.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.verticalLayout_lrc.addWidget(self.listWidget_3)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")

        self.verticalLayout_lrc.addLayout(self.verticalLayout_7)


        self.horizontalLayout_body.addLayout(self.verticalLayout_lrc)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.horizontalLayout_body.addLayout(self.horizontalLayout_4)

        self.horizontalSpacer_3 = QSpacerItem(20, 100, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_body.addItem(self.horizontalSpacer_3)

        self.widget_comment = QWidget(self.widget)
        self.widget_comment.setObjectName(u"widget_comment")
        self.verticalLayout_3 = QVBoxLayout(self.widget_comment)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_body.addWidget(self.widget_comment)


        self.verticalLayout_5.addLayout(self.horizontalLayout_body)

        self.widget_bottom = QWidget(self.widget)
        self.widget_bottom.setObjectName(u"widget_bottom")
        self.widget_bottom.setMinimumSize(QSize(0, 45))
        self.widget_bottom.setMaximumSize(QSize(16777215, 45))
        self.widget_bottom.setStyleSheet(u"QWidget#widget_bottom{\n"
"	background:rgb(245, 36, 67);\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-bottom-right-radius:10px;\n"
"    	border-bottom-left-radius:10px;\n"
"}\n"
"\n"
"QPushButton{\n"
"	border:none;\n"
"}")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_bottom)
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.widget_bottom)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.label)

        self.label_time_end = QLabel(self.widget_bottom)
        self.label_time_end.setObjectName(u"label_time_end")
        self.label_time_end.setMinimumSize(QSize(0, 0))
        self.label_time_end.setStyleSheet(u"font: 9pt \"LXGW WenKai\";\n"
"color: #616161;")

        self.horizontalLayout_6.addWidget(self.label_time_end)

        self.textEdit = QTextEdit(self.widget_bottom)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.textEdit)

        self.label_2 = QLabel(self.widget_bottom)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.label_2)


        self.verticalLayout_5.addWidget(self.widget_bottom)


        self.horizontalLayout_9.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LrcMusicPlayer", None))
        self.pushButton_red.setText("")
        self.pushButton_yellow.setText("")
        self.pushButton_green.setText("")
        self.pushButton_update.setText(QCoreApplication.translate("MainWindow", u"v0.0.0", None))
        self.label_list_name.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">\u804c\u4e1a\u6027\u683c\u6d4b\u8bd5</span></p></body></html>", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"1.\u4e0b\u5217\u54ea\u4e00\u79cd\u662f\u4f60\u7684\u4e00\u822c\u751f\u6d3b\u53d6\u5411?", None))

        self.checkBox_1.setText(QCoreApplication.translate("MainWindow", u"\u53ea\u7ba1\u505a\u5427\u3002", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u627e\u51fa\u591a\u79cd\u4e0d\u540c\u9009\u62e9\u3002", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"2.\u4f60\u559c\u6b22\u81ea\u5df1\u7684\u54ea\u79cd\u6027\u683c\uff1f", None))

        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u51b7\u9759\u800c\u7406\u6027\u3002", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\u70ed\u60c5\u800c\u4f53\u8c05\u3002", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("MainWindow", u"3.\u4f60\u64c5\u957f", None))

        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"\u5728\u6709\u9700\u8981\u65f6\u95f4\u65f6\u540c\u65f6\u534f\u8c03\u8fdb\u884c\u591a\u9879\u5de5\u4f5c\u3002", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"\u4e13\u6ce8\u5728\u67d0\u4e00\u9879\u5de5\u4f5c\u4e0a\uff0c\u76f4\u81f3\u628a\u5b83\u5b8c\u6210\u4e3a\u6b62\u3002", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("MainWindow", u"4.\u4f60\u53c2\u4e0e\u793e\u4ea4\u805a\u4f1a\u65f6", None))

        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"\u603b\u662f\u80fd\u8ba4\u8bc6\u65b0\u670b\u53cb\u3002", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"\u53ea\u8ddf\u51e0\u4e2a\u4eb2\u5bc6\u631a\u53cb\u5446\u5728\u4e00\u8d77\u3002", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"5.\u5f53\u4f60\u5c1d\u8bd5\u4e86\u89e3\u67d0\u4e9b\u4e8b\u60c5\u65f6\uff0c\u4e00\u822c\u4f60\u4f1a", None))

        self.checkBox_9.setText(QCoreApplication.translate("MainWindow", u"\u5148\u8981\u4e86\u89e3\u7ec6\u8282\u3002", None))
        self.checkBox_10.setText(QCoreApplication.translate("MainWindow", u"\u5148\u4e86\u89e3\u6574\u4f53\u60c5\u51b5\uff0c\u7ec6\u8282\u5bb9\u540e\u518d\u8c08\u3002", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("MainWindow", u"6.\u4f60\u5bf9\u4e0b\u5217\u54ea\u65b9\u9762\u8f83\u611f\u5174\u8da3\uff1f", None))

        self.checkBox_11.setText(QCoreApplication.translate("MainWindow", u"\u77e5\u9053\u522b\u4eba\u7684\u60f3\u6cd5\u3002", None))
        self.checkBox_12.setText(QCoreApplication.translate("MainWindow", u"\u77e5\u9053\u522b\u4eba\u7684\u611f\u53d7\u3002", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4", None))
        self.label_name.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">\u9ad8\u8003\u5fd7\u613f\u586b\u62a5</span></p></body></html>", None))
        self.comboBox_7.setItemText(0, QCoreApplication.translate("MainWindow", u"\u6240\u5728\u7701\u4efd\uff08\u5fc5\u9009\u9879\uff09", None))
        self.comboBox_7.setItemText(1, QCoreApplication.translate("MainWindow", u"\u6cb3\u5317", None))

        self.comboBox_8.setItemText(0, QCoreApplication.translate("MainWindow", u"\u9996\u9009\u79d1\u76ee\uff08\u5fc5\u9009\u9879\uff09", None))
        self.comboBox_8.setItemText(1, QCoreApplication.translate("MainWindow", u"\u7269\u7406", None))
        self.comboBox_8.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5386\u53f2", None))

        self.comboBox_9.setItemText(0, QCoreApplication.translate("MainWindow", u"\u6b21\u9009\u79d1\u76ee", None))
        self.comboBox_9.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5730\u7406\u3001\u653f\u6cbb", None))
        self.comboBox_9.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5316\u5b66\u3001\u751f\u7269", None))
        self.comboBox_9.setItemText(3, QCoreApplication.translate("MainWindow", u"\u5730\u7406\u3001\u5316\u5b66", None))
        self.comboBox_9.setItemText(4, QCoreApplication.translate("MainWindow", u"\u5730\u7406\u3001\u751f\u7269", None))
        self.comboBox_9.setItemText(5, QCoreApplication.translate("MainWindow", u"\u5316\u5b66\u3001\u653f\u6cbb", None))
        self.comboBox_9.setItemText(6, QCoreApplication.translate("MainWindow", u"\u751f\u7269\u3001\u653f\u6cbb", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u8003\u8bd5\u6392\u540d\uff08\u5fc5\u586b\uff0c\u53c2\u8003\u4e00\u5206\u4e00\u6863\u8868\u586b\u5199\uff09", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u804c\u4e1a\u6027\u683c\u8bf4\u660e\uff08\u6839\u636e\u804c\u4e1a\u6027\u683c\u6d4b\u8bd5\u751f\u6210\uff09", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8\u4e13\u4e1a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u610f\u5411\u4e13\u4e1a", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4", None))

        __sortingEnabled = self.listWidget_3.isSortingEnabled()
        self.listWidget_3.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget_3.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u8054\u7cfb\u65b9\u5f0f", None));
        ___qlistwidgetitem1 = self.listWidget_3.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u5fae\u4fe1\uff1abithomeAI", None));
        ___qlistwidgetitem2 = self.listWidget_3.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u7535\u8bdd\uff1a19331839916", None));
        ___qlistwidgetitem3 = self.listWidget_3.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u300c\u9ad8\u8003\u5fd7\u613f\u300d\u4ea4\u6d41\u7fa4\uff1ahttps://t.zsxq.com/x8PTu", None));
        self.listWidget_3.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5fae\u4fe1\uff1abithomeAI", None))
        self.label_time_end.setText("")
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:700;\">\u300c\u9ad8\u8003\u5fd7\u613f\u300d\u4ea4\u6d41\u7fa4\uff1a</span><a href=\"https://t.zsxq.com/x8PTu\"><span style=\" font-size:10pt; font-weight:700; text-decoration: underline; color:#0078d7;\">https://t.zsxq.com/x8PTu</span></a></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7535\u8bdd\uff1a19331839916", None))
    # retranslateUi

