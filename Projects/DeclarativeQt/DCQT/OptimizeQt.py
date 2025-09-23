# Python's edition must be no less than 3.12!

# Basic Types & some constants
from Optimize.QTyping import (
    WidgetOrLayoutType,
    IconWithStringType,
    TabCfgType,
    ButtonStateQssSimpleGenerator,
    ColorTypeWithPen,
    ColorType,
    ColorTypeWithBrush
)
from Optimize.QConst import QColorSkyblue, QColorLightskyblue, QColorTan
from Optimize.OptChart.ChartsAssistTyping import (
    FontStyle,
    LegendStyle,
    LineStyle,
    LabelStyle,
    SeriesBindAxesWithAligns
)

# Optimized Widgets
from Optimize.ABSW import AbstractWidget, OptApplication
from Optimize.OptLabel import OptLabel, CircleAvatar
from Optimize.OptLayout import SimpleGrid, SizedBox, Row, Column
from Optimize.OptButton import Switch, OptToolButton, OptPushButton, FlashButton, TextButton
from Optimize.OptDlg import OptDlg, InputDialog
from Optimize.OptSlider import OptSlider
from Optimize.OptInput import OptTextEdit, OptLineEdit, PwdEdit, UnderlineEdit
from Optimize.OptComboBox import OptComboBox, DropButtonComboBox
from Optimize.OptSplitter import OptSplitter
from Optimize.PartingLine import PartingLine
from Optimize.Navigator import OptTabWidget, AppBar, ButtonGroupWidget
from Optimize.Container import Stack, Group, ScrollArea
from Optimize.OptMenuSeries import OptSeparator, OptMenuBar, OptMenu, OptAction
from Optimize.OptChart.Charts import ChartContainer, Chart, PolarChart
from Optimize.OptChart.Axis import AbsAxis, ValueAxis, DateTimeAxis, LogValueAxis, BarCategoryAxis, CategoryAxis
from Optimize.OptChart.Series import (
    AbsSeries,
    AbsBarSeries,
    VBarSeries,
    HPercentBarSeries,
    HBarSeries,
    VPercentBarSeries,
    HStackedBarSeries,
    VStackedBarSeries,
    XYSeries,
    LineSeries,
    ScatterSeries,
    SplineSeries,
    PieSeries,
    BoxPlotSeries,
    CandlestickSeries,
    AreaSeries
)
from Optimize.OptChart.Marker import (
    LegendMarker,
    CandlestickLegendMarker,
    AreaLegendMarker,
    PieLegendMarker,
    BarLegendMarker,
    BoxPlotLegendMarker,
    XYLegendMarker
)
from Optimize.OptChart.ChartsOthers import Legend, BoxSet, BarSet, CandlestickSet, PieSlice, FunctionalLegend
from Optimize.OptChart.ChartsAssistTyping import EffortOptions, ChartOptions, LegendOptions, GridOptions, xAxis, yAxis, SeriesOption, Options

# ThirdParties
from Optimize.OptMatplotlib import MatplotlibQtFigure