import sys
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *

from SideBar import SideBar
from OptimizeQt import *
from CanvasUI import *

WHATTHIS = "Find Simple tools in Drawer."


class SimpleDrawer(QMainWindow, AbstractWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.homePage = OptLabel.textBuild(text="Home")
        self.scaGallery = TabCanvas()
        self.lineGallery = TabCanvas()
        self.pieGallery = TabCanvas()
        self.barGallery = TabCanvas()

        self.__setUI()

    def __setUI(self) -> None:
        self.setCentralWidget(
            OptSplitter(
                horizontal=True,
                widgets=[
                    SideBar(
                        leader_func=lambda: self.setStackWidget(0),
                        scatter_func=lambda: self.setStackWidget(1),
                        line_func=lambda: self.setStackWidget(2),
                        bar_func=lambda: self.setStackWidget(3),
                        pie_func=lambda: self.setStackWidget(4)
                    ),
                    Stack(
                        minw=400,
                        widgets=[
                            self.homePage,
                            self.scaGallery,
                            self.lineGallery,
                            self.barGallery,
                            self.pieGallery,
                        ],
                        currentIndex=0,
                        objectName='stack'
                    )
                ]
            )
        )

        self.scaGallery.linkOpenFunction(self.drawScatter)

    def setStackWidget(self, index: int) -> None:
        stack: Stack = self.findChild(Stack, 'stack')
        if index != stack.currentIndex:
            stack.setCurrentIndex(index)

    def drawScatter(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "打开散点图模板",
            "C:/",
            "模板(*.json)"
        )
        if fileName:
            try:
                wrapper = ScatterWrapper(fileName).data
                self.scaGallery.append(TabType(
                    widget=ScatterView(wrapper),
                    title=wrapper.get('title')
                ))
            except Exception as e:
                w = AbstractWidget()
                w.setUniqueWidget(
                    widget=OptLabel.textBuild(text=e.__str__(), textWrap=True),
                    contentMargins=[0, 0, 0, 0]
                )
                self.scaGallery.append(TabType(
                    widget=w,
                    title=str(type(e))
                ))
            self.scaGallery.setCurrentPath(fileName)
        else:
            self.scaGallery.setCurrentPath("Lost FilePath!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = SimpleDrawer()
    ui.show()
    sys.exit(app.exec_())