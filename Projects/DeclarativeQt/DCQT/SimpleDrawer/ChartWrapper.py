import sys
import json
from collections import UserDict
from os import PathLike
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *

from SideBar import SideBar
from OptimizeQt import *
from WarpperBase import *
"""
ScatterSeries(
    borderColor : ColorType = Qt.black,
    markerShape : QScatterSeries.MarkerShape = QScatterSeries.MarkerShapeCircle,
    markerSize : float = 1.,
    points: Iterable[Union[QPoint, QPointF, List, Tuple]] | None = None,  # 数据点列表，可选
    brush: ColorTypeWithBrush = None,  # 刷子颜色类型，可选
    color: ColorType = None,  # 颜色类型，可选
    pen: ColorTypeWithPen = None,  # 画笔颜色类型，可选
    pointLabelsClipping: bool = True,  # 数据点标签是否剪切，默认为 True
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

def translatePoints(src : dict) -> Union[List[QPointF], List[List[QPointF]]]:
    xs = src['xs']
    ys = src['ys']
    get = []
    if isinstance(xs, list):
        for i in xs:
            tp = []
            yi = ys[i]
            for index, value in enumerate(xs[i]):
                tp.append(QPointF(value, yi[index]))
            get.append(tp)
    else:
        for index, value in enumerate(xs):
            get.append(QPointF(value, ys[index]))
    return get

class ScatterWrapper:
    def __init__(self, path : Union[PathLike, str]):
        settings = json.load(open(path, 'r', encoding='utf-8'))
        shape = settings['shape']
        if isinstance(shape, str):
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                series=ScatterSeries(
                    markerShape=ShapeMap[shape],
                    markerSize=settings.get('markerSize', 1.),
                    points=translatePoints(settings),
                    color=settings['color'],
                    name=settings['categories'],
                ),
                mult=False,
                theme=ChartThemeMap[settings.get('theme', 0)],
            )
        else:
            scaseries = []
            ps = translatePoints(settings)
            for i in range(len(shape)):
                scaseries.append(ScatterSeries(
                    markerShape=ShapeMap[shape[i]],
                    markerSize=settings['markerSize'][i],
                    points=ps[i],
                    color=settings['color'][i],
                    name=settings['categories'][i]
                ))
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                series=scaseries,
                mult=True,
                theme=ChartThemeMap[settings.get('theme', 0)],
            )
    @property
    def data(self) -> dict: return self.__data

class ScatterView(ChartContainer):
    def __init__(self, wrapper : dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.wrapper = wrapper
        self.chart = QChart()
        self.__setUI()

    def __setUI(self) -> None:
        self.setChart(self.chart)
        self.chart.createDefaultAxes()
        self.chart.setTheme(self.wrapper.get('theme'))
        self.chart.setTitle(self.wrapper.get('title'))

        if self.wrapper.get('mult'):
            series : List[QAbstractSeries] = self.wrapper.get('series')
            for s in series:
                self.chart.addSeries(s)
        else:
            self.chart.addSeries(self.wrapper.get('series'))


print(ScatterWrapper("../template/scatter.template.json"))