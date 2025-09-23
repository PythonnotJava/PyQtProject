# -*- coding: utf-8 -*-

from friends import *

class CW(QMainWindow):
    def __init__(self):
        super(CW, self).__init__()
        self.setMinimumSize(1200, 600)
        self.setWindowOpacity(0.8)
        self.setWindowIcon(QIcon('src/img/logo.ico'))
        self.setWindowTitle("CuteWriting")

        # 基础变量
        self.globalIni = operateJson()
        self.allImg = self.globalIni['theme']['bg']                         # bg
        self.originWidth = self.width()                                     # 基础宽
        self.originHeight = self.height()                                   # 基础高
        self.fontsize = self.globalIni['font']['size']                 # 字体大小
        self.fontfam = self.globalIni['font']['family']                    # 字体样式
        self._fontCol = self.globalIni['font']['color']              # 字体颜色
        self.fontCol = QColor(*self._fontCol)
        self.fontWe = self.globalIni['font']['weight']                            # 字体粗细程度
        self.fontSty = self.globalIni['font']['style']         # 字体样式

        # 编辑区
        self.textedit = TextEdit(self)
        self.tex, self.tey, self.tew, self.teh = 240, 50, 960, 500

        # 上部栏目主控件
        self.topWidget = QFrame(self)
        self.tox, self.toy, self.tow, self.toh = 240, 0, 960, 50

        # 下部栏目主控件
        self.bottomWidget = QFrame(self)
        self.bmx, self.bmy, self.bmw, self.bmh = 240, 550, 960, 50
        self.register = QPushButton(self.bottomWidget)
        self.b1x, self.b1y, self.b1w, self.b1h = 690, 0, 90, 50
        self.setting = QPushButton(self.bottomWidget)
        self.b2x, self.b2y, self.b2w, self.b2h = 780, 0, 90, 50
        self.extend = QPushButton(self.bottomWidget)
        self.b3x, self.b3y, self.b3w, self.b3h = 870, 0, 90, 50

        # 拖动工具栏
        # self.tool = self.addToolBar("File")
        # edit = QAction(QIcon("src/img/logo.ico"), "save", self)
        # self.tool.addAction(edit)

        # 普通工具栏
        self.tool1 = QToolButton(self.topWidget)
        self.t1x, self.t1y, self.t1w, self.t1h = 0, 0, 80, 50
        self.tool2 = QToolButton(self.topWidget)
        self.t2x, self.t2y, self.t2w, self.t2h = 80, 0, 80, 50
        self.tool3 = QToolButton(self.topWidget)
        self.t3x, self.t3y, self.t3w, self.t3h = 160, 0, 80, 50

        self.set_ui()

    def set_ui(self):
        # 编辑器
        self.textedit.setStyleSheet(ttqss)
        self.textFont = QFont()
        self.textFont.setPixelSize(self.fontsize)
        self.textFont.setWeight(self.fontWe)
        self.textFont.setFamily(self.fontfam)
        self.textFont.setStyle(self.fontSty)
        self.textedit.setTextColor(self.fontCol)
        self.textedit.setFont(self.textFont)

        # 右下角三个控件
        self.bottomWidget.setGeometry(QRect(self.bmx, self.bmy, self.bmw, self.bmh))
        self.bottomWidget.setStyleSheet("background-color : gold;")
        self.register.setIcon(qtawesome.icon('fa.user-circle-o', color='darkblue'))
        self.setting.setIcon(qtawesome.icon('fa.cogs', color='darkblue'))
        self.extend.setIcon(qtawesome.icon('mdi.google-circles-extended', color='darkblue'))
        self.register.setStyleSheet(qssbut)
        self.setting.setStyleSheet(qssbut)
        self.extend.setStyleSheet(qssbut)
        self.register.setToolTip('Account')
        self.setting.setToolTip('Setting(F2)')
        self.extend.setToolTip('Extend')
        self.setting.setShortcut('F2')

        # 右键菜单栏
        self.clickRightButton()

        # 普通工具栏
        self.tool1.setIcon(qtawesome.icon('ei.file-alt',color='darkblue'))
        self.tool2.setIcon(qtawesome.icon('fa5s.street-view', color='darkblue'))
        self.tool3.setIcon(qtawesome.icon('mdi.format-font', color='darkblue'))

        self.tool1.setStyleSheet(toolqss)
        self.tool2.setStyleSheet(toolqss)
        self.tool3.setStyleSheet(toolqss)
        self.tool1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tool2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tool3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tool1.setText('文件')
        self.tool2.setText('导航')
        self.tool3.setText('工具')
        self.tool1.setPopupMode(QToolButton.InstantPopup)
        # self.tool2.setPopupMode(QToolButton.InstantPopup)         # 先注释掉，期待下次更新
        self.tool3.setPopupMode(QToolButton.InstantPopup)

        # 工具栏功能1
        fileOpe = QMenu()
        explainCWMLFile = fileOpe.addAction('打开并解析CWML文件')
        explainCWMLFile.setIcon(qtawesome.icon('fa5s.lock-open', color='darkblue'))
        explainCWMLFile.triggered.connect(self.explainCWML)
        self.tool1.setMenu(fileOpe)
        explainCWMLFile.setShortcut('Ctrl+Shift+B')
        saveAS = fileOpe.addAction('保存为一般或者CWML文件')
        saveAS.triggered.connect(self.if_textchanged)
        saveAS.setShortcut('Ctrl+Shift+N')
        saveAS.setIcon(qtawesome.icon('mdi.content-save-edit', color='darkblue'))

        # 工具栏功能2
        self.tool2.clicked.connect(self.tool3Origin)

        # 工具栏功能3
        tool3menu = QMenu()
        tool3menu_menu = tool3menu.addMenu('字体设置')
        tool3menu_menu.setIcon(qtawesome.icon('fa5b.fonticons', color='darkblue'))
        t3_1 : QAction = tool3menu_menu.addAction(qtawesome.icon('mdi.format-size', color='darkblue'), "字体")
        t3_2 : QAction = tool3menu_menu.addAction(qtawesome.icon('mdi.invert-colors', color='daroblue'), "颜色")
        self.tool3.setMenu(tool3menu)
        t3_1.triggered.connect(self.t3_1_func)
        t3_2.triggered.connect(self.t3_2_func)
        t3_1.setShortcut('Ctrl+Shift+S')
        t3_2.setShortcut('Ctrl+Shift+C')

        # 底部栏功能setting
        self.setting.clicked.connect(self._setting)
    # 绘制全局背景图片
    def paintEvent(self, a0 : QPaintEvent):
        self.setAutoFillBackground(True)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), QPixmap(self.allImg))

    # 检测窗口大小改变，为了让控件适应大小，包括图标
    def resizeEvent(self, a0 : QResizeEvent):
        # 改变窗口大小后的新尺寸
        new_h, new_w = a0.size().height(), a0.size().width()
        new_change_w, new_change_h = new_w / self.originWidth, new_h / self.originHeight
        # 重置比例
        self.textedit.setGeometry(QRect(
            int(self.tex / self.originWidth * new_w),
            int(self.tey / self.originHeight * new_h),
            int(self.tew * new_change_w),
            int(self.teh * new_change_h)
        ))
        self.topWidget.setGeometry(QRect(
            int(self.tox / self.originWidth * new_w),
            int(self.toy / self.originHeight * new_h),
            int(self.tow * new_change_w),
            int(self.toh * new_change_h)
        ))
        self.bottomWidget.setGeometry(QRect(
            int(self.bmx / self.originWidth * new_w),
            int(self.bmy / self.originHeight * new_h),
            int(self.bmw * new_change_w),
            int(self.bmh * new_change_h)
        ))
        self.register.setGeometry(QRect(
            int(self.b1x * new_change_w),
            int(self.b1y / self.bmh * self.teh * new_change_h),
            int(self.b1w * new_change_w),
            int(self.b1h * new_change_h)
        ))
        self.setting.setGeometry(QRect(
            int(self.b2x * new_change_w),
            int(self.b2y / self.bmh * self.teh * new_change_h),
            int(self.b2w * new_change_w),
            int(self.b2h * new_change_h)
        ))
        self.extend.setGeometry(QRect(
            int(self.b3x * new_change_w),
            int(self.b3y / self.bmh * self.teh * new_change_h),
            int(self.b3w * new_change_w),
            int(self.b3h * new_change_h)
        ))
        self.tool1.setGeometry(QRect(
            int(self.t1x * new_change_w),
            int(self.t1y * new_change_h),
            int(self.t1w * new_change_w),
            int(self.t1h * new_change_h)
        ))
        self.tool2.setGeometry(QRect(
            int(self.t2x * new_change_w),
            int(self.t2y * new_change_h),
            int(self.t2w * new_change_w),
            int(self.t2h * new_change_h)
        ))
        self.tool3.setGeometry(QRect(
            int(self.t3x * new_change_w),
            int(self.t3y * new_change_h),
            int(self.t3w * new_change_w),
            int(self.t3h * new_change_h)
        ))

        # 图标自适应
        self.register.setIconSize(QSize(self.register.size()))
        self.setting.setIconSize(QSize(self.setting.size()))
        self.extend.setIconSize(QSize(self.extend.size()))
        self.tool1.setIconSize(QSize(self.tool1.width(), self.tool1.height()-20))
        self.tool2.setIconSize(QSize(self.tool2.width(), self.tool2.height()-20))
        self.tool3.setIconSize(QSize(self.tool3.width(), self.tool3.height()-20))

    # 右键菜单栏
    def clickRightButton(self):
        self.textedit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textedit.customContextMenuRequested.connect(self._clickRightButton)
        self.rightClick = QMenu()
        self.rightClick.setStyleSheet(menuqss)
        # 功能
        self.copy = self.rightClick.addAction('复制')
        self.select_all = self.rightClick.addAction('全选')
        self.paste = self.rightClick.addAction('粘贴')
        self.delete = self.rightClick.addAction('删除')
        self.readByPc = self.rightClick.addAction('人工读取')

        self.copy : QAction
        self.select_all : QAction
        self.paste : QAction
        self.delete : QAction
        self.readByPc : QAction
        self.copy.triggered.connect(self._copy)
        self.select_all.triggered.connect(self._select_all)
        self.paste.triggered.connect(self.__paste)
        self.delete.triggered.connect(self._delete)
        self.readByPc.triggered.connect(self._readByPc)

    def _clickRightButton(self):
        self.rightClick.move(QCursor.pos())
        self.rightClick.show()

    # 复制
    def _copy(self):
        tc = self.textedit.textCursor()
        select_text = tc.selectedText()
        __ = QApplication.clipboard()
        __.setText(select_text)

    # 全选
    def _select_all(self):
        __ = QApplication.clipboard()
        self.textedit.selectAll()

    # 粘贴
    def __paste(self):
        __ = QApplication.clipboard()
        self.textedit.setText(__.text())

    # 删除
    def _delete(self): self.textedit.setText(None)

    # 代替人工读取
    def _readByPc(self):
        self.mythread1 = MyThread(sayWord, self.textedit.toPlainText())
        self.mythread1.start()

    # 文件功能
    def t3_1_func(self):
        ffont = QFontDialog(self)
        font, ok = ffont.getFont()
        font : QFont
        if ok:
            self.textedit.setFont(font)
            self.fontfam = font.family()
            self.fontWe = font.weight()
            self.fontsize = font.pointSize()
            self.fontSty = font.style()

    def t3_2_func(self):
        ccolor = QColorDialog.getColor()
        self.textedit.setTextColor(ccolor)
        self._fontCol = ccolor.getRgb()

    # # 关闭检查
    def closeEvent(self, a0 : QCloseEvent) -> None:
        # 写入配置
        # 写入新配置--所有（包含字体、背景、透明度等等等）
        new_obj = {'font':
                       {'size': self.fontsize,
                        'family': self.fontfam,
                        'color': self._fontCol,
                        'weight': self.fontWe,
                        'style': self.fontSty
                        },
                   'theme':
                       {'bg': self.allImg}
                   }
        reloadJson(obj=new_obj)
        # 如果文本改变(这里不考虑配置改变文本不改变情况),提示保存文件
        if self.textedit.document().isModified():
            dlg = QMessageBox.information(self, 'Warning', '是否保存文件',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if dlg == QMessageBox.Yes: self.chooseSave()
            elif dlg == QMessageBox.No: a0.accept()
            elif dlg == QMessageBox.Cancel: a0.ignore()
        else: a0.accept()

    # 普通写入文件
    def writeSimple(self, fileName):
        f = open(fileName, 'w', encoding='U8')
        f.write(self.textedit.toPlainText())
        f.close()

    # 解析cwml文件
    def explainCWML(self):
        fileName, typeName = QFileDialog.getOpenFileName(self, "打开CWML文件", ".", "CWML Files (*.cwml)")
        try:
            if fileName is not None or '':
                size, family, color, weight, style, content = readInCWML(fileName)
                # content : str
                # 读取之后，把编辑器格式转换为配置，包含内容
                self.textedit.setText(content)
            else: pass
        except : pass

    # 选择性保存文件
    def chooseSave(self):
        try:
            # 写入文件
            fileName, typeName = QFileDialog.getSaveFileName(self, "保存", ".",
                                                             "CWML Files (*.cwml);;All files(*.*)")
            if fileName is not None or '':
                if fileName.endswith('cwml'):
                    saveAsObj = {'font':
                                     {'size': self.fontsize,
                                      'family': self.fontfam,
                                      'color': self._fontCol,
                                      'weight': self.fontWe,
                                      'style': self.fontSty
                                      },
                                 "content": self.textedit.document().toHtml()
                                 }
                    writeInCWML(saveAsObj, fileName)
                    print(saveAsObj)
                else: self.writeSimple(fileName)
            else: pass
        except: pass

    # 只有文本被改变，才能触发保存功能
    def if_textchanged(self):
        if self.textedit.document().isModified(): self.chooseSave()
        else: pass

    # 设面板
    def _setting(self):
        from settingDLG import FormLayout
        self.surface = FormLayout(self)
        self.surface.show()

    # tool2目前功能
    @staticmethod
    def tool3Origin(self): os.system(f'{os.getcwd()}/src/exa/next-time.html')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CW()
    ex.show()
    sys.exit(app.exec())
