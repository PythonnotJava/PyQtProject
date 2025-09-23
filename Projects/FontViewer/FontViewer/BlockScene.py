import sys

from PyQt5.QtCore import QPointF, Qt, QTimer, QRectF
from PyQt5.QtGui import QFont, QPainter
from fontTools.ttLib import TTFont
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsSimpleTextItem, QApplication, QDialog

class GlyphBlock(QGraphicsRectItem):
    """单个字符块"""
    def __init__(self, char, code, font, rect, parent=None):
        super().__init__(rect, parent)
        self.char = char  # 显示的字符
        self.code = code  # 对应的编码
        self.font = font  # 字体
        self.default_brush = Qt.white  # 默认背景色
        self.clicked_brush = Qt.gray  # 点击时的背景色
        self.setBrush(self.default_brush)

        self.setup_content()

    def setup_content(self):
        """设置字符和编码的显示内容"""
        # 字符
        char_item = QGraphicsSimpleTextItem(self.char, self)
        char_item.setFont(self.font)
        char_item.setBrush(Qt.black)
        char_item.setPos(self.rect().center() - char_item.boundingRect().center() + QPointF(0, -10))

        # 编码
        code_item = QGraphicsSimpleTextItem(self.code, self)
        code_item.setFont(QFont("Arial", 8))
        code_item.setBrush(Qt.black)
        code_item.setPos(self.rect().center() - code_item.boundingRect().center() + QPointF(0, 20))

    def mousePressEvent(self, event):
        """点击事件：复制编码并触发点击效果"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code)  # 复制编码
        self.setBrush(self.clicked_brush)  # 点击效果
        QTimer.singleShot(200, lambda: self.setBrush(self.default_brush))  # 恢复默认背景色
        super().mousePressEvent(event)

class _BlockViewer(QGraphicsView):
    """字体展示窗口"""
    def __init__(self, font_path, p):
        super().__init__(p)
        self.font_path = font_path
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("字体展示")
        self.setRenderHint(QPainter.Antialiasing)

        # 加载字体
        font = self.load_font(self.font_path)
        if font is None:
            print("字体加载失败")
            return

        # 提取字体中的所有字符
        chars = self.extract_characters_from_font(self.font_path)

        # 布局参数
        cols = 10  # 每行固定 10 个块
        block_size = 60
        margin = 10

        # 绘制字符块
        for idx, (char, code) in enumerate(chars):
            row = idx // cols
            col = idx % cols
            x = col * (block_size + margin)
            y = row * (block_size + margin)
            rect = QRectF(x, y, block_size, block_size)
            block = GlyphBlock(char.upper(), code, font, rect)
            self.scene.addItem(block)

        # 设置场景大小
        total_width = cols * (block_size + margin) - margin
        total_height = (len(chars) // cols + 1) * (block_size + margin) - margin
        self.scene.setSceneRect(0, 0, total_width, total_height)

    @staticmethod
    def load_font(font_path):
        """加载字体"""
        try:
            font = QFont(font_path)
            return font
        except Exception as e:
            print(f"加载字体失败: {e}")
            return None

    @staticmethod
    def extract_characters_from_font(font_path):
        """使用fonttools提取字体中的字符"""
        font = TTFont(font_path)  # 使用fonttools打开字体文件
        chars = []

        # 获取所有字符
        for cmap in font['cmap'].tables:
            for char_code, glyph_name in cmap.cmap.items():
                char = chr(char_code)  # 将字符代码转换为字符
                chars.append((char, f"U+{char_code:04X}"))

        return chars

class BlockViewer(QDialog):
    def __init__(self, path):
        super().__init__()
        self.setFixedSize(730, 730)
        self.gh = _BlockViewer(path, self)
        self.gh.setGeometry(10, 10, 710, 710)

__all__ = ['BlockViewer']
if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_path = "fonts/Menlo-Bold.ttf"  # 替换为实际字体文件路径
    font_viewer = BlockViewer(font_path)
    font_viewer.show()
    sys.exit(app.exec_())
