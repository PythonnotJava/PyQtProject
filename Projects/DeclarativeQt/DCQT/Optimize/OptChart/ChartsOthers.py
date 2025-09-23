from typing import Union, Optional, Iterable, List

from PyQt5.QtCore import QObject, Qt, QMarginsF
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtChart import QLegend, QBarSet, QBoxSet, QPieSlice, QCandlestickSet

from ..QTyping import ColorType, ColorTypeWithPen, ColorTypeWithBrush

class Legend(QLegend):
    def __init__(
        self,
        align: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
        backgroundVisible: bool = True,  # 背景可见性
        pen: ColorTypeWithPen = None,  # 背景边框设置
        backgroundColor: ColorType = QColor('skyblue'),  # 背景颜色
        borderColor: ColorType = Qt.black,  # 背景边框颜色，会与QPen的颜色冲突
        brush: ColorTypeWithBrush = None,
        font: Optional[QFont] = None,
        labelBrush: ColorTypeWithBrush = None,
        labelColor: ColorType = QColor('skyblue'),  # 标记边框颜色
        markerShape: QLegend.MarkerShape = QLegend.MarkerShapeRectangle,
        reverseMarkers: bool = True,
        showToolTips: bool = True,
        tips: Optional[str] = None,  # 标记提示
        contentMargins: Optional[Union[QMarginsF, Iterable]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setAlignment(align)
        self.setBackgroundVisible(backgroundVisible)
        self.setShowToolTips(showToolTips)
        self.setMarkerShape(markerShape)
        self.setReverseMarkers(reverseMarkers)

        if contentMargins:
            self.setContentsMargins(contentMargins if isinstance(contentMargins, QMarginsF) else QMarginsF(contentMargins))
        if labelColor:
            self.setLabelColor(labelColor)
        if backgroundColor:
            self.setColor(backgroundColor)
        if borderColor:
            self.setBorderColor(borderColor)
        if brush:
            self.setBrush(brush)
        if font:
            self.setFont(font)
        if pen:
            self.setPen(pen)
        if tips:
            self.setToolTip(tips)
        if labelBrush:
            self.setLabelBrush(labelBrush)

def FunctionalLegend(
    legend : QLegend,
    align: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
    backgroundVisible: bool = True,  # 背景可见性
    pen: ColorTypeWithPen = None,  # 背景边框设置
    backgroundColor: ColorType = QColor('skyblue'),  # 背景颜色
    borderColor: ColorType = Qt.black,  # 背景边框颜色，会与QPen的颜色冲突
    brush: ColorTypeWithBrush = None,
    font: Optional[QFont] = None,
    labelBrush: ColorTypeWithBrush = None,
    labelColor: ColorType = QColor('skyblue'),  # 标记边框颜色
    markerShape: QLegend.MarkerShape = QLegend.MarkerShapeRectangle,
    reverseMarkers: bool = True,
    showToolTips: bool = True,
    tips: Optional[str] = None,  # 标记提示
    contentMargins: Optional[Union[QMarginsF, Iterable]] = None,
    **kwargs
) -> QLegend:
    legend.setAlignment(align)
    legend.setBackgroundVisible(backgroundVisible)
    legend.setShowToolTips(showToolTips)
    legend.setMarkerShape(markerShape)
    legend.setReverseMarkers(reverseMarkers)
    if contentMargins:
        legend.setContentsMargins(contentMargins if isinstance(contentMargins, QMarginsF) else QMarginsF(contentMargins))
    if labelColor:
        legend.setLabelColor(labelColor)
    if backgroundColor:
        legend.setColor(backgroundColor)
    if borderColor:
        legend.setBorderColor(borderColor)
    if brush:
        legend.setBrush(brush)
    if font:
        legend.setFont(font)
    if pen:
        legend.setPen(pen)
    if tips:
        legend.setToolTip(tips)
    if labelBrush:
        legend.setLabelBrush(labelBrush)

    for key, value in kwargs.items():
        setattr(legend, key, value)

    return legend

class BarSet(QBarSet):
    def __init__(
            self,
            label : str,
            sets : Union[float, Iterable[float], None] = None,
            borderColor : ColorType = Qt.black,
            brush : ColorTypeWithBrush = None,
            color : ColorType = QColor('skyblue'),
            labelBrush : ColorTypeWithBrush = None,
            labelColor : ColorType = Qt.black,
            labelFont : Optional[QFont] = None,
            pen : ColorTypeWithPen = None,
            parent=None
    ):
        super().__init__(label, parent)
        if sets:
            self.append(sets)
        if borderColor:
            self.setBorderColor(borderColor)
        if brush:
            self.setBrush(brush)
        if color:
            self.setColor(color)
        if labelBrush:
            self.setLabelBrush(labelBrush)
        if labelColor:
            self.setLabelColor(labelColor)
        if labelFont:
            self.setLabelFont(labelFont)
        if pen:
            self.setPen(pen)

class BoxSet(QBoxSet):
    def __init__(
            self,
            sets : Union[float, Iterable[float], None] = None,
            brush : ColorTypeWithBrush = None,
            label : Optional[str] = None,
            pen : ColorTypeWithPen = None,
            value : Optional[List] = None,
            parent : Optional[QObject] = None,
            objectName : Optional[str] = None
    ):
        super().__init__()
        if parent:
            self.setParent(parent)
        if objectName:
            self.setObjectName(objectName)
        if sets:
            self.append(sets)
        if brush:
            self.setBrush(brush)
        if label:
            self.setLabel(label)
        if pen:
            self.setPen(pen)
        if value:
            self.setValue(*value)

class PieSlice(QPieSlice):
    def __init__(
            self,
            label: str,  # 饼图切片的标签
            value: float,  # 切片的值
            labelArmLengthFactor: float = 1.,  # 标签臂长度因子
            labelBrush: ColorTypeWithBrush = None,  # 标签画刷
            labelColor: ColorType = Qt.black,  # 标签颜色
            labelFont: Optional[QFont] = None,  # 标签字体
            labelPosition: QPieSlice.LabelPosition = QPieSlice.LabelInsideNormal,  # 标签位置
            labelVisible: bool = True,  # 是否显示标签
            borderColor: ColorType = Qt.black,  # 边框颜色
            borderWidth: int = 1,  # 边框宽度
            brush: ColorTypeWithBrush = None,  # 填充刷子
            color: ColorType = Qt.blue,  # 切片颜色
            exploded: bool = True,  # 是否分离
            explodeDistanceFactor: float = 1.,  # 分离距离因子
            pen: ColorTypeWithPen = None,  # 画笔
            parent: Optional[QObject] = None,
            objectName: Optional[str] = None
    ):
        super().__init__(label, value)
        self.setValue(value)

        if pen:
            self.setPen(pen)
        if exploded:
            self.setExplodeDistanceFactor(explodeDistanceFactor)
        if parent:
            self.setParent(parent)
        if objectName:
            self.setObjectName(objectName)
        if labelVisible:
            if label:
                self.setLabelArmLengthFactor(labelArmLengthFactor)
                self.setLabelPosition(labelPosition)
                self.setLabel(label)
                if labelBrush:
                    self.setLabelBrush(labelBrush)
                if labelColor:
                    self.setLabelColor(labelColor)
                if labelFont:
                    self.setLabelFont(labelFont)
        if borderColor and borderWidth:
            self.setBorderColor(borderColor)
            self.setBorderWidth(borderWidth)
        if brush:
            self.setBrush(brush)
        if color:
            self.setColor(color)

class CandlestickSet(QCandlestickSet):
    def __init__(
            self,
            brush: ColorTypeWithBrush = None,  # 蜡烛图集合的填充刷子
            close: float = 1.,  # 收盘价
            high: float = 1.,  # 最高价
            low: float = 1.,  # 最低价
            open_: float = 1.,  # 开盘价
            pen: ColorTypeWithPen = None,  # 画笔
            timestamp: float = 0.,  # 时间戳
            parent: Optional[QObject] = None,
            objectName: Optional[str] = None
    ):
        super().__init__()
        self.setHigh(high)
        self.setLow(low)
        self.setClose(close)
        self.setOpen(open_)
        self.setTimestamp(timestamp)

        if pen:
            self.setPen(pen)
        if brush:
            self.setBrush(brush)
        if parent:
            self.setParent(parent)
        if objectName:
            self.setObjectName(objectName)

__all__ = ['Legend', 'BarSet', 'BoxSet', 'PieSlice', 'CandlestickSet', 'FunctionalLegend']