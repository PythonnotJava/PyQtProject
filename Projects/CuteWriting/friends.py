# -*- coding: utf-8 -*-
import sys
import qtawesome
import os

from PyQt5.QtCore import (QMimeData,
                          QFileInfo,
                          QUrl,
                          QFile,
                          QBuffer,
                          QIODevice,
                          QByteArray,
                          Qt,
                          QThread,
                          QRect,
                          QSize)
import json
import pyttsx3
from PyQt5.QtGui import (QImageReader,
                         QImage,
                         QTextDocumentFragment,
                         QTextCursor,
                         QFont,
                         QCloseEvent,
                         QIcon,
                         QPixmap,
                         QPaintEvent,
                         QColor,
                         QPainter,
                         QResizeEvent,
                         QCursor)
from PyQt5.QtWidgets import (QTextEdit,
                             QMessageBox,
                             QDialog,
                             QLabel,
                             QSlider,
                             QApplication,
                             QFormLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QMainWindow,
                             QPushButton,
                             QToolButton,
                             QFrame,
                             QMenu,
                             QAction,
                             QFileDialog,
                             QFontDialog,
                             QColorDialog)

from configobj import ConfigObj
from beaqss import *

class TextEdit(QTextEdit):
    def __init__(self, p): super(TextEdit, self).__init__(p)

    def canInsertFromMimeData(self, source: QMimeData) -> bool:
        return source.hasImage() or source.hasUrls() or super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source: QMimeData) -> None:
        if source.hasImage(): self.insert_image(source.imageData())
        elif source.hasUrls():
            for url in source.urls():
                file_info = QFileInfo(url.toLocalFile())
                ext = file_info.suffix().lower()
                if ext in QImageReader.supportedImageFormats(): self.insert_image(QImage(file_info.filePath()), ext)
                else: self.insert_file(url)
        else: super(TextEdit, self).insertFromMimeData(source)


    def insert_image(self, image: QImage, fmt: str = "png"):
        """插入图片"""
        try:
            data = QByteArray()
            buffer = QBuffer(data)
            image.save(buffer, fmt)
            base64_data = str(data.toBase64())[2:-1]
            data = f'<img src="data:image/{fmt};base64,{base64_data}" />'
            fragment = QTextDocumentFragment.fromHtml(data)
            self.textCursor().insertFragment(fragment)
        except: QMessageBox.warning(self, 'Error', 'Something wrong in the pictures or pictures!', QMessageBox.Ok)

    def insert_file(self, url: QUrl):
        """插入文件"""
        file = None
        try:
            file = QFile(url.toLocalFile())
            if file.fileName().endswith('ml'):
                if not file.open(QIODevice.ReadOnly or QIODevice.Text): return
                file_data = file.readAll()
                # try:
                __t : QTextCursor = self.textCursor()
                __t.insertHtml(str(file_data, encoding="utf8"))
                # except: QMessageBox.warning(self, 'Error', 'Just can‘t read in it1!', QMessageBox.Ok)
            else:
                # try:
                __f = open(file.fileName(), 'r', encoding='U8')
                __t1 = __f.read()
                __f.close()
                __t2 : QTextCursor = self.textCursor()
                __t2.insertText(__t1)
                # except: pass
        except Exception:
            if file: file.close()

def operateJson(path='src/cfg/setting.json'):
    _f = open(path, 'r', encoding='U8')
    _t = json.load(_f)
    _f.close()
    return _t

def reloadJson(path='src/cfg/setting.json', obj=None):
    if obj is None:
        obj = {'font': {'size': 9, 'family': '隶书', 'color': [29, 214, 255, 255], 'weight': 50, 'style': 0},
               'theme': {'bg': 'src/img/bg.png'}}
    _f = open(path, 'w', encoding='U8')
    json.dump(obj, _f)
    _f.close()


# 自定义CWML文件(基于json文件)的读取操作
def writeInCWML(obj, path=r'src\exa\model.cwml'):
    _f = open(path, 'w', encoding='U8')
    json.dump(obj, _f)
    _f.close()

def readInCWML(path):
    _f = open(path, 'r', encoding='U8')
    _t = json.load(_f)
    _f.close()
    """
    Aout _t : U will get an obj as below : 
    {"font": 
        {
        "size": 72, 
        "family": "\u534e\u6587\u884c\u6977", 
        "color": [15, 7, 255, 255], 
        "weight": 50, 
        "style": 0
            }, 
    "theme": {
        "bg": "src/img/bg.png"
            },
    "content" : "对于内容、图片内容，使用链接声明"
    }
    """
    return _t['font']['size'], _t['font']['family'], _t['font']['color'], _t['font']['weight'], _t['font']['style'], _t['content']

# 语音读取
def sayWord(word):
    teacher = pyttsx3.init()
    teacher.say(word)
    teacher.runAndWait()

# 多线程用来防卡顿
class MyThread(QThread):
    def __init__(self, func, *args):
        super(MyThread, self).__init__()
        self.func = func
        self.arg = args

    def run(self): self.func(*self.arg)