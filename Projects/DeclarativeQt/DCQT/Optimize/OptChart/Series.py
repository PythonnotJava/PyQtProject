# 图表系列
from typing import Union, Optional, List, Callable, Tuple, Iterable

from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtChart import (
    QAbstractAxis,
    QAbstractSeries,
    QBarSeries,
    QBarSet,
    QXYSeries,
    QAbstractBarSeries,
    QHorizontalPercentBarSeries,
    QHorizontalStackedBarSeries,
    QPieSeries,
    QStackedBarSeries,
    QLineSeries,
    QPercentBarSeries,
    QScatterSeries,
    QSplineSeries,
    QCandlestickSeries,
    QPieSlice,
    QBoxSet,
    QCandlestickSet,
    QAreaSeries,
    QBoxPlotSeries
)

from ..QTyping import ColorType, ColorTypeWithPen, ColorTypeWithBrush

# 抽象图表
class AbsSeries(QAbstractSeries):
    def __init__(
            self,
            objectName: Optional[str] = None,
            name: Optional[str] = None,
            bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
            opacity : float = 1.,
            useOpenGL : bool = True,
            visible : bool = True,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setVisible(visible)
        self.setOpacity(opacity)
        self.setUseOpenGL(useOpenGL)

        if objectName:
            self.setObjectName(objectName)
        if name:
            self.setName(name)
        if isinstance(bindAxes, QAbstractAxis):
            self.attachAxis(bindAxes)
        elif isinstance(bindAxes, List):
            for axis in bindAxes:
                self.attachAxis(axis)
        else:
            pass

    def __call__(self, funcLike: Union[Callable, str], *args, **kwargs) -> 'AbsSeries':
        # funcLike可以是直接函数，也可以是类域内的函数，需要传入函数名字去寻找，默认是有这个函数的，不做判断
        func: Callable = getattr(self, funcLike) if isinstance(funcLike, str) else funcLike
        value = func(*args, **kwargs)
        # @better 有返回值就打印，这里完全可以再传入一个函数参数，用于操作这个value
        print(value)
        return self

    # @bug 调用属性下的方法--有问题
    def callPropertyFunc(self, name : str, funcLike : Union[Callable, str], *args, **kwargs) -> 'AbsSeries':
        p_func : Callable = getattr(getattr(self, name), funcLike) if isinstance(funcLike, str) else funcLike
        value = p_func(*args, **kwargs)
        print(value)
        return self

# 抽象条形图图表
class AbsBarSeries(QAbstractBarSeries, AbsSeries):
    """
    AbsBarSeries(
        barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
        barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
        labelsAngle: float = 90,  # 标签的角度，默认为 90 度
        labelsFormat: Optional[str] = None,  # 标签的格式，可选
        labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
        labelsPrecision: Optional[int] = None,  # 标签的精度，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(
            self,
            barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
            barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
            labelsAngle: float = 90,  # 标签的角度，默认为 90 度
            labelsFormat: Optional[str] = None,  # 标签的格式，可选
            labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
            labelsPrecision: Optional[int] = None,  # 标签的精度，可选
            labelsVisible: bool = True,  # 标签是否可见，默认为 True
            **kwargs
    ):
        super().__init__(**kwargs)

        if barSets:
            self.append(barSets)
        if barWidth:  # 考虑后续可能在添加柱子，因此不写在if barSets下
            self.setBarWidth(barWidth)
        if labelsVisible:
            self.setLabelsAngle(labelsAngle)
            if labelsPrecision:
                self.setLabelsPrecision(labelsPrecision)
            if labelsPosition:
                self.setLabelsPosition(labelsPosition)
            if labelsFormat:
                self.setLabelsFormat(labelsFormat)

# QBarSeries 用于创建条形图系列，支持将多个条形图数据添加到同一个系列中。
# QStackedBarSeries 用于创建堆叠条形图系列，条形图中的每个条块会堆叠在前一个条块之上。
# QPercentBarSeries 用于创建百分比堆叠条形图系列，条形图中的每个条块的高度按其在总高度中的百分比显示。
# QHorizontalBarSeries 类似于 QBarSeries，但条形图是水平显示的。
# QHorizontalStackedBarSeries 类似于 QStackedBarSeries，但条形图是水平堆叠的。
# QHorizontalPercentBarSeries 类似于 QPercentBarSeries，但条形图是水平显示的。

# 纵向多个条形图
class VBarSeries(QBarSeries, AbsBarSeries):
    """
    VBarSeries(
        barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
        barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
        labelsAngle: float = 90,  # 标签的角度，默认为 90 度
        labelsFormat: Optional[str] = None,  # 标签的格式，可选
        labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
        labelsPrecision: Optional[int] = None,  # 标签的精度，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 横向多个条形图
class HBarSeries(QHorizontalPercentBarSeries, AbsBarSeries):
    """
    HBarSeries(
        barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
        barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
        labelsAngle: float = 90,  # 标签的角度，默认为 90 度
        labelsFormat: Optional[str] = None,  # 标签的格式，可选
        labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
        labelsPrecision: Optional[int] = None,  # 标签的精度，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 纵向堆叠条形图
class VStackedBarSeries(QStackedBarSeries, AbsBarSeries):
    """
    VStackedBarSeries(
        barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
        barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
        labelsAngle: float = 90,  # 标签的角度，默认为 90 度
        labelsFormat: Optional[str] = None,  # 标签的格式，可选
        labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
        labelsPrecision: Optional[int] = None,  # 标签的精度，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 横向堆叠条形图
class HStackedBarSeries(QHorizontalStackedBarSeries, AbsBarSeries):
    """
    HStackedBarSeries(
        barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
        barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
        labelsAngle: float = 90,  # 标签的角度，默认为 90 度
        labelsFormat: Optional[str] = None,  # 标签的格式，可选
        labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
        labelsPrecision: Optional[int] = None,  # 标签的精度，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 纵向百分比堆叠条形图
class VPercentBarSeries(QPercentBarSeries, AbsBarSeries):
    """
    VPercentBarSeries(
        barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
        barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
        labelsAngle: float = 90,  # 标签的角度，默认为 90 度
        labelsFormat: Optional[str] = None,  # 标签的格式，可选
        labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
        labelsPrecision: Optional[int] = None,  # 标签的精度，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 横向百分比堆叠条形图
class HPercentBarSeries(QHorizontalPercentBarSeries, AbsBarSeries):
    """
    HPercentBarSeries(
        barSets: Union[QBarSet, List[QBarSet], None] = None,  # 条形图数据集，可选
        barWidth: float = 0.5,  # 条形的宽度，默认为 0.5
        labelsAngle: float = 90,  # 标签的角度，默认为 90 度
        labelsFormat: Optional[str] = None,  # 标签的格式，可选
        labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,  # 标签的位置，可选
        labelsPrecision: Optional[int] = None,  # 标签的精度，可选
        labelsVisible: bool = True,  # 标签是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 用于表示包含 (x, y) 数据点的图表系列。它为具体的 (x, y) 数据系列类型（如折线图和散点图）提供了基础功能。
class XYSeries(QXYSeries, AbsSeries):
    """
    XYSeries(
        points: Iterable[Union[QPoint, QPointF, List, Tuple]] | None = None,  # 数据点列表，可选
        brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
        color: ColorType = None,  # 颜色类型，可选
        pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
        pointLabelsClipping: bool = False,  # 数据点标签是否剪切，默认为 False
        pointLabelsColor: ColorType = Qt.black,  # 数据点标签颜色，默认为黑色
        pointLabelsFont: Optional[QFont] = None,  # 数据点标签字体，可选
        pointLabelsFormat: Optional[str] = None,  # 数据点标签格式，可选
        pointLabelsVisible: bool = True,  # 数据点标签是否可见，默认为 True
        pointsVisible: bool = True,  # 数据点是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(
            self,
            points: Iterable[Union[QPoint, QPointF, List, Tuple]] | None = None,  # 数据点列表，可选
            brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
            color: ColorType = None,  # 颜色类型，可选
            pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
            pointLabelsClipping: bool = False,  # 数据点标签是否剪切，默认为 False
            pointLabelsColor: ColorType = Qt.black,  # 数据点标签颜色，默认为黑色
            pointLabelsFont: Optional[QFont] = None,  # 数据点标签字体，可选
            pointLabelsFormat: Optional[str] = None,  # 数据点标签格式，可选
            pointLabelsVisible: bool = True,  # 数据点标签是否可见，默认为 True
            pointsVisible: bool = True,  # 数据点是否可见，默认为 True
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setPointsVisible(pointsVisible)

        if points:
            if isinstance(next(iter(points)), (QPointF, QPoint)):
                self.append(points)
            else:
                self.append(QPointF(*pt) for pt in points)
        if pointLabelsVisible:
            self.setPointLabelsClipping(pointLabelsClipping)
            if pointLabelsFont:
                self.setPointLabelsFont(pointLabelsFont)
            if pointLabelsFormat:
                self.setPointLabelsFormat(pointLabelsFormat)
            if pointLabelsColor:
                self.setPointLabelsColor(pointLabelsColor)
        if pen:
            self.setPen(pen)
        if color:
            self.setColor(color)
        if brush:
            self.setBrush(brush)

# 折线图
class LineSeries(QLineSeries, XYSeries):
    """
    LineSeries(
        points: Iterable[Union[QPoint, QPointF, List, Tuple]] | None = None,  # 数据点列表，可选
        brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
        color: ColorType = None,  # 颜色类型，可选
        pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
        pointLabelsClipping: bool = False,  # 数据点标签是否剪切，默认为 False
        pointLabelsColor: ColorType = Qt.black,  # 数据点标签颜色，默认为黑色
        pointLabelsFont: Optional[QFont] = None,  # 数据点标签字体，可选
        pointLabelsFormat: Optional[str] = None,  # 数据点标签格式，可选
        pointLabelsVisible: bool = True,  # 数据点标签是否可见，默认为 True
        pointsVisible: bool = True,  # 数据点是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 散点图
class ScatterSeries(QScatterSeries, XYSeries):
    """
    ScatterSeries(
        borderColor : ColorType = Qt.black,
        markerShape : QScatterSeries.MarkerShape = QScatterSeries.MarkerShapeCircle,
        markerSize : float = 10.,
        points: Iterable[Union[QPoint, QPointF, List, Tuple]] | None = None,  # 数据点列表，可选
        brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
        color: ColorType = None,  # 颜色类型，可选
        pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
        pointLabelsClipping: bool = False,  # 数据点标签是否剪切，默认为 False
        pointLabelsColor: ColorType = Qt.black,  # 数据点标签颜色，默认为黑色
        pointLabelsFont: Optional[QFont] = None,  # 数据点标签字体，可选
        pointLabelsFormat: Optional[str] = None,  # 数据点标签格式，可选
        pointLabelsVisible: bool = True,  # 数据点标签是否可见，默认为 True
        pointsVisible: bool = True,  # 数据点是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(
            self,
            borderColor : ColorType = Qt.black,
            markerShape : QScatterSeries.MarkerShape = QScatterSeries.MarkerShapeCircle,
            markerSize : float = 10.,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setMarkerSize(markerSize)
        self.setMarkerShape(markerShape)
        if borderColor:
            self.setBorderColor(borderColor)

# 平滑曲线图
class SplineSeries(QSplineSeries, XYSeries):
    """
    SplineSeries(
        points: Iterable[Union[QPoint, QPointF, List, Tuple]] | None = None,  # 数据点列表，可选
        brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
        color: ColorType = None,  # 颜色类型，可选
        pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
        pointLabelsClipping: bool = False,  # 数据点标签是否剪切，默认为 False
        pointLabelsColor: ColorType = Qt.black,  # 数据点标签颜色，默认为黑色
        pointLabelsFont: Optional[QFont] = None,  # 数据点标签字体，可选
        pointLabelsFormat: Optional[str] = None,  # 数据点标签格式，可选
        pointLabelsVisible: bool = True,  # 数据点标签是否可见，默认为 True
        pointsVisible: bool = True,  # 数据点是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(self, **kwargs): super().__init__(**kwargs)

# 用于绘制蜡烛图（K 线图）的类
class CandlestickSeries(QCandlestickSeries, AbsSeries):
    """
    CandlestickSeries(
        candlestickSet: Union[
            QCandlestickSet, Iterable[QCandlestickSet], None
        ] = None,  # 蜡烛图数据集，可以是单个或可迭代的 QCandlestickSet
        bodyOutlineVisible: bool = True,  # 是否显示蜡烛图柱体轮廓，默认为 True
        bodyWidth: float = 1.,  # 蜡烛图柱体宽度，默认为 1
        brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
        capsVisible: bool = True,  # 是否显示蜡烛图顶部和底部的线帽，默认为 True
        capsWidth: float = 1.,  # 蜡烛图顶部和底部线帽的宽度，默认为 1
        decreasingColor: ColorType = Qt.black,  # 蜡烛图下跌柱体的颜色，默认为黑色
        increasingColor: ColorType = Qt.green,  # 蜡烛图上涨柱体的颜色，默认为绿色
        maximumColumnWidth: float = 1.,  # 柱体的最大宽度，默认为 1
        minimumColumnWidth: float = 1.,  # 柱体的最小宽度，默认为 1
        pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes: Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity: float = 1.,
        useOpenGL: bool = True,
        visible: bool = True,
        **kwargs
    )
    """
    def __init__(
            self,
            candlestickSet: Union[
                QCandlestickSet, Iterable[QCandlestickSet], None
            ] = None,  # 蜡烛图数据集，可以是单个或可迭代的 QCandlestickSet
            bodyOutlineVisible: bool = True,  # 是否显示蜡烛图柱体轮廓，默认为 True
            bodyWidth: float = 1.,  # 蜡烛图柱体宽度，默认为 1
            brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
            capsVisible: bool = True,  # 是否显示蜡烛图顶部和底部的线帽，默认为 True
            capsWidth: float = 1.,  # 蜡烛图顶部和底部线帽的宽度，默认为 1
            decreasingColor: ColorType = Qt.black,  # 蜡烛图下跌柱体的颜色，默认为黑色
            increasingColor: ColorType = Qt.green,  # 蜡烛图上涨柱体的颜色，默认为绿色
            maximumColumnWidth: float = 1.,  # 柱体的最大宽度，默认为 1
            minimumColumnWidth: float = 1.,  # 柱体的最小宽度，默认为 1
            pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setBodyOutlineVisible(bodyOutlineVisible)
        self.setBodyWidth(bodyWidth)
        self.setMaximumColumnWidth(maximumColumnWidth)
        self.setMinimumColumnWidth(minimumColumnWidth)

        if decreasingColor:
            self.setDecreasingColor(decreasingColor)
        if increasingColor:
            self.setIncreasingColor(increasingColor)
        if candlestickSet:
            self.append(candlestickSet)
        if brush:
            self.setBrush(brush)
        if capsVisible:
            self.setCapsWidth(capsWidth)
        if pen:
            self.setPen(pen)

# 饼状图
class PieSeries(QPieSeries, AbsSeries):
    """
    PieSeries(
        pieSlices: Union[
            QPieSlice, Iterable[QPieSlice], None
        ] = None,  # 饼图切片数据集，可以是单个或可迭代的 QPieSlice，默认为 None。
        holeSize: float = 1.,  # 饼图中心空洞的大小，范围为 0 到 1，默认为 1（无空洞）。
        horizontalPosition: float = 1.,  # 饼图水平位置，默认为 1。
        verticalPosition: float = 1.,  # 饼图垂直位置，默认为 1。
        labelsPosition: QPieSlice.LabelPosition = QPieSeries.LabelInsideHorizontal,
        # 饼图切片标签位置，默认为 QPieSeries.LabelInsideHorizontal。
        labelsVisible: bool = True,  # 饼图切片标签是否可见，默认为 True。
        pieEndAngle: float = 0.,  # 饼图结束角度，以度为单位，默认为 0。
        pieSize: float = 1.,  # 饼图大小，相对于默认大小的比例，默认为 1。
        pieStartAngle: float = 0.,  # 饼图起始角度，以度为单位，默认为 0。
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes : Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity : float = 1.,
        useOpenGL : bool = True,
        visible : bool = True,
        **kwargs
    )
    """
    def __init__(
            self,
            pieSlices: Union[
                QPieSlice, Iterable[QPieSlice], None
            ] = None,  # 饼图切片数据集，可以是单个或可迭代的 QPieSlice，默认为 None。
            holeSize: float = 1.,  # 饼图中心空洞的大小，范围为 0 到 1，默认为 1（无空洞）。
            horizontalPosition: float = 1.,  # 饼图水平位置，默认为 1。
            verticalPosition: float = 1.,  # 饼图垂直位置，默认为 1。
            labelsPosition: QPieSlice.LabelPosition = QPieSlice.LabelInsideNormal,
            # 饼图切片标签位置，默认为 QPieSeries.LabelInsideHorizontal。
            labelsVisible: bool = True,  # 饼图切片标签是否可见，默认为 True。
            pieEndAngle: float = 0.,  # 饼图结束角度，以度为单位，默认为 0。
            pieSize: float = 1.,  # 饼图大小，相对于默认大小的比例，默认为 1。
            pieStartAngle: float = 0.,  # 饼图起始角度，以度为单位，默认为 0。
            **kwargs
    ):
        super().__init__(**kwargs)
        if pieSlices:
            self.append(pieSlices)
        if labelsVisible:
            self.setLabelsPosition(labelsPosition)

        self.setHoleSize(holeSize)
        self.setHorizontalPosition(horizontalPosition)
        self.setVerticalPosition(verticalPosition)
        self.setPieEndAngle(pieEndAngle)
        self.setPieSize(pieSize)
        self.setPieStartAngle(pieStartAngle)

# 用于创建面积图的类
class AreaSeries(QAreaSeries, AbsSeries):
    """
    AreaSeries(
        borderColor: ColorType = Qt.black,  # 边界线颜色，默认为黑色
        brush: ColorTypeWithBrush = None,  # 填充区域的画刷颜色类型，可选
        color: ColorType = QColor('skyblue'),  # 区域颜色，默认为天蓝色
        lowerSeries: Optional[QLineSeries] = None,  # 下边界系列，可以是 QLineSeries 实例或 None
        upperSeries: Optional[QLineSeries] = None,  # 上边界系列，可以是 QLineSeries 实例或 None
        pen: ColorTypeWithPen = None,  # 用于绘制边界线的画笔颜色类型，可选
        pointLabelsClipping: bool = False,  # 数据点标签是否剪切，默认为 False
        pointLabelsColor: ColorType = Qt.black,  # 数据点标签颜色，默认为黑色
        pointLabelsFont: Optional[QFont] = None,  # 数据点标签字体，可选
        pointLabelsFormat: Optional[str] = None,  # 数据点标签格式，可选
        pointLabelsVisible: bool = True,  # 数据点标签是否可见，默认为 True
        pointsVisible: bool = True,  # 数据点是否可见，默认为 True
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes: Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity: float = 1.,
        useOpenGL: bool = True,
        visible: bool = True,
        **kwargs
    )
    """
    def __init__(
            self,
            borderColor: ColorType = Qt.black,  # 边界线颜色，默认为黑色
            brush: ColorTypeWithBrush = None,  # 填充区域的画刷颜色类型，可选
            color: ColorType = QColor('skyblue'),  # 区域颜色，默认为天蓝色
            lowerSeries: Optional[QLineSeries] = None,  # 下边界系列，可以是 QLineSeries 实例或 None
            upperSeries: Optional[QLineSeries] = None,  # 上边界系列，可以是 QLineSeries 实例或 None
            pen: ColorTypeWithPen = None,  # 用于绘制边界线的画笔颜色类型，可选
            pointLabelsClipping: bool = False,  # 数据点标签是否剪切，默认为 False
            pointLabelsColor: ColorType = Qt.black,  # 数据点标签颜色，默认为黑色
            pointLabelsFont: Optional[QFont] = None,  # 数据点标签字体，可选
            pointLabelsFormat: Optional[str] = None,  # 数据点标签格式，可选
            pointLabelsVisible: bool = True,  # 数据点标签是否可见，默认为 True
            pointsVisible: bool = True,  # 数据点是否可见，默认为 True
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setPointsVisible(pointsVisible)

        if color:
            self.setColor(color)
        if borderColor:
            self.setBorderColor(borderColor)
        if pen:
            self.setPen(pen)
        if brush:
            self.setBrush(brush)
        if lowerSeries:
            self.setLowerSeries(lowerSeries)
        if upperSeries:
            self.setUpperSeries(upperSeries)
        if pointLabelsVisible:
            self.setPointLabelsClipping(pointLabelsClipping)
            if pointLabelsColor:
                self.setPointLabelsColor(pointLabelsColor)
            if pointLabelsFont:
                self.setPointLabelsFont(pointLabelsFont)
            if pointLabelsFormat:
                self.setPointLabelsFormat(pointLabelsFormat)

# 用于创建箱线图系列的类。箱线图（又称盒须图）
class BoxPlotSeries(QBoxPlotSeries, AbsSeries):
    """
    BoxPlotSeries(
        boxSet: Union[QBoxSet, Iterable[QBoxSet], None] = None,  # 箱线图数据集，可以是单个或可迭代的 QBoxSet
        boxOutlineVisible: bool = True,  # 是否显示箱线图轮廓，默认为 True
        boxWidth: float = 1.0,  # 箱线图宽度，默认为 1.0
        brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
        pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
        objectName: Optional[str] = None,
        name: Optional[str] = None,
        bindAxes: Union[QAbstractAxis, List[QAbstractAxis], None] = None,
        opacity: float = 1.,
        useOpenGL: bool = True,
        visible: bool = True,
        **kwargs
    )
    """
    def __init__(
            self,
            boxSet: Union[QBoxSet, Iterable[QBoxSet], None] = None,  # 箱线图数据集，可以是单个或可迭代的 QBoxSet
            boxOutlineVisible: bool = True,  # 是否显示箱线图轮廓，默认为 True
            boxWidth: float = 1.0,  # 箱线图宽度，默认为 1.0
            brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
            pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
            **kwargs
    ):
        super().__init__(**kwargs)

        self.setBoxWidth(boxWidth)
        self.setBoxOutlineVisible(boxOutlineVisible)
        if boxSet:
            self.append(boxSet)
        if brush:
            self.setBrush(brush)
        if pen:
            self.setPen(pen)

__all__ = [
    'AbsSeries',
    'AbsBarSeries',
    'VBarSeries',
    'HBarSeries',
    'VStackedBarSeries',
    'HStackedBarSeries',
    'HPercentBarSeries',
    'VPercentBarSeries',
    'XYSeries',
    'LineSeries',
    'ScatterSeries',
    'SplineSeries',
    'CandlestickSeries',
    'PieSeries',
    'AreaSeries',
    'BoxPlotSeries'
]