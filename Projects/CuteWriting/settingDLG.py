from friends import *

class FormLayout(QDialog):
    def __init__(self, p=None):
        # if p is None: super(FormLayout, self).__init__()
        super(FormLayout, self).__init__()
        self.p = p
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        self.setWindowTitle('设置(快捷键 : F2)')
        self.setWindowIcon(qtawesome.icon('fa.cogs', color='darkblue'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setStyleSheet('background-color : 	#008B8B;')
        # 基础变量
        path = 'src/cfg/cfg.ini'
        self.__f = ConfigObj(path)
        self.globalAlpha = float(self.__f['setting']['alpha'])

        # 透明度控件
        self.labelAlpha = QLabel(self)
        self.alphaSetting = QSlider(self)
        self.alphaSetting.valueChanged.connect(self.changeAlpha)

        # 添加表单布局
        self.gridlayout1 = QFormLayout()
        self.hbox = QHBoxLayout()
        # 整个程序的灵魂,将QVBoxLayout改成QHBoxLayout可以改变hbox和vbox的布局从垂直布局到水平布局
        self.vlayout = QVBoxLayout()

        self.setUI()

    def setUI(self):
        # 透明度
        self.labelAlpha.setText(f"透明度{self.globalAlpha}")
        self.alphaSetting.setValue(int(self.globalAlpha * 100))
        self.alphaSetting.setOrientation(Qt.Horizontal)
        self.alphaSetting.setMinimum(20)
        self.alphaSetting.setMaximum(100)
        self.alphaSetting.setSingleStep(5)
        self.alphaSetting.setStyleSheet(sliderqss)
        self.alphaSetting.setToolTip('拖动改变透明度')
        self.labelAlpha.setStyleSheet(laqss)
        self.labelAlpha.setFixedSize(90, 60)
        self.alphaSetting.setFixedSize(650, 60)

        # 添加水平布局
        self.gridlayout1.addRow(self.labelAlpha, self.alphaSetting)
        self.gridlayout1.setSpacing(50)
        self.hbox.addLayout(self.gridlayout1)
        self.vlayout.addLayout(self.hbox)
        self.setLayout(self.vlayout)

    # 透明度改变
    def changeAlpha(self):
        value = self.alphaSetting.value() / 100
        self.labelAlpha.setText(f"透明度{value}")
        self.globalAlpha = value

    def closeEvent(self, e : QCloseEvent):
        if self.p is not None:
            self.__f['setting']['alpha'] = self.globalAlpha
            self.__f.write()
            self.p.setWindowOpacity(self.globalAlpha)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    qb = FormLayout()
    qb.show()
    sys.exit(app.exec_())
