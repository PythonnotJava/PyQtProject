# 为了QtChart方便而封装的类
from typing import Optional, Union, Sequence, Iterable, Dict, Literal
# @warning 在 Python 的 dataclasses 模块中，默认的可变类型（如列表、字典、对象实例等）不能直接作为字段的默认值。
# 这是为了防止所有实例共享同一个可变默认值，导致意外的行为。相反，应该使用 default_factory 来创建每个实例的默认值
from dataclasses import dataclass

from PyQt5.QtGui import QFont, QPen, QColor
from PyQt5.QtCore import Qt, QMarginsF, QEasingCurve
from PyQt5.QtChart import QAbstractAxis, QLegend, QChart, QAbstractSeries, QPolarChart
from PyQt5.QtWidgets import QGraphicsItem

from Optimize.QTyping import *

# 绑定着伴有方向坐标轴的图表类
# 图表是可以不绑定轴的
# 备注：使用QPolarChart以及QPolarChart子类需要把aligns声明为：QPolarChart.PolarOrientation
@dataclass
class SeriesBindAxesWithAligns:
    series : QAbstractSeries
    axesWithAligns : Optional[Dict[QAbstractAxis, Union[Qt.AlignmentFlag, Qt.Alignment]]] = None

@dataclass
class FontStyle:
    size: int = 12  # 字体大小（以点为单位）
    bold: bool = True  # 是否加粗
    weight: int = 900  # 字体权重，范围是0-1000，通常400为正常，700为加粗
    family: str = "微软雅黑"  # 字体家族名称
    italic: bool = False  # 是否斜体
    underline: bool = False  # 是否有下划线
    strike_out: bool = False  # 是否有删除线
    kerning: bool = True  # 是否启用字距调整
    capitalization: QFont.Capitalization = QFont.MixedCase  # 字体大小写转换方式
    letter_spacing: float = 0.0  # 字母间距
    word_spacing: float = 0.0  # 单词间距
    stretch: int = QFont.Unstretched  # 字体拉伸度，范围是0-4000，默认是100（正常）
    style_strategy: QFont.StyleStrategy = QFont.PreferDefault  # 字体样式策略

    def toQFont(self) -> QFont:
        """
        将 FontStyle 对象转换为 QFont 对象，设置 QFont 的各个属性并返回。
        """
        font = QFont()
        font.setFamily(self.family)
        font.setPointSize(self.size)
        font.setBold(self.bold)
        font.setWeight(self.weight)
        font.setItalic(self.italic)
        font.setUnderline(self.underline)
        font.setStrikeOut(self.strike_out)
        font.setKerning(self.kerning)
        font.setCapitalization(self.capitalization)
        font.setLetterSpacing(QFont.AbsoluteSpacing, self.letter_spacing)
        font.setWordSpacing(self.word_spacing)
        font.setStretch(self.stretch)
        font.setStyleStrategy(self.style_strategy)
        return font

class LegendStyle(Dict):
    def __init__(
        self,
        align: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignBottom,
        backgroundVisible: bool = True,  # 背景可见性
        pen: ColorTypeWithPen = None,  # 背景边框设置
        backgroundColor: ColorType = None,  # 背景颜色
        borderColor: ColorType = None,  # 背景边框颜色，会与QPen的颜色冲突
        brush: ColorTypeWithBrush = None,
        font: Optional[QFont] = None,
        labelBrush: ColorTypeWithBrush = None,
        labelColor: ColorType = None,  # 标记边框颜色
        markerShape: QLegend.MarkerShape = QLegend.MarkerShapeRectangle,
        reverseMarkers: bool = True,
        showToolTips: bool = True,
        tips: Optional[str] = None,  # 标记提示
        contentMargins: Optional[Union[QMarginsF, Iterable]] = None,
        parent: Optional[QGraphicsItem] = None,
        flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags()
    ):
        super().__init__(
            align=align,
            backgroundVisible=backgroundVisible,
            borderColor=borderColor,
            brush=brush,
            backgroundColor=backgroundColor,
            font=font,
            labelBrush=labelBrush,
            labelColor=labelColor,
            markerShape=markerShape,
            pen=pen,
            reverseMarkers=reverseMarkers,
            showToolTips=showToolTips,
            tips=tips,
            contentMargins=contentMargins,
            parent=parent,
            flags=flags
        )

@dataclass
class LineStyle:
    width : int = 1
    color : ColorTypeWithBrush = None
    style : Qt.PenStyle = Qt.SolidLine

    def toQPen(self, cap: Qt.PenCapStyle = Qt.SquareCap, join: Qt.PenJoinStyle = Qt.BevelJoin) -> QPen:
        return QPen(self.color if self.color else QColor(), self.width, self.style, cap, join)

@dataclass
class LabelStyle:
    font : Optional[FontStyle] = None
    rotate : int = 45
    color : ColorType = Qt.black
    backgroundColor : ColorTypeWithBrush = Qt.green

@dataclass
class MarkerStyle:
    shape : QLegend.MarkerShape = QLegend.MarkerShapeRectangle

@dataclass
class EffortOptions:
    theme: QChart.ChartTheme = QChart.ChartTheme.ChartThemeDark
    animationDuration: int = 1000
    animationEasingCurve: Union[QEasingCurve, QEasingCurve.Type] = QEasingCurve.OutCurve
    animationOptions: Union[QChart.AnimationOptions, QChart.AnimationOption] = QChart.AnimationOption.AllAnimations

class ChartOptions:
    def __init__(
            self,
            text: str = '',
            color: ColorType = Qt.black,
            font: Optional[FontStyle] = None,
            backgroundColor: ColorTypeWithBrush = QColor('Skyblue'),
            borderColor: ColorTypeWithPen = Qt.black,
            borderWidth: int = 10,
            borderRadius: int = 50,
            left: int = 50,
            right: int = 50,
            bottom: int = 50,
            top: int = 50,
            padding: QMarginsF = QMarginsF(50, 50, 50, 50)
    ):
        self.text = text
        self.color = color
        self.font = font
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.padding = padding

# 主题会影响Legend的配置
class LegendOptions:
    def __init__(
        self,
        align: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignTop,
        backgroundColor: ColorTypeWithBrush = QColor('skyblue'),  # legend背景颜色
        borderColor: ColorTypeWithPen = Qt.black,  # legend边框颜色
        borderWidth: int = 1,  # legend边框宽度
        font: Optional[FontStyle] = None,
        tooltip: Optional[str] = None
    ):
        self.align = align
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.font = font
        self.tooltip = tooltip

class GridOptions:
    def __init__(self, lineStyle: LineStyle = LineStyle(color=Qt.black, width=10, style=Qt.SolidLine)):
        self.lineStyle = lineStyle

class xAxis:
    def __init__(
        self,
        name: Optional[str] = 'X Value',
        type: str = 'value',
        data: Optional[Sequence] = None,
        position: Union[Qt.Alignment, Qt.AlignmentFlag, QPolarChart.PolarOrientation] = Qt.AlignBottom,  # QPolarChart.PolarOrientation仅仅提供给极坐标图
        min: Optional[float] = None,
        max: Optional[float] = None,
        interval: float = 1.0,
        lineStyle: LineStyle = LineStyle(),
        labelStyle: LabelStyle = LabelStyle()
    ):
        self.name = name
        self.type = type
        self.data = data
        self.position = position
        self.min = min
        self.max = max
        self.interval = interval
        self.lineStyle = lineStyle
        self.labelStyle = labelStyle

class yAxis(xAxis): pass

class SeriesOption:
    def __init__(
            self,
            type: Literal['line', 'pie', 'bar', 'scatter', 'boxplot', 'candlestick'] = 'line',
            name: str = '',
            data: Optional[Sequence] = None,
            color: ColorType = Qt.black,
            lineWidth: int = 5
    ):
        self.type = type
        self.name = name
        self.data = data
        self.color = color
        self.lineWidth = lineWidth

class Options:
    def __init__(
            self,
            effortOptions: EffortOptions = EffortOptions(),
            chartOptions: ChartOptions = ChartOptions(),
            # legendOptions: Optional[LegendOptions] = None,  # @bug 不提供legend的设置，除了legend-align
            legendAlign : Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignTop,
            gridOptions: GridOptions = GridOptions(
                lineStyle=LineStyle(

                )
            ),
            xAxis: xAxis = xAxis(),
            yAxis: yAxis = yAxis(),
            seriesOption: SeriesOption = SeriesOption()
    ):
        self.effortOptions = effortOptions
        self.chartOptions = chartOptions
        # self.legendOptions = legendOptions
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.gridOptions = gridOptions
        self.seriesOption = seriesOption
        self.legendAlign = legendAlign

# 备注，与xxxType、xxxStyle、xxxCfg不同的是，xxxOptions面向echarts设计的
__all__ = [
    'EffortOptions',
    'ChartOptions',
    'LegendOptions',
    'GridOptions',
    'xAxis',
    'yAxis',
    'SeriesOption',
    'Options',
    'FontStyle',
    'LegendStyle',
    'LineStyle',
    'LabelStyle',
    'SeriesBindAxesWithAligns'
]
