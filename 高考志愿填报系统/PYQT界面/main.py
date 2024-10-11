#【在指定虚拟环境下执行以减少冗余的文件包的干扰（需要在把原来环境当中的pyinstaller卸载后在新的环境当中重新安装）】这里的虚拟环境指的是纯python的虚拟环境不是conda的虚拟环境
# cd C:\Users\13480\gitee\trade\高考志愿填报系统\PYQT界面

#删除环境
# conda env remove -n my_env
#新建环境
# conda create -n my_env python=3.9

#【打包命令说明】尽量用原始的python虚拟环境，不要用conda的虚拟环境，conda的虚拟环境自带太多包了
# conda激活环境之后先pip install pipenv
# 之后cd进项目文件夹#cd C:\Users\13480\gitee\trade\高考志愿填报系统\PYQT界面
# 运行pipenv install#说明pipenv install会自动读取requirements
# 完成后运行pipenv shell
# 之后安装pyinstaller和其他所需要的包，然后就是正常的打包流程了

# pip install pyinstaller
# pip install requests PySide6

# -D 打包成一个带各种运行所需文件的文件夹，其中包括可执行文件
# -F 打包成一个独立的可执行文件
# -w 打包完后运行可执行文件不会弹出命令行窗口
# pyinstaller -F -w -i images/music.ico -n gaokao main.py#这个就是直接用exe文件就行
# pyinstaller -D -w -i images/music.ico -n gaokao main.py#这个后面要合成zip文件

# 更新版本之后删除原来的文件
# Python可以删除自身文件，但打包成.exe文件之后exe本身在执行时文件是被占用的状态无法删除自身，因而需要额外的bat文件参与
import sys
import os
from subprocess import Popen as subprocessPopen
def WriteRestartCmd():
    b=open("upgrade.bat",'w')
    TempList="@echo off\n";# 关闭bat脚本的输出
    TempList+="ping -n 5 127.0.0.1>nul \n"# 有的电脑没有sleep命令，因而使用ping替代，ping一次默认一秒左右
    TempList+="del "+os.path.realpath(sys.argv[0])+"\n"# 删除当前文件【sys.argv[0]获取文件路径，在exe文件当中更加准确】
    TempList+="ping -n 10 127.0.0.1>nul \n"# 有的电脑没有sleep命令，因而使用ping替代，ping一次默认一秒左右
    b.write(TempList)
    b.close()
    subprocessPopen("upgrade.bat")# 执行版本升级命令
    sys.exit()# 退出此程序
from pandas import DataFrame as pdDataFrame#pandas占地过大，使用from单独引用部分模块
from json import dumps as jsondumps
from json import load as jsonload
from webbrowser import open as webopen
from requests import get as requestget
from PySide6.QtWidgets import QApplication,QLineEdit,QDialog,QGraphicsDropShadowEffect,QMessageBox,QMainWindow,QVBoxLayout,QLabel,QDialogButtonBox
from PySide6.QtCore import QCoreApplication, Qt, QPoint
from PySide6.QtGui import QFontDatabase
# pip install requests PySide6
from mainwindow_ui import Ui_MainWindow
# self.horizontalLayout_body.addWidget(self.widget_info, 0, Qt.AlignmentFlag.Qt.AlignmentFlag.AlignVCenter)
# 换成下面这行【文件才能执行下去】不然报错qt里面没有这个文件
# self.horizontalLayout_body.addWidget(self.widget_info, 0, Qt.AlignVCenter)

# #【ui文件转py】
# pyside6-uic input.ui -o output.py
# #【qrc文件转py】
# pyside6-rcc C:\Users\13480\gitee\trade\高考志愿填报系统\PYQT界面\resource.qrc -o output.py

NOW_VERSION = '2025'#版本号需要单独设置【不需要单独的文件，每次弄新的版本的时候都要修改】

#生成弹窗界面
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('请输入账户密码')
        self.accountLineEdit = QLineEdit(self)
        self.accountLineEdit.setPlaceholderText('账户')
        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setPlaceholderText('密码')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(QLabel('账户:', self))
        layout.addWidget(self.accountLineEdit)
        layout.addWidget(QLabel('密码:', self))
        layout.addWidget(self.passwordLineEdit)

        # 创建按钮
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # 连接按钮的信号到槽
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)

        self.setLayout(layout)
    def get_account(self):
        return self.accountLineEdit.text()
    def get_password(self):
        return self.passwordLineEdit.text()


class PlayerWindow(QMainWindow):
    '主窗体类'
    def __init__(self):
        # 继承父类
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)#自动更新

        #初始化软件使用次数
        self.trytime=0

        # 载入字体
        font_path = ':/fonts/fonts/LXGWWenKai-Regular.ttf'
        fid = QFontDatabase.addApplicationFont(font_path)
        families = QFontDatabase.applicationFontFamilies(fid)
        print(f'载入字体：{families}')

        # 窗口相关
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)  # 设置为无标题栏
        self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.ui.pushButton_update.setText(NOW_VERSION) # 设定版本号

        # 控件阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)  # 阴影效果
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(10)  # 阴影半径
        self.effect_shadow.setColor(Qt.black)  # 阴影颜色
        self.ui.widget.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口

        self.effect_shadow = QGraphicsDropShadowEffect(self)  # 阴影效果
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(10)  # 阴影半径
        self.effect_shadow.setColor(Qt.black)  # 阴影颜色

        # 事件过滤器
        self.installEventFilter(self)

        # 鼠标响应
        self.setMouseTracking(True)
        self.ui.centralwidget.setMouseTracking(True)
        self.ui.widget.setMouseTracking(True)
        self.ui.widget_bottom.setMouseTracking(True)

        # 窗口变量初始化【关键因素不可更改】
        self.move_drag = False
        self.move_DragPosition = 0
        self.right_bottom_corner_drag = False
        self.left_bottom_corner_drag = False
        self.left_drag = False
        self.right_drag = False
        self.bottom_drag = False
        self.left_rect = []
        self.right_rect = []
        self.bottom_rect = []
        self.right_bottom_corner_rect = []
        self.left_bottom_corner_rect = []

        # 按键绑定
        self.ui.pushButton_red.clicked.connect(self.close_window)
        self.ui.pushButton_green.clicked.connect(self.showMinimized)
        self.ui.pushButton_yellow.clicked.connect(self.maximize_window)
        self.ui.pushButton_update.clicked.connect(self.get_update)

        self.ui.pushButton.clicked.connect(self.mbit)#mbit职业性格测试按钮
        self.ui.pushButton_2.clicked.connect(self.zytb)#志愿填报按钮

        # 参数设置
        self.lrc_trans_mode = 1  # 歌词翻译模式
        self.lrc_time_list = []  # 歌词时间戳列表
        self.is_window_maximized = False  # 窗口最大化状态

        # 自动换行
        self.ui.label_name.setWordWrap(True)#中间部分（原歌词上方）自动换行滚动条
        self.ui.listWidget_3.setWordWrap(True)#联系方式位置的自动换行

        # 气泡提示
        self.ui.pushButton_red.setToolTip('关闭')
        self.ui.pushButton_yellow.setToolTip('最大化')
        self.ui.pushButton_green.setToolTip('最小化')

    def mbit(self):
        thisbool=self.get_update()
        if thisbool:
            print("验证软件版本完毕")
            '提交职业性格测试'
            # id,title_id,title,question,type
            # 2,2,下列哪一种是你的一般生活取向?,只管做吧。,S
            # 3,2,下列哪一种是你的一般生活取向?,找出多种不同选择。,N
            # 4,3,你喜欢自己的哪种性格？,冷静而理性。,T
            # 5,3,你喜欢自己的哪种性格？,热情而体谅。,F
            # 6,4,你擅长,在有需要时间时同时协调进行多项工作。,J
            # 7,4,你擅长,专注在某一项工作上，直至把它完成为止。,P
            # 8,5,你参与社交聚会时,总是能认识新朋友。,E
            # 9,5,你参与社交聚会时,只跟几个亲密挚友呆在一起。,I
            # 10,6,当你尝试了解某些事情时，一般你会,先要了解细节。,S
            # 11,6,当你尝试了解某些事情时，一般你会,先了解整体情况，细节容后再谈。,N
            # 12,7,你对下列哪方面较感兴趣？,知道别人的想法。,T
            # 13,7,你对下列哪方面较感兴趣？,知道别人的感受。,F
            alllist=["S","N","T","F",
                    "J","P","E","I",
                    "S","N","T","F"]#INFJ\ISFJ\ENTJ,SN\TF\JP\EI互斥
            allvalues={"S":0,"N":0,"T":0,"F":0,"J":0,"P":0,"E":0,"I":0}
            for n in range(1,13):
                print(n)
                thisbox=getattr(self.ui, f'checkBox_{n}', None)
                # print(thisbox)#判断是哪一个复选框
                thisvalue=thisbox.isChecked()#判断是否选中
                if thisvalue:#thisbox.isChecked()选中了之后返回值为True才执行下面的任务
                    print("thisvalue",thisvalue)
                    allvalues[alllist[n-1]]+=1
            print(allvalues)
            ##生成最终的ENTJ信息
            self.mbitvalues=""
            if allvalues["E"]>=allvalues["I"]:
                self.mbitvalues+="E"
            else:
                self.mbitvalues+="I"
            if allvalues["S"]>=allvalues["N"]:
                self.mbitvalues+="S"
            else:
                self.mbitvalues+="N"
            if allvalues["F"]>=allvalues["T"]:
                self.mbitvalues+="F"
            else:
                self.mbitvalues+="T"
            if allvalues["P"]>=allvalues["J"]:
                self.mbitvalues+="P"
            else:
                self.mbitvalues+="J"
            if self.mbitvalues=="ISTJ":
                mes="""【人格】ISTJ,内倾感觉思维判断,\n
    1.严肃、安静、藉由集中心 志与全力投入、及可被信赖获致成功。\n
    2.行事务实、有序、实际 、 逻辑、真实及可信赖。\n
    3.十分留意且乐于任何事（工作、居家、生活均有良好组织及有序。\n
    4.负责任。\n
    5.照设定成效来作出决策且不畏阻挠与闲言会坚定为之。\n
    6.重视传统与忠诚。\n
    7.传统性的思考者或经理。,\n
    【专业】ISTJ（“物流师” 人格）：会计学；计算机科学\n
                    """
            elif self.mbitvalues=="ISFJ":
                mes="""【专业】ISFJ,内倾感觉情感判断,\n
    1.安静、和善、负责任且有良心。\n
    2.行事尽责投入。\n
    3.安定性高，常居项目工作或团体之安定力量。\n
    4.愿投入、吃苦及力求精确。\n
    5.兴趣通常不在于科技方面。对细节事务有耐心。\n
    6.忠诚、考虑周到、知性且会关切他人感受\n
    7.致力于创构有序及和谐的工作与家庭环境。,\n
    【专业】ISFJ（“守卫者” 人格）：医学、教育学、社会学；建筑学、工程类\n
                    """
            elif self.mbitvalues=="INFJ":
                mes="""【人格】INFJ,内倾直觉情感判断,"\n
    1.因为坚忍、创意及必须达成的意图而能成功。\n
    2.会在工作中投注最大的努力。\n
    3.默默强力的、诚挚的及用心的关切他人。\n
    4.因坚守原则而受敬重。\n
    5.提出造福大众利益的明确远景而为人所尊敬与追随。\n
    6.追求创见、关系及物质财物的意义及关联。\n
    7.想了解什么能激励别人及对他人具洞察力。\n
    8.光明正大且坚信其价值观。\n
    9.有组织且果断地履行其愿景。,\n
    【专业】INFJ（“提倡者” 人格）：语言、文学、教育学；心理学\n
                    """
            elif self.mbitvalues=="INTJ":
                mes="""【人格】INTJ,内倾直觉思维判断,\n
    1.具强大动力与本意来达成目的与创意—固执顽固者。\n
    2.有宏大的愿景且能快速在众多外界事件中找出有意义的模范。\n
    3.对所承负职务，具良好能力于策划工作并完成。\n
    4.具怀疑心、挑剔性、独立性、果决，对专业水准及绩效要求高。,\n
    【专业】INTJ（“建筑师” 人格）：管理学、工商管理、人力资源管理\n
                    """
            elif self.mbitvalues=="ISTP":
                mes="""【人格】ISTP,内倾感觉思维知觉,\n
    1.冷静旁观者—安静、预留余地、弹性及会以无偏见的好奇心与未预期原始的幽默观察与分析。\n
    2.有兴趣于探索原因及效果，技术事件是为何及如何运作且使用逻辑的原理组构事实、重视效能。\n
    3.擅长于掌握问题核心及找出解决方式。\n
    4.分析成事的缘由且能实时由大量资料中找出实际问题的核心。,\n
    【专业】ISTP（“鉴赏家” 人格）：机械工程\n
                    """
            elif self.mbitvalues=="ISFP":
                mes="""【人格】ISFP,内倾感觉情感知觉,\n
    1.羞怯的、安宁和善地、敏感的、亲切的、且行事谦虚。\n
    2.喜于避开争论，不对他人强加已见或价值观。\n
    3.无意于领导却常是忠诚的追随者。\n
    4.办事不急躁，安于现状无意于以过度的急切或努力破坏现况，且非成果导向。\n
    5.喜欢有自有的空间及照自订的时程办事。,\n
    【专业】ISFP（“探险家” 人格）：舞蹈表演、流行音乐；室内设计、园林规划\n
                    """
            elif self.mbitvalues=="INFP":
                mes="""【人格】INFP,内倾感觉情感知觉,\n
    1.羞怯的、安宁和善地、敏感的、亲切的、且行事谦虚。\n
    2.喜于避开争论，不对他人强加已见或价值观。\n
    3.无意于领导却常是忠诚的追随者。\n
    4.办事不急躁，安于现状无意于以过度的急切或努力破坏现况，且非成果导向。\n
    5.喜欢有自有的空间及照自订的时程办事。,\n
    【专业】INFP（“调停者”人格）：医学、心理学；哲学、艺术史论、音乐学\n
                    """
            elif self.mbitvalues=="INTP":
                mes="""【人格】INTP,内倾直觉思维知觉,\n
    1.安静、自持、弹性及具适应力。\n
    2.特别喜爱追求理论与科学事理。\n
    3.习于以逻辑及分析来解决问题—问题解决者。\n
    4.最有兴趣于创意事务及特定工作，对聚会与闲聊无 大兴趣。\n
    5.追求可发挥个人强烈兴趣的生涯。\n
    6.追求发展对有兴趣事务之逻辑解释。,\n
    【专业】INTP（“逻辑学家” 人格）：金融学、财政学、计算机网络技术\n
                    """
            elif self.mbitvalues=="ESTP":
                mes="""【人格】ESTP,外倾感觉思维知觉,\n
    1.擅长现场实时解决问题—解决问题者。\n
    2.喜欢办事并乐于其中及过程。\n
    3.倾向于喜好技术事务及运动，交结同好友人。\n
    4.具适应性、容忍度、务实性；投注心力于会很快具 成效工作。\n
    5.不喜欢冗长概念的解释及理论。\n
    6.最专精于可操作、处理、分解或组合的真实事务。,\n
    【专业】ESTP（“企业家” 人格）：数据分析相关\n
                    """
            elif self.mbitvalues=="ESFP":
                mes="""【人格】ESFP,外倾感觉情感知觉,\n
    1.外向、和善、接受性、乐于分享喜乐予他人。\n
    2.喜欢与他人一起行动且促成事件发生，在学习时亦然。\n
    3.知晓事件未来的发展并会热列参与。\n
    5.最擅长于人际相处能力及具备完备常识，很有弹性能立即 适应他人与环境。\n
    6.对生命、人、物质享受的热爱者。,\n
    【专业】ESFP（“表演者” 人格）：新闻学、广告学\n
    """
            elif self.mbitvalues=="ENFP":
                mes="""【人格】ENFP,外倾直觉情感知觉,\n
    1.充满热忱、活力充沛、聪明的、富想象力的，视生命充满机会但期能得自他人肯定与支持。\n
    2.几乎能达成所有有兴趣的事。\n
    3.对难题很快就有对策并能对有困难的人施予援手。\n
    4.依赖能改善的能力而无须预作规划准备。\n
    5.为达目的常能找出强制自己为之的理由。\n
    6.即兴执行者。,\n
    【专业】ENFP（“竞选者” 人格）：人力资源管理、国际经济与贸易；社会学\n
    """
            elif self.mbitvalues=="ENTP":
                mes="""【人格】ENTP,外倾直觉思维知觉,\n
    1.反应快、聪明、长于多样事务。\n
    2.具激励伙伴、敏捷及直言讳专长。\n
    3.会为了有趣对问题的两面加予争辩。\n
    4.对解决新及挑战性的问题富有策略，但会轻忽或厌烦经常的任务与细节。\n
    5.兴趣多元，易倾向于转移至新生的兴趣。\n
    6.对所想要的会有技巧地找出逻辑的理由。\n
    7.长于看清础他人，有智能去解决新或有挑战的问题,\n
    【专业】ENTP（“辩论家” 人格）：工商管理、经济学、金融学；国际政治\n
    """
            elif self.mbitvalues=="ESTJ":
                mes="""【人格】ESTJ,外倾感觉思维判断,\n
    1.务实、真实、事实倾向，具企业或技术天份。\n
    2.不喜欢抽象理论；最喜欢学习可立即运用事理。\n
    3.喜好组织与管理活动且专注以最有效率方式行事以达致成效。\n
    4.具决断力、关注细节且很快作出决策—优秀行政者。\n
    5.会忽略他人感受。\n
    6.喜作领导者或企业主管。\n
    7.做事风格比较偏向于权威指挥性。,\n
    【专业】ESTJ（“总经理” 人格）：物业管理、工商管理\n
    """
            elif self.mbitvalues=="ESFJ":
                mes="""【人格】ESFJ,内倾感觉思维判断,\n
    1.诚挚、爱说话、合作性高、受 欢迎、光明正大 的—天生的 合作者及活跃的组织成员。\n
    2.重和谐且长于创造和谐。\n
    3.常作对他人有益事务。\n
    4.给予鼓励及称许会有更佳工作成效。\n
    5.最有兴趣于会直接及有形影响人们生活的事务。\n
    6.喜欢与他人共事去精确且准时地完成工作。,\n
    【专业】ESFJ（“执政官” 人格）：社会学；旅游管理\n
    """
            elif self.mbitvalues=="ENFJ":
                mes="""【人格】ENFJ,外倾直觉情感判断,\n
    1.热忱、易感应及负责任的--具能鼓励他人的领导风格。\n
    2.对别人所想或希求会表达真正关切且切实用心去处理。\n
    3.能怡然且技巧性地带领团体讨论或演示文稿提案。\n
    4.爱交际、受欢迎及富同情心。\n
    5.对称许及批评很在意。\n
    6.喜欢带引别人且能使别人或团体发挥潜能。,\n
    【专业】ENFJ（“主人公” 人格）：管理学、市场营销、经济学；法学\n
    """
            elif self.mbitvalues=="ENTJ":
                mes="""【人格】ENTJ,外倾直觉思维判断,\n
    1.坦诚、具决策力的活动领导者。\n
    2.长于发展与实施广泛的系统以解决组织的问题。\n
    3.专精于具内涵与智能的谈话如对公众演讲。\n
    4.乐于经常吸收新知且能广开信息管道。\n
    5.易生过度自信，会强于表达自已创见。\n
    6.喜于长程策划及目标设定,\n
    【专业】ENTJ（“指挥官” 人格）：播音与主持艺术、戏剧学、工程管理\n
    """
            # 获取1-12号复选框的信息，确定self.mbitvalues的值为后续选专业做准备
            self.ui.textBrowser.append(mes)
            # 专业信息
            zhuanye=requestget("https://gitee.com/bithomeAI/exe/raw/master/zhuanye.json").json()
            print("zhuanye",zhuanye)
            self.ui.textBrowser_2.append(f"""文科专业:{zhuanye["文科"]["0"]}\n
理科专业:{zhuanye["理科"]["0"]}""")
        else:
            print("版本错误不执行任何操作")

    def zytb(self):
        thisbool=self.get_update()
        if thisbool:
            print("验证软件版本完毕")
            data= requestget("https://gitee.com/bithomeAI/exe/raw/master/zytb.json").json()
            #院校信息
            datadf=pdDataFrame(data)#读出来的csv会把true变成1，尽量少用布尔值，这里用字符串"True"还是不管用
            print(datadf)
            #所在省份【先获取索引再获取内容】值为字符串
            comboBox_7value=self.ui.comboBox_7.itemText(self.ui.comboBox_7.currentIndex())
            print(comboBox_7value,type(comboBox_7value))
            #文科理科【先获取索引再获取内容】值为字符串
            comboBox_8value=self.ui.comboBox_8.itemText(self.ui.comboBox_8.currentIndex())
            print(comboBox_8value,type(comboBox_8value))
            #考试排名选项框
            spinBoxvalue=self.ui.spinBox.value()
            print(spinBoxvalue,type(spinBoxvalue))#int类型
            thisdf=datadf.copy()
            if comboBox_7value=="河北":
                pass
            else:
                # 创建一个警示弹窗
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)  # 设置图标为警告
                msg_box.setText('请选择必选项【所在省份】为【河北】')  # 设置文本
                msg_box.setWindowTitle("警示")  # 设置窗口标题
                msg_box.setStandardButtons(QMessageBox.Ok)  # 设置按钮
                msg_box.exec_() # 显示弹窗
                print('请选择必选项【所在省份】为【河北】')
            if comboBox_8value=="历史":
                thisdf=thisdf[thisdf["录取批次"].str.contains("文科")]
            elif comboBox_8value=="物理":
                thisdf=thisdf[thisdf["录取批次"].str.contains("理科")]
            else:
                # 创建一个警示弹窗
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)  # 设置图标为警告
                msg_box.setText('请选择必选项【首选科目】')  # 设置文本
                msg_box.setWindowTitle("警示")  # 设置窗口标题
                msg_box.setStandardButtons(QMessageBox.Ok)  # 设置按钮
                msg_box.exec_() # 显示弹窗
                print('请选择必选项【首选科目】')
            if (comboBox_7value!="所在省份（必选项）")and(comboBox_8value!="首选科目（必选项）"):
                print("已经选择了【所在省份】和【首选科目】，执行任务")
                #只选择投档名次在实际名称+-10000名左右的
                print("thisdf",thisdf)
                if comboBox_8value=="历史":
                    thisdf=thisdf[thisdf["录取批次"].str.contains("文科")]#只要相同首选科目的志愿
                    print(thisdf)
                    thisdf["投档名次"]=thisdf["历史累计人数"]
                elif comboBox_8value=="物理":
                    thisdf=thisdf[thisdf["录取批次"].str.contains("理科")]#只要相同首选科目的志愿
                    print(thisdf)
                    thisdf["投档名次"]=thisdf["物理累计人数"]
                thisdf=thisdf[(thisdf["投档名次"]>=0.9*spinBoxvalue-20000)&(thisdf["投档名次"]<=1.1*spinBoxvalue+20000)]
                thisdf=thisdf.sort_values(by="投档名次",ascending=True)#升序排列
                thisdf.to_csv("./建议填报院校.csv")#【这个路径看看是否正确】
        else:
            print("版本错误不执行任何操作")
    
    # 版本更新事件【需要重写】
    def get_update(self):# '获取版本更新'
        has_last_latest_version=False#初始化版本变量
        try:
            response = requestget("https://gitee.com/bithomeAI/exe/raw/master/version.txt")
            res = response.json()
            # {"version":"2025","users":{"hanyafei":{"20251001":"10"}}}
            print("res",res)
            latest_version = float(res["version"])
            print("latest_version",latest_version)
            if float(NOW_VERSION) >= float(latest_version):
                print("已经更新到最新版本")
                try:
                    with open('./user.json','r') as json_file:
                        thisuser=jsonload(json_file)
                    thisadmin = thisuser["admin"]
                    thispassword = thisuser["password"]
                    print(f'账户: {thisadmin,type(thisadmin)}, 密码: {thispassword,type(thispassword)}')#字符串
                except Exception as e:
                    #生成账号、密码登录弹窗
                    dialog = LoginDialog()
                    if dialog.exec_():
                        thisadmin = dialog.get_account()
                        thispassword = dialog.get_password()
                        print(f'账户: {thisadmin,type(thisadmin)}, 密码: {thispassword,type(thispassword)}')#字符串
                    # print("输出错误类型",e)#输出错误类型
                    thisjson=jsondumps({"admin": str(thisadmin),"password": str(thispassword)})
                    with open('./user.json','w') as json_file:
                        json_file.write(thisjson)
                if (thisadmin!="version")and(
                    thisadmin in res["users"])and(
                    thispassword in res["users"][thisadmin]):
                    print("账号密码对应")
                    self.trytime+=1
                    print("当前账号的总使用次数",res["users"][thisadmin][thispassword])
                    if self.trytime>=float(res["users"][thisadmin][thispassword]):
                        # 新程序启动时，删除旧程序制造的脚本
                        QMessageBox.critical(self,"错误","额度用完，软件自动卸载",QMessageBox.StandardButton.Ok)
                        if os.path.isfile("upgrade.bat"):
                            os.remove("upgrade.bat")
                        WriteRestartCmd()#删除当前运行的文件
                    else:
                        has_last_latest_version=True
                else:
                    QMessageBox.critical(self,"错误","密码错误重新输入",QMessageBox.StandardButton.Ok)
                    #生成账号、密码登录弹窗
                    dialog = LoginDialog()
                    if dialog.exec_():
                        thisadmin = dialog.get_account()
                        thispassword = dialog.get_password()
                        print(f'账户: {thisadmin,type(thisadmin)}, 密码: {thispassword,type(thispassword)}')#字符串
                    # print("输出错误类型",e)#输出错误类型
                    thisjson=jsondumps({"admin": str(thisadmin),"password": str(thispassword)})
                    with open('./user.json','w') as json_file:
                        json_file.write(thisjson)
            else:
                str_update = f"""
                            发现新版本！{float(NOW_VERSION)} --> {float(latest_version)}\n
                            点击 Ok 下载最新版本
                            """
                message = QMessageBox.question(
                    self, "检查更新", str_update,
                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                if message == QMessageBox.StandardButton.Ok:
                    #最新版本下载链接【这里不对需要下载exe文件】
                    latest_version_download_url="https://gitee.com/bithomeAI/exe/releases/download/2025/gaokao.exe"
                    webopen(latest_version_download_url, new=0, autoraise=True)

                # 新程序启动时，删除旧程序制造的脚本
                QMessageBox.critical(self,"错误","发现新版本，软件自动卸载",QMessageBox.StandardButton.Ok)
                if os.path.isfile("upgrade.bat"):
                    os.remove("upgrade.bat")
                WriteRestartCmd()#删除当前运行的文件
        except Exception as e:
            str_update = '获取失败！请检查网络连接'
            print(str_update)
            QMessageBox.critical(self, "错误", str_update, QMessageBox.StandardButton.Ok)
        return has_last_latest_version#返回版本是否正确的结果

    #窗口关闭
    def close_window(self):
        '关闭按钮'
        # 自动保存配置
        QCoreApplication.quit()

    #最大化最小化
    def maximize_window(self):
        '窗口最大化切换'
        if self.is_window_maximized:
            self.showNormal()
            self.is_window_maximized = False
        else:
            self.showMaximized()
            self.is_window_maximized = True

    # 窗口大小调整事件
    def resizeEvent(self, resize_event):
        '自定义窗口调整大小事件'
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self.left_rect = [QPoint(x, y) for x in range(0, 5)
                          for y in range(5, self.height() - 5)]
        self.right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 1)
                           for y in range(5, self.height() - 5)]
        self.bottom_rect = [QPoint(x, y) for x in range(5, self.width() - 5)
                            for y in range(self.height() - 5, self.height() + 1)]
        self.right_bottom_corner_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 1)
                                         for y in range(self.height() - 5, self.height() + 1)]
        self.left_bottom_corner_rect = [QPoint(x, y) for x in range(0, 5)
                                        for y in range(self.height() - 5, self.height() + 1)]
    
    # 鼠标事件
    def mouseMoveEvent(self, mouse_event):
        '重写函数，实现拖动'
        # 判断鼠标位置切换鼠标手势
        if mouse_event.position().toPoint() in self.right_bottom_corner_rect:
            self.setCursor(Qt.SizeFDiagCursor)
        elif mouse_event.position().toPoint() in self.left_bottom_corner_rect:
            self.setCursor(Qt.SizeBDiagCursor)
        elif mouse_event.position().toPoint() in self.bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif mouse_event.position().toPoint() in self.right_rect:
            self.setCursor(Qt.SizeHorCursor)
        elif mouse_event.position().toPoint() in self.left_rect:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整（+5 或 -5 匹配margin）
        if Qt.LeftButton and self.right_drag:
            # 右侧调整窗口宽度
            self.resize(mouse_event.position().toPoint().x() + 5, self.height())
            mouse_event.accept()
        elif Qt.LeftButton and self.left_drag:
            # 左侧调整窗口高度
            self.resize(self.width() - mouse_event.position().toPoint().x() + 5, self.height())
            self.move(self.x() + mouse_event.position().toPoint().x() - 5, self.y())
            mouse_event.accept()
        elif Qt.LeftButton and self.bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), mouse_event.position().toPoint().y() + 5)
            mouse_event.accept()
        elif Qt.LeftButton and self.right_bottom_corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(mouse_event.position().toPoint().x() + 5, mouse_event.position().toPoint().y() + 5)
            mouse_event.accept()
        elif Qt.LeftButton and self.left_bottom_corner_drag:
            # 左下角同时调整高度和宽度
            self.resize(self.width() - mouse_event.position().toPoint().x() + 5,
                        mouse_event.position().toPoint().y() + 5)
            self.move(self.x() + mouse_event.position().toPoint().x() - 5, self.y())
            mouse_event.accept()
        elif Qt.LeftButton and self.move_drag:
            # 标题栏拖放窗口位置
            self.move(mouse_event.globalPosition().toPoint() - self.move_DragPosition)
            mouse_event.accept()

    # 鼠标点击事件
    def mousePressEvent(self, event):
        '重写鼠标点击的事件'
        if (event.button() == Qt.LeftButton) and (event.position().toPoint().y() < self.ui.widget_top.height() + 5):
            # 鼠标左键点击标题栏区域
            self.move_drag = True
            self.move_DragPosition = event.globalPosition().toPoint() - self.pos()
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.position().toPoint() in self.right_bottom_corner_rect):
            # 鼠标左键点击右下角边界区域
            self.right_bottom_corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.position().toPoint() in self.left_bottom_corner_rect):
            # 鼠标左键点击左下角边界区域
            self.left_bottom_corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.position().toPoint() in self.left_rect):
            # 鼠标左键点击左侧边界区域
            self.left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.position().toPoint() in self.right_rect):
            # 鼠标左键点击右侧边界区域
            self.right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.position().toPoint() in self.bottom_rect):
            # 鼠标左键点击下侧边界区域
            self.bottom_drag = True
            event.accept()

    #鼠标双击事件【在标题栏上双击实现窗口最大化最小化】
    def mouseDoubleClickEvent(self, event):
        '重写鼠标双击事件'
        if (event.button() == Qt.LeftButton) and (event.y() < self.ui.widget_top.height() + 5):
            # 鼠标左键点击标题栏区域
            self.maximize_window()

    #鼠标释放事件
    def mouseReleaseEvent(self, mouse_event):
        '鼠标释放后，各扳机复位'
        self.move_drag = False
        self.right_bottom_corner_drag = False
        self.bottom_drag = False
        self.right_drag = False
        self.left_drag = False
        self.left_bottom_corner_drag = False

    #按键响应事件
    def keyPressEvent(self, event):
        '按键响应事件'
        # print("按下：" + str(event.key()))
        if event.key() == Qt.Key_Escape:#esc键退出软件
            self.close_window()
        elif (event.key() == Qt.Key_Enter) or (event.key() == Qt.Key_Return):
            self.get_update()#回车键触发版本更新

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 声明应用程序
    player_window = PlayerWindow()  # 声明窗口
    player_window.show()
    sys.exit(app.exec())  # 当点击窗口的x时，退出程序
