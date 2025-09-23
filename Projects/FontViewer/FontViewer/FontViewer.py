import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextDocument, QFont, QColor, QFontDatabase, QTextCharFormat, QIcon, QContextMenuEvent
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLabel, QSplitter,
                             QHBoxLayout, QVBoxLayout, QTextEdit, QTextBrowser,
                             QMenu, QAction, QPushButton, QMenuBar, QDockWidget,
                             QApplication, QFileDialog, QSpinBox, QColorDialog)

from readfont import extract_font_properties
from BlockScene import BlockViewer
from states import StateVarious

class CustomTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, _): pass

class RenewableTextEdit(QTextEdit):
    def __init__(self, browser: QTextBrowser, highlight='#ffff00'):
        super().__init__()
        self.default_place = ''.join([chr(i) for i in range(128)]) + "\n这是一句中文测试！"
        self.setPlaceholderText(self.default_place)
        self.browser = browser
        self.highlight = highlight

        self.setBaseUI()

    def setBaseUI(self):
        self.browser.setPlaceholderText(self.default_place)
        self.toggle_model(True)

    def toggle_model(self, use_md=True):
        if use_md:
            self.textChanged.connect(lambda: self.browser.setMarkdown(
                self.toMarkdown(QTextDocument.MarkdownFeature.MarkdownDialectGitHub)))
            self.browser.setMarkdown(self.toMarkdown(QTextDocument.MarkdownFeature.MarkdownDialectGitHub))
        else:
            self.textChanged.connect(lambda: self.browser.setText(self.toPlainText()))
            self.browser.setText(self.toPlainText())

    def contextMenuEvent(self, event: QContextMenuEvent, *args):
        menu = QMenu(self)
        highlight_action = QAction("设置高亮", self)
        highlight_action.triggered.connect(self.apply_highlight)
        cancel_highlight_action = QAction('取消高亮', self)
        cancel_highlight_action.triggered.connect(self.cancel_highlight)
        menu.addAction(highlight_action)
        menu.addAction(cancel_highlight_action)
        menu.exec_(event.globalPos())

    def apply_highlight(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return
        text_format = QTextCharFormat()
        text_format.setBackground(QColor(self.highlight))  # 设置背景色为黄色
        cursor.mergeCharFormat(text_format)
        self.update_browser()

    def cancel_highlight(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return
        text_format = QTextCharFormat()
        text_format.setBackground(QColor("#ffffff"))
        cursor.mergeCharFormat(text_format)
        self.update_browser()

    def update_browser(self):
        self.browser.setMarkdown(self.toMarkdown(QTextDocument.MarkdownFeature.MarkdownDialectGitHub))

class _AttrViewDock(QWidget):
    def __init__(self, path: str | None, **kwargs):
        super().__init__(**kwargs)
        """
        Template:
        Family Name: Unknow
        Style Name: Unknow
        Full Name: Unknow
        Weight Class: Unknow
        Is Italic: Unknow
        Underline Position: -77
        Underline Thickness: 155
        Ascender: 2048
        Descender: -512
        Line Gap: 171
        """
        if path:
            self.FontProperties, self.characters = extract_font_properties(path)
        else:
            self.FontProperties, self.characters = {
                "家族": 'Unknow',
                "样式": 'Unknow',
                "完整名字": 'Unknow',
                "粗细": 'Unknow',
                "是否斜体": 'Unknow',
                "垂直偏移量": 'Unknow',
                "下划线粗细": 'Unknow',
                "Ascender": 'Unknow',
                "Descender": 'Unknow',
                "Line Gap": 'Unknow',
                "支持字符数量": 'Unknow'
            }, []
        self.messageLabelRecords: [[QLabel, QLabel]] = []
        self.setBaseUI()

    def setBaseUI(self):
        self.setMinimumSize(180, 350)
        self.setLayout(QVBoxLayout())
        for k, v in self.FontProperties.items():
            h = QHBoxLayout()
            k, v = QLabel(k), QLabel(str(v))
            h.addWidget(k)
            h.addWidget(v)
            self.messageLabelRecords.append([k, v])
            h.setAlignment(Qt.Alignment())
            self.layout().addLayout(h)

    def reset(self, path):
        self.FontProperties, self.characters = extract_font_properties(path)
        try:
            for i, v in enumerate(self.FontProperties.values()):
                self.messageLabelRecords[i][1].setText(str(v))
        except Exception as e:
            print(e)


class _AttrSetDock(QWidget):
    refreshSignal = pyqtSignal(list)
    """
    list[0]
    0：字体大小
    1：粗细
    2：是否斜体
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fontsizeInput = QSpinBox()
        self.weightInput = QSpinBox()
        self.isItalicBtn = QPushButton()
        self.highlightColorDlg = QPushButton()
        self.highlight = '#FFFF00'

        self.setBaseUI()

    def setBaseUI(self):
        v = QVBoxLayout()
        self.setLayout(v)

        def hlay(text, wg) -> None:
            h = QHBoxLayout()
            h.addWidget(QLabel(text))
            h.addWidget(wg)
            h.setAlignment(Qt.Alignment())
            v.addLayout(h)

        self.fontsizeInput.setValue(12)
        self.fontsizeInput.setRange(8, 144)
        self.fontsizeInput.setSingleStep(2)
        self.fontsizeInput.valueChanged.connect(lambda: self.refreshSignal.emit([0, self.fontsizeInput.value()]))
        hlay('字体大小', self.fontsizeInput)

        self.weightInput.setValue(400)
        self.weightInput.setRange(100, 900)
        self.weightInput.setSingleStep(100)
        self.weightInput.valueChanged.connect(lambda: self.refreshSignal.emit([1, self.weightInput.value()]))
        hlay('字体粗细', self.weightInput)

        self.isItalicBtn.setText('False')
        self.isItalicBtn.clicked.connect(lambda: self.isItalicBtn.setText(str(self.isItalicBtn.text() != 'True'))
                                                 or self.refreshSignal.emit([2, self.isItalicBtn.text() != 'True']))
        hlay('是否斜体', self.isItalicBtn)

        self.highlightColorDlg.setStyleSheet('background:#FFFF00')
        self.highlightColorDlg.setText(self.highlight)
        self.highlightColorDlg.clicked.connect(self.changeHl)
        hlay('高亮颜色', self.highlightColorDlg)

    def changeHl(self):
        cdlg: QColor | None = QColorDialog.getColor(QColor(self.highlightColorDlg.text()), self, )
        if cdlg:
            self.highlightColorDlg.setText(cdlg.name())
            self.highlightColorDlg.setStyleSheet(f'background:{cdlg.name()}')
            self.refreshSignal.emit([3, cdlg.name()])

class FontViewer(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.Menubar = QMenuBar()
        self.StatusBar = StateVarious()
        self.AttrViewDock = QDockWidget()
        self.AttrSetDock = QDockWidget()
        self.MainSplitter = QSplitter()
        self.TextViewer = CustomTextBrowser()
        self.TextEditor = RenewableTextEdit(self.TextViewer)
        self.filePath = None  # 只记录当前导入的存在文件

        self.setBaseUI()

    def setBaseUI(self):
        self.setWindowTitle("字体查看器")
        self.setMinimumSize(800, 600)

        self.setCentralWidget(self.MainSplitter)
        self.MainSplitter.setOrientation(Qt.Vertical)
        self.MainSplitter.addWidget(self.TextEditor)
        self.MainSplitter.addWidget(self.TextViewer)
        self.MainSplitter.setSizes([100, 100])

        self.setStatusBar(self.StatusBar)

        self.setMenuBarCfg()
        self.setDockCfg()
        self.setTextEditAndViewerCfg()

    def setMenuBarCfg(self):
        self.setMenuBar(self.Menubar)
        openAct: QAction = self.Menubar.addAction("打开字体文件")
        openAct.triggered.connect(self.loadFont)
        markdownAct: QAction = self.Menubar.addAction('开启Markdown模式中')
        markdownAct.triggered.connect(lambda: self.md_toggle(markdownAct))
        viewUtfAct : QAction = self.Menubar.addAction('查看文本字符集')
        viewUtfAct.triggered.connect(lambda : self.view_blocks())

    def setDockCfg(self):
        self.addDockWidget(Qt.LeftDockWidgetArea, self.AttrSetDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.AttrViewDock)
        self.tabifyDockWidget(self.AttrSetDock, self.AttrViewDock)
        self.AttrSetDock.setWindowTitle("属性调试")
        setDock = _AttrSetDock()
        self.AttrSetDock.setWidget(setDock)
        setDock.refreshSignal.connect(lambda _: self.refreshText(setDock, _))
        self.AttrViewDock.setWindowTitle("属性视图")
        self.AttrViewDock.setWidget(_AttrViewDock(path=None))

    def setTextEditAndViewerCfg(self):
        pass

    def loadFont(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "打开字体文件", "C://", "字体文件 (*.ttf)")
        if filePath:
            # 加载字体
            font_id = QFontDatabase.addApplicationFont(filePath)
            if font_id != -1:
                self.AttrViewDock.widget().reset(filePath)
                # 获取字体系列名称
                self.filePath = filePath
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                child : _AttrViewDock = self.AttrViewDock.widget()
                weight = child.FontProperties['粗细'] if child.FontProperties['粗细'] != 'Unknow' else 400
                italic = child.FontProperties['是否斜体'] if child.FontProperties['是否斜体'] != 'Unknow' else False
                new_font = QFont(font_family, self.AttrSetDock.widget().fontsizeInput.value())
                self.TextEditor.setFont(new_font)
                self.TextViewer.setFont(new_font)
            else:
                print("加载字体失败！")

    def md_toggle(self, action: QAction):
        if action.text().startswith('关'):
            self.TextEditor.toggle_model(True)
            action.setText('开启Markdown模式中')
        else:
            self.TextEditor.toggle_model(False)
            action.setText('关闭Markdown模式中')

    def view_blocks(self):  # 此处有个待优化处，一开始已经读取了一次字符集，现在因为没做到数据共享，又读取了一次
        if self.filePath:
            dlg = BlockViewer(self.filePath)
            dlg.exec_()
        else:
            print("No FilePath exist！")

    def refreshText(self, dock : _AttrSetDock, msgs : list):
        which = msgs[0]
        msg = msgs[1]
        if which != 3:
            f1 : QFont = self.TextEditor.font()
            f2 : QFont = self.TextViewer.font()
            if which == 0:
                f1.setPointSize(msg)
                f2.setPointSize(msg)
            elif which == 1:
                msg = {
                    100: 0,    # Thin
                    200: 12,   # ExtraLight
                    300: 25,   # Light
                    400: 50,   # Normal
                    500: 57,   # Medium
                    600: 63,   # DemiBold
                    700: 75,   # Bold
                    800: 81,   # ExtraBold
                    900: 87    # Black
                }[msg]
                print(msg)
                f1.setWeight(msg)
                f2.setWeight(msg)
            elif which == 2:
                f1.setItalic(msg)
                f2.setItalic(msg)
            self.TextEditor.setFont(f1)
            self.TextViewer.setFont(f2)
        else:
            self.TextEditor.highlight = msgs[1]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('favicon.ico'))
    app.setApplicationName("FontViewer")
    ui = FontViewer()
    ui.setStyleSheet(open('style.css', encoding='u8').read())
    ui.show()
    sys.exit(app.exec_())
