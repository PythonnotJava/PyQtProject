from PyQt5.QtChart import *

ShapeMap = {
    'c' : QScatterSeries.MarkerShape.MarkerShapeCircle,
    'r' : QScatterSeries.MarkerShape.MarkerShapeRectangle
}

ChartThemeMap = {
    0 : QChart.ChartTheme.ChartThemeLight,
    1 : QChart.ChartTheme.ChartThemeBlueCerulean,
    2 : QChart.ChartTheme.ChartThemeDark,
    3 : QChart.ChartTheme.ChartThemeBrownSand,
    4 : QChart.ChartTheme.ChartThemeBlueNcs,
    5 : QChart.ChartTheme.ChartThemeHighContrast,
    6 : QChart.ChartTheme.ChartThemeBlueIcy,
    7 : QChart.ChartTheme.ChartThemeQt
}