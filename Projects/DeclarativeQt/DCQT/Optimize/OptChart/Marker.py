# 不同图表的数据点标记
from typing import Optional

from PyQt5.QtGui import QFont
from PyQt5.QtChart import QLegend, QLegendMarker, QXYLegendMarker, QPieLegendMarker, QAreaLegendMarker, QBoxPlotLegendMarker, QCandlestickLegendMarker, QBarLegendMarker

from ..QTyping import ColorTypeWithBrush, ColorTypeWithPen

class LegendMarker(QLegendMarker):
    def __init__(
            self,
            label: Optional[str] = None,
            labelBrush : ColorTypeWithBrush = None,
            shape : QLegend.MarkerShape = QLegend.MarkerShapeCircle,
            pen : ColorTypeWithPen = None,
            brush : ColorTypeWithBrush = None,
            font : Optional[QFont] = None,
            visible : bool = True,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setShape(shape)
        self.setVisible(visible)
        if pen:
            self.setPen(pen)
        if label:
            self.setLabel(label)
            if labelBrush:
                self.setLabelBrush(labelBrush)
        if brush:
            self.setBrush(brush)
        if font:
            self.setFont(font)

class BarLegendMarker(QBarLegendMarker, LegendMarker):
    def __init__(self, **kwargs): super().__init__(**kwargs)

class AreaLegendMarker(QAreaLegendMarker, LegendMarker):
    def __init__(self, **kwargs): super().__init__(**kwargs)

class BoxPlotLegendMarker(QBoxPlotLegendMarker, LegendMarker):
    def __init__(self, **kwargs): super().__init__(**kwargs)

class CandlestickLegendMarker(QCandlestickLegendMarker, LegendMarker):
    def __init__(self, **kwargs): super().__init__(**kwargs)

class PieLegendMarker(QPieLegendMarker, LegendMarker):
    def __init__(self, **kwargs): super().__init__(**kwargs)

class XYLegendMarker(QXYLegendMarker, LegendMarker):
    def __init__(self, **kwargs): super().__init__(**kwargs)

__all__ = [
    'LegendMarker',
    'BarLegendMarker',
    'AreaLegendMarker',
    'BoxPlotLegendMarker',
    'CandlestickLegendMarker',
    'PieLegendMarker',
    'XYLegendMarker'
]