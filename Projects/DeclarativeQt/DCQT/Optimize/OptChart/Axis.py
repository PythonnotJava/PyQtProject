# 轴类型
from typing import Union, Optional, Dict, overload, Iterable, Callable, Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtChart import QAbstractAxis, QValueAxis, QCategoryAxis, QLogValueAxis, QBarCategoryAxis, QDateTimeAxis

from ..QTyping import ColorType, ColorTypeWithPen, ColorTypeWithBrush

# 抽象轴
class AbsAxis(QAbstractAxis):
    def __init__(
            self,
            objectName : Optional[str] = None,
            titleText: Optional[str] = None,  # 标题文本，可选
            titleVisible: bool = True,  # 标题是否可见，默认为 True
            titleFont: Optional[QFont] = None,  # 标题字体，可选
            titleBrush: ColorTypeWithBrush = None,  # 标题画笔，可选
            gridLineColor: ColorType = None,  # 网格线颜色
            gridLinePen: ColorTypeWithPen = None,  # 网格线画笔，可选
            gridLineVisible: bool = False,  # 是否显示网格线，默认为 True
            labelsAngle: int = 90,  # 标签角度，默认为 90 度
            labelsBrush: ColorTypeWithBrush = None,  # 标签画笔，可选
            labelsColor: ColorType = Qt.black,  # 标签颜色，默认为黑色
            labelsEditable: bool = False,  # 标签是否可编辑，默认为 False
            labelsFont: Optional[QFont] = None,  # 标签字体，可选
            labelsVisible: bool = True,  # 标签是否可见，默认为 True
            linePen: ColorTypeWithPen = None,  # 轴线画笔，可选
            linePenColor: ColorType = Qt.black,  # 轴线颜色，默认为黑色
            lineVisible: bool = True,  # 轴线是否可见，默认为 True
            min_=None,  # 最小值，默认为 None
            max_=None,  # 最大值，默认为 None
            range_=None,  # 范围，默认为 None == (min_, max_)
            minorGridLineColor: ColorType = Qt.black,  # 次网格线颜色，默认为黑色
            minorGridLinePen: ColorTypeWithPen = None,  # 次网格线画笔，可选
            minorGridLineVisible: bool = True,  # 是否显示次网格线，默认为 True
            reverse: bool = False,  # 是否反向，默认为 False
            shadesBorderColor: ColorType = Qt.white,  # 区域边框颜色，默认为白色
            shadesBrush: ColorTypeWithBrush = None,  # 区域画刷，可选
            shadesColor: ColorType = Qt.white,  # 区域颜色，默认为白色
            shadesPen: ColorTypeWithPen = None,  # 区域画笔，可选
            shadesVisible: bool = True,  # 区域是否可见，默认为 True
            visible: bool = True,  # 轴是否可见，默认为 True
            **kwargs
    ):
        super().__init__(**kwargs)

        self.setVisible(visible)
        self.setReverse(reverse)

        if objectName:
            self.setObjectName(objectName)
        if titleVisible:
            if titleText:
                self.setTitleText(titleText)
            if titleFont:
                self.setTitleFont(titleFont)
            if titleBrush:
                self.setTitleBrush(titleBrush)
        if gridLineVisible:
            if gridLineColor:
                self.setGridLineColor(gridLineColor)
            if gridLinePen:
                self.setGridLinePen(gridLinePen)
        if labelsVisible:
            self.setLabelsEditable(labelsEditable)
            self.setLabelsAngle(labelsAngle)
            if labelsColor:
                self.setLabelsColor(labelsColor)
            if labelsFont:
                self.setLabelsFont(labelsFont)
            if labelsBrush:
                self.setLabelsBrush(labelsBrush)
        if lineVisible:
            if linePen:
                self.setLinePen(linePen)
            if linePenColor:
                self.setLinePenColor(linePenColor)
        if min_:
            self.setMin(min_)
        if max_:
            self.setMax(max_)
        if range_:
            self.setRange(*range_)
        if minorGridLineVisible:
            if minorGridLineColor:
                self.setMinorGridLineColor(minorGridLineColor)
            if minorGridLinePen:
                self.setMinorGridLinePen(minorGridLinePen)
        if shadesVisible:
            if shadesColor:
                self.setShadesColor(shadesColor)
            if shadesPen:
                self.setShadesPen(shadesPen)
            if shadesBrush:
                self.setShadesBrush(shadesBrush)
            if shadesBorderColor:
                self.setShadesBorderColor(shadesBorderColor)

    def __call__(self, funcLike: Union[Callable, str], *args, **kwargs) -> 'AbsAxis':
        # funcLike可以是直接函数，也可以是类域内的函数，需要传入函数名字去寻找，默认是有这个函数的，不做判断
        func: Callable = getattr(self, funcLike) if isinstance(funcLike, str) else funcLike
        value = func(*args, **kwargs)
        if value:  # @better 有返回值就打印，这里完全可以再传入一个函数参数，用于操作这个value
            print(value)
        return self

    # 只考虑数值，其他默认
    @classmethod
    def justRange(cls, min_ : Any, max_ : Any, **kwargs) -> 'AbsAxis': return cls(min_=min_, max_=max_, **kwargs)

# 用于显示数值数据的轴
class ValueAxis(QValueAxis, AbsAxis):
    """
    ValueAxis(
        labelFormat: Optional[str] = None,  # 标签格式，可选
        minorTickCount: Optional[int] = None,  # 次要刻度线数量，可选
        tickAnchor: Optional[float] = None,  # 刻度锚点，可选
        tickCount: Optional[int] = None,  # 刻度数量，可选
        tickInterval: Optional[float] = None,  # 刻度间隔，可选
        tickType: Optional[QValueAxis.TickType] = None,  # 刻度类型，可选
        objectName : Optional[str] = None,
        titleText: Optional[str] = None,  # 标题文本，可选
        titleVisible: bool = True,  # 标题是否可见，默认为 True
        titleFont: Optional[QFont] = None,  # 标题字体，可选
        titleBrush: ColorTypeWithBrush = None,  # 标题画笔，可选
        gridLineColor: ColorType = None,  # 网格线颜色
        gridLinePen: ColorTypeWithPen = None,  # 网格线画笔，可选
        gridLineVisible: bool = False,  # 是否显示网格线，默认为 True
        labelsAngle: int = 90,  # 标签角度，默认为 90 度
        labelsBrush: ColorTypeWithBrush = None,  # 标签画笔，可选
        labelsColor: ColorType = Qt.black,  # 标签颜色，默认为黑色
        labelsEditable: bool = False,  # 标签是否可编辑，默认为 False
        labelsFont: Optional[QFont] = None,  # 标签字体，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        linePen: ColorTypeWithPen = None,  # 轴线画笔，可选
        linePenColor: ColorType = Qt.black,  # 轴线颜色，默认为黑色
        lineVisible: bool = True,  # 轴线是否可见，默认为 True
        min_=None,  # 最小值，默认为 None
        max_=None,  # 最大值，默认为 None
        range_=None,  # 范围，默认为 None == (min_, max_)
        minorGridLineColor: ColorType = Qt.black,  # 次网格线颜色，默认为黑色
        minorGridLinePen: ColorTypeWithPen = None,  # 次网格线画笔，可选
        minorGridLineVisible: bool = True,  # 是否显示次网格线，默认为 True
        reverse: bool = True,  # 是否反向，默认为 True
        shadesBorderColor: ColorType = Qt.white,  # 区域边框颜色，默认为白色
        shadesBrush: ColorTypeWithBrush = None,  # 区域画刷，可选
        shadesColor: ColorType = Qt.white,  # 区域颜色，默认为白色
        shadesPen: ColorTypeWithPen = None,  # 区域画笔，可选
        shadesVisible: bool = True,  # 区域是否可见，默认为 True
        visible: bool = True,  # 轴是否可见，默认为 True
        **kwargs
    )
    """
    def __init__(
            self,
            labelFormat: Optional[str] = None,  # 标签格式，可选
            minorTickCount: Optional[int] = None,  # 次要刻度线数量，可选
            tickAnchor: Optional[float] = None,  # 刻度锚点，可选
            tickCount: Optional[int] = None,  # 刻度数量，可选
            tickInterval: Optional[float] = None,  # 刻度间隔，可选
            tickType: Optional[QValueAxis.TickType] = None,  # 刻度类型，可选
            **kwargs
    ):
        super().__init__(**kwargs)
        if labelFormat:
            self.setLabelFormat(labelFormat)
        if minorTickCount:
            self.setMinorTickCount(minorTickCount)
        if tickType:
            self.setTickType(tickType)
        if tickAnchor:
            self.setTickAnchor(tickAnchor)
        if tickCount:
            self.setTickCount(tickCount)
        if tickInterval:
            self.setTickInterval(tickInterval)
# 用于显示分类数据的轴
class CategoryAxis(QCategoryAxis, AbsAxis):
    """
    CategoryAxis(
        categories: Dict[str, float],  # 分类与对应数值组成的键值对
        labelsPosition: Optional[QCategoryAxis.AxisLabelsPosition] = None,  # 标签位置
        startValue: Optional[float] = None,  # 轴起始值
        labelFormat: Optional[str] = None,  # 标签格式，可选
        minorTickCount: Optional[int] = None,  # 次要刻度线数量，可选
        tickAnchor: Optional[float] = None,  # 刻度锚点，可选
        tickCount: Optional[int] = None,  # 刻度数量，可选
        tickInterval: Optional[float] = None,  # 刻度间隔，可选
        tickType: Optional[QValueAxis.TickType] = None,  # 刻度类型，可选
        objectName : Optional[str] = None,
        titleText: Optional[str] = None,  # 标题文本，可选
        titleVisible: bool = True,  # 标题是否可见，默认为 True
        titleFont: Optional[QFont] = None,  # 标题字体，可选
        titleBrush: ColorTypeWithBrush = None,  # 标题画笔，可选
        gridLineColor: ColorType = None,  # 网格线颜色
        gridLinePen: ColorTypeWithPen = None,  # 网格线画笔，可选
        gridLineVisible: bool = False,  # 是否显示网格线，默认为 True
        labelsAngle: int = 90,  # 标签角度，默认为 90 度
        labelsBrush: ColorTypeWithBrush = None,  # 标签画笔，可选
        labelsColor: ColorType = Qt.black,  # 标签颜色，默认为黑色
        labelsEditable: bool = False,  # 标签是否可编辑，默认为 False
        labelsFont: Optional[QFont] = None,  # 标签字体，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        linePen: ColorTypeWithPen = None,  # 轴线画笔，可选
        linePenColor: ColorType = Qt.black,  # 轴线颜色，默认为黑色
        lineVisible: bool = True,  # 轴线是否可见，默认为 True
        min_=None,  # 最小值，默认为 None
        max_=None,  # 最大值，默认为 None
        range_=None,  # 范围，默认为 None == (min_, max_)
        minorGridLineColor: ColorType = Qt.black,  # 次网格线颜色，默认为黑色
        minorGridLinePen: ColorTypeWithPen = None,  # 次网格线画笔，可选
        minorGridLineVisible: bool = True,  # 是否显示次网格线，默认为 True
        reverse: bool = True,  # 是否反向，默认为 True
        shadesBorderColor: ColorType = Qt.white,  # 区域边框颜色，默认为白色
        shadesBrush: ColorTypeWithBrush = None,  # 区域画刷，可选
        shadesColor: ColorType = Qt.white,  # 区域颜色，默认为白色
        shadesPen: ColorTypeWithPen = None,  # 区域画笔，可选
        shadesVisible: bool = True,  # 区域是否可见，默认为 True
        visible: bool = True,  # 轴是否可见，默认为 True
        **kwargs
    )
    """
    def __init__(
            self,
            categories: Dict[str, float],  # 分类与对应数值组成的键值对
            labelsPosition: Optional[QCategoryAxis.AxisLabelsPosition] = None,  # 标签位置
            startValue: Optional[float] = None,  # 轴起始值
            **kwargs
    ):
        super().__init__(**kwargs)

        for category, position in categories.items():
            self.append(category, position)
        if labelsPosition:
            self.setLabelsPosition(labelsPosition)
        if startValue is not None:
            self.setStartValue(startValue)

    @overload
    def append(self, label: str, categoryEndValue: float) -> None: ...
    @overload
    def append(self, categories: Dict[str, float]) -> None: ...
    def append(self, *args, **_):
        if len(args) == 2:
            super().append(args[0], args[1])
        else:
            for category, position in args[0].items():
                super().append(category, position)

# 用于对数值数据进行对数变换的轴
class LogValueAxis(QLogValueAxis, AbsAxis):
    """
    LogValueAxis(
        base: Optional[float] = None,  # 对数的基数
        labelFormat: Optional[str] = None,  # 标签格式
        minorTickCount: Optional[int] = None,  # 次要刻度线数量
        objectName : Optional[str] = None,
        titleText: Optional[str] = None,  # 标题文本，可选
        titleVisible: bool = True,  # 标题是否可见，默认为 True
        titleFont: Optional[QFont] = None,  # 标题字体，可选
        titleBrush: ColorTypeWithBrush = None,  # 标题画笔，可选
        gridLineColor: ColorType = None,  # 网格线颜色
        gridLinePen: ColorTypeWithPen = None,  # 网格线画笔，可选
        gridLineVisible: bool = False,  # 是否显示网格线，默认为 True
        labelsAngle: int = 90,  # 标签角度，默认为 90 度
        labelsBrush: ColorTypeWithBrush = None,  # 标签画笔，可选
        labelsColor: ColorType = Qt.black,  # 标签颜色，默认为黑色
        labelsEditable: bool = False,  # 标签是否可编辑，默认为 False
        labelsFont: Optional[QFont] = None,  # 标签字体，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        linePen: ColorTypeWithPen = None,  # 轴线画笔，可选
        linePenColor: ColorType = Qt.black,  # 轴线颜色，默认为黑色
        lineVisible: bool = True,  # 轴线是否可见，默认为 True
        min_=None,  # 最小值，默认为 None
        max_=None,  # 最大值，默认为 None
        range_=None,  # 范围，默认为 None == (min_, max_)
        minorGridLineColor: ColorType = Qt.black,  # 次网格线颜色，默认为黑色
        minorGridLinePen: ColorTypeWithPen = None,  # 次网格线画笔，可选
        minorGridLineVisible: bool = True,  # 是否显示次网格线，默认为 True
        reverse: bool = True,  # 是否反向，默认为 True
        shadesBorderColor: ColorType = Qt.white,  # 区域边框颜色，默认为白色
        shadesBrush: ColorTypeWithBrush = None,  # 区域画刷，可选
        shadesColor: ColorType = Qt.white,  # 区域颜色，默认为白色
        shadesPen: ColorTypeWithPen = None,  # 区域画笔，可选
        shadesVisible: bool = True,  # 区域是否可见，默认为 True
        visible: bool = True,  # 轴是否可见，默认为 True
        **kwargs
    )
    """
    def __init__(
            self,
            base: Optional[float] = None,  # 对数的基数
            labelFormat: Optional[str] = None,  # 标签格式
            minorTickCount: Optional[int] = None,  # 次要刻度线数量
            **kwargs
    ):
        super().__init__(**kwargs)
        if base:
            self.setBase(base)
        if labelFormat:
            self.setLabelFormat(labelFormat)
        if minorTickCount:
            self.setMinorTickCount(minorTickCount)

class BarCategoryAxis(QBarCategoryAxis, AbsAxis):
    """
    BarCategoryAxis(
        barCategory : Union[str, Iterable[str], None] = None,  # 用于在轴上添加初始类别数据
        objectName : Optional[str] = None,
        titleText: Optional[str] = None,  # 标题文本，可选
        titleVisible: bool = True,  # 标题是否可见，默认为 True
        titleFont: Optional[QFont] = None,  # 标题字体，可选
        titleBrush: ColorTypeWithBrush = None,  # 标题画笔，可选
        gridLineColor: ColorType = None,  # 网格线颜色
        gridLinePen: ColorTypeWithPen = None,  # 网格线画笔，可选
        gridLineVisible: bool = False,  # 是否显示网格线，默认为 True
        labelsAngle: int = 90,  # 标签角度，默认为 90 度
        labelsBrush: ColorTypeWithBrush = None,  # 标签画笔，可选
        labelsColor: ColorType = Qt.black,  # 标签颜色，默认为黑色
        labelsEditable: bool = False,  # 标签是否可编辑，默认为 False
        labelsFont: Optional[QFont] = None,  # 标签字体，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        linePen: ColorTypeWithPen = None,  # 轴线画笔，可选
        linePenColor: ColorType = Qt.black,  # 轴线颜色，默认为黑色
        lineVisible: bool = True,  # 轴线是否可见，默认为 True
        min_=None,  # 最小值，默认为 None
        max_=None,  # 最大值，默认为 None
        range_=None,  # 范围，默认为 None == (min_, max_)
        minorGridLineColor: ColorType = Qt.black,  # 次网格线颜色，默认为黑色
        minorGridLinePen: ColorTypeWithPen = None,  # 次网格线画笔，可选
        minorGridLineVisible: bool = True,  # 是否显示次网格线，默认为 True
        reverse: bool = True,  # 是否反向，默认为 True
        shadesBorderColor: ColorType = Qt.white,  # 区域边框颜色，默认为白色
        shadesBrush: ColorTypeWithBrush = None,  # 区域画刷，可选
        shadesColor: ColorType = Qt.white,  # 区域颜色，默认为白色
        shadesPen: ColorTypeWithPen = None,  # 区域画笔，可选
        shadesVisible: bool = True,  # 区域是否可见，默认为 True
        visible: bool = True,  # 轴是否可见，默认为 True
        **kwargs
    )
    """
    def __init__(
            self,
            barCategory : Union[str, Iterable[str], None] = None,  # 用于在轴上添加初始类别数据
            **kwargs
    ):
        super().__init__(**kwargs)
        self.append(barCategory)

# 用于在图表中绘制带有日期和时间刻度的轴
class DateTimeAxis(QDateTimeAxis, AbsAxis):
    """
    DateTimeAxis(
        format_ : Optional[str] = None,
        tickCount : Optional[int] = None,
        objectName : Optional[str] = None,
        titleText: Optional[str] = None,  # 标题文本，可选
        titleVisible: bool = True,  # 标题是否可见，默认为 True
        titleFont: Optional[QFont] = None,  # 标题字体，可选
        titleBrush: ColorTypeWithBrush = None,  # 标题画笔，可选
        gridLineColor: ColorType = None,  # 网格线颜色
        gridLinePen: ColorTypeWithPen = None,  # 网格线画笔，可选
        gridLineVisible: bool = False,  # 是否显示网格线，默认为 True
        labelsAngle: int = 90,  # 标签角度，默认为 90 度
        labelsBrush: ColorTypeWithBrush = None,  # 标签画笔，可选
        labelsColor: ColorType = Qt.black,  # 标签颜色，默认为黑色
        labelsEditable: bool = False,  # 标签是否可编辑，默认为 False
        labelsFont: Optional[QFont] = None,  # 标签字体，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        linePen: ColorTypeWithPen = None,  # 轴线画笔，可选
        linePenColor: ColorType = Qt.black,  # 轴线颜色，默认为黑色
        lineVisible: bool = True,  # 轴线是否可见，默认为 True
        min_=None,  # 最小值，默认为 None
        max_=None,  # 最大值，默认为 None
        range_=None,  # 范围，默认为 None == (min_, max_)
        minorGridLineColor: ColorType = Qt.black,  # 次网格线颜色，默认为黑色
        minorGridLinePen: ColorTypeWithPen = None,  # 次网格线画笔，可选
        minorGridLineVisible: bool = True,  # 是否显示次网格线，默认为 True
        reverse: bool = True,  # 是否反向，默认为 True
        shadesBorderColor: ColorType = Qt.white,  # 区域边框颜色，默认为白色
        shadesBrush: ColorTypeWithBrush = None,  # 区域画刷，可选
        shadesColor: ColorType = Qt.white,  # 区域颜色，默认为白色
        shadesPen: ColorTypeWithPen = None,  # 区域画笔，可选
        shadesVisible: bool = True,  # 区域是否可见，默认为 True
        visible: bool = True,  # 轴是否可见，默认为 True
        **kwargs
    )
    """
    def __init__(
            self,
            format_ : Optional[str] = None,
            tickCount : Optional[int] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if format_:
            self.setFormat(format_)
        if tickCount:
            self.setTickCount(tickCount)

__all__ = ['AbsAxis', 'ValueAxis', 'CategoryAxis', 'LogValueAxis', 'BarCategoryAxis', 'DateTimeAxis']