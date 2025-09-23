#  QChartView是容器、QChart是画布、图表是画
from typing import Optional, Union, Callable, Dict, Sequence, Iterable

from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtCore import Qt, QEasingCurve, QMargins, QLocale, QRectF, QMarginsF
from PyQt5.QtWidgets import QGraphicsItem, QWidget
from PyQt5.QtChart import QAbstractAxis, QChart, QChartView, QAbstractSeries, QPolarChart

from ..ABSW import AbstractWidget
from ..QTyping import ColorTypeWithPen, ColorTypeWithBrush

from Optimize.OptChart.ChartsOthers import FunctionalLegend as _ChartsOthers_FunctionalLegend
from Optimize.OptChart.ChartsAssistTyping import LegendStyle, SeriesBindAxesWithAligns


# QChartView <- QGraphicsView <- QAbstractScrollArea <- QFrame
class ChartContainer(QChartView, AbstractWidget):
    def __init__(self,
                 chart: Optional[QChart] = None,
                 hints: Union[
                     QPainter.RenderHints, QPainter.RenderHint
                 ] = QPainter.Antialiasing,  # 设置渲染提示,以指定绘制图形项时的一些选项和优化
                 rubberBand: Union[
                     QChartView.RubberBands, QChartView.RubberBand
                 ] = QChartView.NoRubberBand,  # 光标在图标示图控件上拖动选择框的类型
                 rubberBandSelectionMode: Qt.ItemSelectionMode = Qt.ContainsItemShape,  # 选择模式
                 viewportWidget: Optional[QWidget] = None,
                 align: Union[Qt.AlignmentFlag, Qt.Alignment] = Qt.AlignCenter,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        if chart:
            self.setChart(chart)
        if viewportWidget:
            self.setViewport(viewportWidget)

        self.setAlignment(align)
        self.setRubberBand(rubberBand)
        self.setRenderHints(hints)
        self.setRubberBandSelectionMode(rubberBandSelectionMode)

# 只对QChart浅层封装，不封装其父类
class Chart(QChart):
    def __init__(
            self,
            theme : Optional[QChart.ChartTheme] = QChart.ChartThemeQt,
            title : Optional[str] = None,
            titleBrush : ColorTypeWithBrush = None,  # 标题颜色
            titleFont : Optional[QFont] = None,
            seriesBindAxesWithAligns: Optional[Sequence[SeriesBindAxesWithAligns]] = None,
            series: Optional[Sequence[QAbstractSeries]] = None,
            # 可选的序列，包含要添加到图表中的 QAbstractSeries，也就是仅显示图表，不与轴绑定。
            axesWithAligns : Optional[Dict[QAbstractAxis, Union[Qt.AlignmentFlag, Qt.Alignment]]] = None,
            # 可选的序列，仅显示某些方向的轴，不与图表绑定。
            animationDuration: int = 1000,  # 动画持续时间，单位毫秒，默认为 1000。
            animationEasingCurve: Union[QEasingCurve, QEasingCurve.Type, None] = None,  # 动画缓和曲线类型。
            animationOptions: Union[
                QChart.AnimationOptions, QChart.AnimationOption
            ] = QChart.NoAnimation,  # 动画选项，默认为无动画。
            axisXBindSeries: Union[Dict[QAbstractAxis, QAbstractSeries], None] = None,  # 映射，将 X 轴与 QAbstractSeries 绑定。
            axisYBindSeries: Union[Dict[QAbstractAxis, QAbstractSeries], None] = None,  # 映射，将 Y 轴与 QAbstractSeries 绑定。
            backgroundBrush: ColorTypeWithBrush = None,  # 图表背景的画刷颜色。
            backgroundPen: ColorTypeWithPen = None,  # 图表背景的画笔颜色。
            backgroundRoundness: float = 1.,  # 图表背景圆角度，默认为 1。
            backgroundVisible: bool = True,  # 图表背景是否可见，默认为 True。
            dropShadowEnabled: bool = False,  # 是否启用阴影效果，默认为 False。
            graphicsItem: Optional[QGraphicsItem] = None,  # 与图表关联的可选 QGraphicsItem。
            locale: Optional[QLocale] = None,  # 用于数字格式化的区域设置。
            localizeNumbers: bool = True,  # 是否根据区域设置本地化数字，默认为 True。
            margins: Optional[Union[QMargins, Iterable]] = None,  # 图表绘图区域的边距。
            ownedByLayout: bool = True,  # 图表是否由布局拥有，默认为 True。
            plotArea: Optional[QRectF] = None,  # 定义绘图区域的矩形区域。
            plotAreaBackgroundBrush: ColorTypeWithBrush = None,  # 绘图区域背景的画刷颜色。
            plotAreaBackgroundPen: ColorTypeWithPen = None,  # 绘图区域背景的画笔颜色。
            plotAreaBackgroundVisible: bool = True,  # 绘图区域背景是否可见，默认为 True。
            tips : Optional[str] = None,
            legendSets : Union[LegendStyle, Dict, None] = None,  # 图例配置
            contentMargins: Optional[Union[QMarginsF, Iterable]] = None,  # 图表绘图内容区域的边距，相当于padding。
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setAnimationDuration(animationDuration)
        self.setAnimationOptions(animationOptions)
        self.setOwnedByLayout(ownedByLayout)
        self.setDropShadowEnabled(dropShadowEnabled)

        if legendSets:
            _ChartsOthers_FunctionalLegend(self.legend(), **legendSets)
        if tips:
            self.setToolTip(tips)
        if theme:
            self.setTheme(theme)
        if title:
            self.setTitle(title)
            if titleFont:
                self.setTitleFont(titleFont)
            if titleBrush:
                self.setTitleBrush(titleBrush)
        if seriesBindAxesWithAligns:
            for saa in seriesBindAxesWithAligns:
                self.addSeries(saa.series)
                if saa.axesWithAligns:
                    for axis_align in saa.axesWithAligns.items():
                        axis, align = axis_align
                        self.addAxis(axis, align)
                        saa.series.attachAxis(axis)
        if series:
            for s in series:
                self.addSeries(s)
        if axesWithAligns:
            for axis_align in axesWithAligns.items():
                self.addAxis(*axis_align)
        if animationEasingCurve:
            self.setAnimationEasingCurve(animationEasingCurve)
        if axisXBindSeries:
            self.setAxisX(*next(iter(axisXBindSeries.items())))
        if axisYBindSeries:
            self.setAxisX(*next(iter(axisYBindSeries.items())))
        if backgroundVisible:
            if backgroundPen:
                self.setBackgroundPen(backgroundPen)
            if backgroundBrush:
                self.setBackgroundBrush(backgroundBrush)
            self.setBackgroundRoundness(backgroundRoundness)
        if graphicsItem:
            self.setGraphicsItem(graphicsItem)
        if locale:
            self.setLocale(locale)
            self.setLocalizeNumbers(localizeNumbers)
        if margins:
            self.setMargins(margins if isinstance(margins, QMargins) else QMargins(*margins))
        if plotAreaBackgroundVisible:
            if plotArea:
                self.setPlotArea(plotArea)
            if plotAreaBackgroundPen:
                self.setPlotAreaBackgroundPen(plotAreaBackgroundPen)
            if plotAreaBackgroundBrush:
                self.setPlotAreaBackgroundBrush(plotAreaBackgroundBrush)
        if contentMargins:
            self.setContentsMargins(contentMargins if isinstance(contentMargins, QMarginsF) else QMarginsF(*contentMargins))

    # 联级调用addxxx方法比较方便
    def __call__(self, funcLike: Union[Callable, str], *args, **kwargs) -> 'Chart':
        # funcLike可以是直接函数，也可以是类域内的函数，需要传入函数名字去寻找，默认是有这个函数的，不做判断
        func: Callable = getattr(self, funcLike) if isinstance(funcLike, str) else funcLike
        value = func(*args, **kwargs)
        # @better 有返回值就打印，这里完全可以再传入一个函数参数，用于操作这个value
        print(value)
        return self

# 用于绘制极坐标图形
class PolarChart(QPolarChart, Chart):
    """
    PolarChart(
        theme : Optional[QChart.ChartTheme] = QChart.ChartThemeQt,
        title : Optional[str] = None,
        titleBrush : ColorTypeWithBrush = None,
        titleFont : Optional[QFont] = None,
        seriesBindAxesWithAligns: Optional[Sequence[SeriesBindAxesWithAligns]] = None,
        series: Optional[Sequence[QAbstractSeries]] = None,
        # 可选的序列，包含要添加到图表中的 QAbstractSeries，也就是仅显示图表，不与轴绑定。
        axesWithAligns : Optional[Dict[QAbstractAxis, Union[Qt.AlignmentFlag, Qt.Alignment]]] = None,
        series: Optional[Sequence[QAbstractSeries]] = None,  # 可选的序列，包含要添加到图表中的 QAbstractSeries。
        animationDuration: int = 1000,  # 动画持续时间，单位毫秒，默认为 1000。
        animationEasingCurve: Union[QEasingCurve, QEasingCurve.Type, None] = None,  # 动画缓和曲线类型。
        animationOptions: Union[
            QChart.AnimationOptions, QChart.AnimationOption
        ] = QChart.NoAnimation,  # 动画选项，默认为无动画。
        axisXBindSeries: Union[Dict[QAbstractAxis, QAbstractSeries], None] = None,  # 映射，将 X 轴与 QAbstractSeries 绑定。
        axisYBindSeries: Union[Dict[QAbstractAxis, QAbstractSeries], None] = None,  # 映射，将 Y 轴与 QAbstractSeries 绑定。
        backgroundBrush: ColorTypeWithBrush = None,  # 图表背景的画刷颜色。
        backgroundPen: ColorTypeWithPen = None,  # 图表背景的画笔颜色。
        backgroundRoundness: float = 1.,  # 图表背景圆角度，默认为 1。
        backgroundVisible: bool = True,  # 图表背景是否可见，默认为 True。
        dropShadowEnabled: bool = False,  # 是否启用阴影效果，默认为 False。
        graphicsItem: Optional[QGraphicsItem] = None,  # 与图表关联的可选 QGraphicsItem。
        locale: Optional[QLocale] = None,  # 用于数字格式化的区域设置。
        localizeNumbers: bool = True,  # 是否根据区域设置本地化数字，默认为 True。
        margins: Optional[Union[QMargins, Iterable]] = None,  # 图表绘图区域的边距。
        ownedByLayout: bool = True,  # 图表是否由布局拥有，默认为 True。
        plotArea: Optional[QRectF] = None,  # 定义绘图区域的矩形区域。
        plotAreaBackgroundBrush: ColorTypeWithBrush = None,  # 绘图区域背景的画刷颜色。
        plotAreaBackgroundPen: ColorTypeWithPen = None,  # 绘图区域背景的画笔颜色。
        plotAreaBackgroundVisible: bool = True,  # 绘图区域背景是否可见，默认为 True。
        tips : Optional[str] = None,
        legendSets : Union[LegendStyle, Dict, None] = None,  # 图例配置
        contentMargins: Optional[Union[QMarginsF, Iterable]]  = None,  # 图表绘图内容区域的边距，相当于padding。
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

__all__ = ['ChartContainer', 'Chart', 'PolarChart']
