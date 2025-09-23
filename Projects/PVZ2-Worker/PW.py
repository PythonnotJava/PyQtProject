import sys
import pickle
import json
from PyQt5.QtCore import QRect, Qt, QEvent
from PyQt5.QtWidgets import QPushButton, QLabel, QApplication, \
    QDialog, QFileDialog, QComboBox, QSpinBox, QLineEdit, QMessageBox, QAbstractItemView, QWhatsThis
from PyQt5.QtGui import QIcon, QPixmap, QWheelEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from getpass import getuser

class ComBoBox(QComboBox):
    def wheelEvent(self, e : QWheelEvent) : pass

class APP(QDialog):
    # data
    __file = open('src/setting.json', 'r', encoding='U8')
    data = json.load(__file)
    __file.close()

    def __init__(self):
        super(APP, self).__init__()
        self.setMinimumSize(800, 900)
        self.setMaximumSize(800, 900)

        self.path = None

        self.readFile = QLineEdit(self)
        self.openButton = QPushButton(self)
        self.diamondEdit = QSpinBox(self)
        self.goldEdit = QSpinBox(self)
        self.mintEdit = QSpinBox(self)
        self.energyEdit = QSpinBox(self)
        self.tool1 = QSpinBox(self)
        self.tool2 = QSpinBox(self)
        self.tool3 = QSpinBox(self)
        self.tool4 = QSpinBox(self)
        self.tool5 = QSpinBox(self)
        self.tool6 = QSpinBox(self)
        self.toolBox = [self.diamondEdit, self.goldEdit, self.mintEdit, self.energyEdit,
                        self.tool1, self.tool2, self.tool3, self.tool4, self.tool5, self.tool6]
        self.toolName = ['钻石', '金币', '薄荷币', '罐子透视',
                         '充电盒子', '手套', '植物种子',  '冰霜手指', '闪电手指', '弹飞手指']
        self.label1 = QLabel(self)
        self.label11 = QLabel(self)
        self.label111 = QLabel(self)
        self.label1111 = QLabel(self)
        self.label11111 = QLabel(self)
        self.label111111 = QLabel(self)
        self.label1111111 = QLabel(self)
        self.label11111111 = QLabel(self)
        self.label111111111 = QLabel(self)
        self.label1111111111 = QLabel(self)
        self.labels = [self.label1, self.label11, self.label111, self.label1111,
                       self.label11111, self.label111111, self.label1111111, self.label11111111,
                       self.label111111111, self.label1111111111]

        self.yourNameLabel = QLabel(self)
        self.yourNameEdit = QLineEdit(self)
        self.changeName = QPushButton(self)
        self.confirmName = QPushButton(self)

        # plants
        self.plantsName = ComBoBox(self)
        self.plantsLevel = QSpinBox(self)
        self.plantsPieces = QSpinBox(self)
        self.plantsMaster = QSpinBox(self)
        self.plantsPiecesLabel = QLabel(self)
        self.plantsMasterLabel = QLabel(self)
        self.plantsLevelLabel = QLabel(self)
        self.plantsNameLabel = QLabel(self)
        self.plantsLabelNmaes = ['选中植物', '植物等级', '植物碎片', '大师等级']
        self.plantsAttr = [self.plantsName, self.plantsLevel, self.plantsPieces, self.plantsMaster]
        self.plantsLabel = [self.plantsNameLabel, self.plantsLevelLabel, self.plantsPiecesLabel, self.plantsMasterLabel]

        # plants data
        with open('src/plants.dat', 'rb') as f:
            self.plants_dict : dict = pickle.load(f)
            f.close()
        self.plants_names = list(self.plants_dict.keys())

        # all plants
        self.allplants = QLabel(self)
        self.allplantsMasterLabel = QLabel(self)
        self.allplantsLevelLabel = QLabel(self)
        self.allplantsPiecesLabel = QLabel(self)
        self.allplantsm = QSpinBox(self)
        self.allplantsl = QSpinBox(self)
        self.allplantsp = QSpinBox(self)

        # 范围锁定
        self.rangeLessThan27x = [self.diamondEdit, self.goldEdit, self.mintEdit, self.energyEdit,
                                 self.tool1, self.tool2, self.tool3, self.tool4, self.tool5, self.tool6,
                                 self.plantsLevel, self.plantsPieces, self.plantsMaster,
                                 self.allplantsl, self.allplantsm, self.allplantsp]
        self.howToUse = QPushButton(self)
        self.ifYourSure = QPushButton(self)
        self.ifYourSureAll = QPushButton(self)
        self.showLabel = QLabel(self)

    def setUI(self):
        self.readFile.setDisabled(True)
        self.readFile.setGeometry(QRect(5, 10, 700, 25))
        self.readFile.setText("选中文件路径 ： ")
        self.readFile.setReadOnly(True)
        self.readFile.setContextMenuPolicy(Qt.NoContextMenu)
        self.openButton.setGeometry(QRect(715, 8, 80, 28))
        self.openButton.setText("Open")
        self.openButton.setCursor(Qt.PointingHandCursor)
        self.readFile.setCursor(Qt.ForbiddenCursor)
        self.openButton.clicked.connect(self.openYourData)
        self.yourNameLabel.setText("亲爱的玩家：")
        self.yourNameLabel.setGeometry(QRect(400, 80, 160, 50))
        self.yourNameEdit.setText('')
        self.yourNameEdit.setGeometry(QRect(570, 80, 225, 50))
        self.yourNameEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.yourNameEdit.setReadOnly(True)
        self.changeName.setGeometry(QRect(400, 140, 120, 50))
        self.confirmName.setGeometry(QRect(660, 140, 120, 50))
        self.changeName.setText("一键改名")
        self.changeName.clicked.connect(lambda : self.changeYourName(0))
        self.confirmName.setText("确定修改")
        self.confirmName.clicked.connect(lambda : self.changeYourName(1))
        self.confirmName.setEnabled(False)
        self.changeName.setCursor(Qt.PointingHandCursor)
        self.confirmName.setCursor(Qt.ForbiddenCursor)

        # 核心道具
        for i in range(len(self.labels)):
            self.labels[i].setText(self.toolName[i])
            self.labels[i].setGeometry(QRect(25, 60+i*70, 120, 50))
            self.toolBox[i].setGeometry(QRect(160, 60+70*i, 200, 55))
            self.toolBox[i].setContextMenuPolicy(Qt.NoContextMenu)
            self.toolBox[i].setCursor(Qt.PointingHandCursor)

        # 植物核心
        for i in range(len(self.plantsLabel)):
            self.plantsLabel[i].setGeometry(QRect(400, 220 + 70 * i, 120, 50))
            self.plantsLabel[i].setText(self.plantsLabelNmaes[i])
            self.plantsAttr[i].setGeometry(QRect(570, 220 + 70 * i, 220, 50))
            self.plantsAttr[i].setCursor(Qt.PointingHandCursor)

        self.plantsName.view().setVerticalScrollMode(QAbstractItemView.ScrollPerItem)

        self.plantsName.addItems(self.plants_names)
        self.plantsName.currentIndexChanged.connect(self.changePlant)

        for i in self.rangeLessThan27x:
            try:
                i.setRange(0, self.data['MAX'])
            except OverflowError:
                i.setRange(0, 2147483647)
            try:
                i.setSingleStep(self.data['step'])
            except OverflowError:
                i.setSingleStep(2147483647)

        # 一次性改完
        self.allplants.setText("一次性全部植物修改")
        self.allplants.setGeometry(QRect(400, 280 + 70 * 3, 380, 50))
        self.allplants.setStyleSheet("padding-left : 60px;")
        self.allplantsLevelLabel.setText("植物等级")
        self.allplantsPiecesLabel.setText("植物碎片")
        self.allplantsMasterLabel.setText("大师等级")
        _ = [self.allplantsLevelLabel, self.allplantsPiecesLabel, self.allplantsMasterLabel]
        __ = [self.allplantsl, self.allplantsp, self.allplantsm]
        for i in _:
            i.setGeometry(QRect(400, 550+70*_.index(i), 120, 50))
            __[_.index(i)].setGeometry(QRect(570, 550+70*_.index(i), 220, 50))

        self.ifYourSure.setText("单颗+资源修改")
        self.ifYourSureAll.setText("全部修改")
        self.howToUse.setText("使用与注意")
        self.howToUse.setCursor(Qt.PointingHandCursor)
        self.ifYourSure.setCursor(Qt.PointingHandCursor)
        self.ifYourSureAll.setCursor(Qt.PointingHandCursor)
        self.ifYourSure.setGeometry(QRect(640, 750, 150, 40))
        self.ifYourSureAll.setGeometry(QRect(640, 800, 150, 40))
        self.howToUse.setGeometry(QRect(640, 850, 150, 40))
        self.showLabel.setGeometry(QRect(25, 750, 580, 140))
        self.showLabel.setPixmap(QPixmap("src/bg.png"))
        self.showLabel.setStyleSheet('padding-left : 0;')
        self.showLabel.setScaledContents(True)
        self.howToUse.clicked.connect(self.giveUsomeHelp)
        self.ifYourSure.clicked.connect(lambda : self.confirmAllChanges(0))
        self.ifYourSureAll.clicked.connect(lambda: self.confirmAllChanges(1))

    def changeYourName(self, n : int):
        # 改名字
        if n == 0:
            self.yourNameEdit.setReadOnly(False)
            self.confirmName.setEnabled(True)
            self.changeName.setEnabled(False)
            self.confirmName.setCursor(Qt.PointingHandCursor)
            self.changeName.setCursor(Qt.ForbiddenCursor)
        elif n == 1:
            # 不允许空名字
            if self.yourNameEdit.text() == "" or None or 0 == len(self.yourNameEdit.text()):
                QMessageBox.warning(self, "Waring", "不允许空名字！")
            else: pass
            self.yourNameEdit.setReadOnly(True)
            self.confirmName.setEnabled(False)
            self.changeName.setEnabled(True)
            self.changeName.setCursor(Qt.PointingHandCursor)
            self.confirmName.setCursor(Qt.ForbiddenCursor)
        else : pass

    def event(self, event : QEvent):
        if event.type() == QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            _f = open('src/Message.html', 'r', encoding='U8')
            mes = _f.read()
            _f.close()
            mess = QMessageBox()
            mess.information(self, "Help", mes, QMessageBox.Ok)
        return QDialog.event(self, event)

    def openYourData(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "请您选取待编辑的Json文件", "C://", "Json(*.json)")
        # 表示没有读取
        if fileName == '' or fileName is None or len(fileName) == 0 : pass
        else:
            self.path = fileName
            self.readFile.setText('选中文件路径 ： ' + fileName)
            file = open(fileName, 'r', encoding='U8')
            # print(fileName)
            data = json.load(file)
            file.close()
            # 钻石
            fault_cope = 10000000
            try:
                self.number_diamond = data['objects'][0]['objdata']['g']
                self.diamondEdit.setValue(self.number_diamond)
            except:
                self.diamondEdit.setValue(fault_cope)
            # 金币
            try:
                self.number_gold = data['objects'][0]['objdata']['c']
                self.goldEdit.setValue(self.number_gold)
            except:
                self.goldEdit.setValue(fault_cope)
            # 薄荷
            try:
                self.number_mint = data['objects'][0]['objdata']['m']
                self.mintEdit.setValue(self.number_mint)
            except:
                self.mintEdit.setValue(fault_cope)
            # 名字
            try:
                self.yourName = data['objects'][0]['objdata']['n']
                self.yourNameEdit.setText(self.yourName)
            except:
                self.yourNameEdit.setText("User Dave")
            # 闪电
            try:
                self.finger1 = data['objects'][0]['objdata']['pr'][0]['i']
                self.tool5.setValue(self.finger1)
            except:
                self.tool5.setValue(fault_cope)
            # 击飞
            try:
                self.finger2 = data['objects'][0]['objdata']['pr'][1]['i']
                self.tool6.setValue(self.finger2)
            except:
                self.tool6.setValue(fault_cope)
            # 冰球
            try:
                self.finger3 = data['objects'][0]['objdata']['pr'][3]['i']
                self.tool4.setValue(self.finger3)
            except:
                self.tool4.setValue(self.finger3)
            # 盒子
            try:
                self.boxNumber = data['objects'][0]['objdata']['pf']
                self.tool1.setValue(self.boxNumber)
            except:
                self.tool1.setValue(fault_cope)
            # 手套
            try:
                self.gloves = data['objects'][0]['objdata']['t']
                self.tool2.setValue(self.gloves)
            except:
                self.tool2.setValue(fault_cope)
            # 透视
            try:
                self.perspective = data['objects'][0]['objdata']['pr'][5]['i']
                self.energyEdit.setValue(self.perspective)
            except:
                self.energyEdit.setValue(fault_cope)
            # 种子
            try:
                self.plantsseed = data['objects'][0]['objdata']['spr']
                self.tool3.setValue(self.plantsseed)
            except:
                self.tool3.setValue(fault_cope)

            # 读取之后把植物卡对应属性填充
            self.plantData : list = data['objects'][0]['objdata']['plis']
            self.curPlantCodeName = self.plants_dict[self.plantsName.currentText()]
            for each_plant in self.plantData:
                each_plant : dict
                if each_plant['p'] == self.curPlantCodeName:
                    self.plantsLevel.setValue(each_plant['l'])
                    self.plantsPieces.setValue(each_plant['x'])
                    self.plantsMaster.setValue(each_plant['m'])
                    break

    def changePlant(self):
        new_plant = self.plantsName.currentText()
        new_curPlantCodeName = self.plants_dict[new_plant]
        for each_plant in self.plantData:
            each_plant: dict
            if each_plant['p'] == new_curPlantCodeName:
                self.plantsLevel.setValue(each_plant['l'])
                self.plantsPieces.setValue(each_plant['x'])
                self.plantsMaster.setValue(each_plant['m'])
                break

    def confirmAllChanges(self, n : int):
        diamond = self.diamondEdit.value()
        gold = self.goldEdit.value()
        mint = self.mintEdit.value()
        vase = self.energyEdit.value()
        box = self.tool1.value()
        gloves = self.tool2.value()
        seed = self.tool3.value()
        frozen = self.tool4.value()
        lighting = self.tool5.value()
        fly = self.tool6.value()
        name = self.yourNameEdit.text()
        choose_a_plant = self.plantsName.currentText()
        choose_a_plantl = self.plantsLevel.value()
        choose_a_plantp = self.plantsPieces.value()
        choose_a_plantm = self.plantsMaster.value()
        all_plantsl = self.allplantsl.value()
        all_plantsm = self.allplantsm.value()
        all_plantsp = self.allplantsp.value()

        if self.path is None:
            QMessageBox.warning(self, 'Waring', "没有文件被导入!", QMessageBox.Ok)
        else:
            with open(self.path, 'r', encoding='U8') as _file:
                data : dict = json.load(_file)
                # 必须把植物添加到列表
                plants_list : list = data['objects'][0]['objdata']['p']
                _file.close()
                data['objects'][0]['objdata']['g'] = diamond
                data['objects'][0]['objdata']['c'] = gold
                data['objects'][0]['objdata']['m'] = mint
                data['objects'][0]['objdata']['n'] = name
                data['objects'][0]['objdata']['pr'][0]['i'] = lighting
                data['objects'][0]['objdata']['pr'][1]['i'] = fly
                data['objects'][0]['objdata']['pr'][3]['i'] = frozen
                data['objects'][0]['objdata']['pf'] = box
                data['objects'][0]['objdata']['t'] = gloves
                # 新手没有这一项
                try:
                    data['objects'][0]['objdata']['pr'][5]['i'] = vase
                except:pass
                data['objects'][0]['objdata']['spr'] = seed
                if n == 0:
                    for each_plant in self.plantData:
                        each_plantN = self.plantData.index(each_plant)
                        if each_plant['p'] == choose_a_plant:
                            data['objects'][0]['objdata']['plis'][each_plantN]['l'] = choose_a_plantl
                            data['objects'][0]['objdata']['plis'][each_plantN]['m'] = choose_a_plantm
                            data['objects'][0]['objdata']['plis'][each_plantN]['x'] = choose_a_plantp
                            plants_list.append(each_plantN)
                            plants_list = list(set(plants_list))
                            data['objects'][0]['objdata']['p'] = plants_list
                            break
                elif n == 1:
                    for each_plant in self.plantData:
                        each_plantN = self.plantData.index(each_plant)
                        plants_list.append(each_plantN)
                        plants_list = list(set(plants_list))
                        data['objects'][0]['objdata']['plis'][each_plantN]['l'] = all_plantsl
                        data['objects'][0]['objdata']['plis'][each_plantN]['m'] = all_plantsm
                        data['objects'][0]['objdata']['plis'][each_plantN]['x'] = all_plantsp
                    data['objects'][0]['objdata']['p'] = plants_list
                else:
                    pass
                print(data)
                filePath, fileType = QFileDialog.getSaveFileName(self, "保存Json数据", 'C://', 'Json(*.json)')
                # 没保存
                if filePath == '' or None or len(filePath) == 0:
                    pass
                else:
                    with open(filePath, 'w', encoding='U8') as file:
                        json.dump(data, file)

    def giveUsomeHelp(self):
        self.webview = QWebEngineView()
        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.setHtml(open('src/readme.html', 'r', encoding='U8').read())
        self.webview.setGeometry(QRect(500, 100, 600, 800))
        self.webview.setAttribute(Qt.WA_DeleteOnClose)
        QApplication.beep()
        self.webview.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("src/logo.ico"))
    app.setApplicationName("PVZ2-Worker")
    __file1 = open('src/main.qss', 'r', encoding='U8')
    ui = APP()
    ui.setStyleSheet(__file1.read())
    __file1.close()
    ui.setUI()
    ui.show()
    if ui.data['if1'] == 0:
        ui.giveUsomeHelp()
        ui.data['if1'] += 1
        user = getuser()
        ui.data['theme']['pc'] = user
        with open('src/setting.json', 'w', encoding='U8') as fd:
            json.dump(ui.data, fd)
    else:
        if ui.data['theme']['pc'] != getuser() : sys.exit()
        else : pass
    sys.exit(app.exec())

