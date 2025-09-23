import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QScatterSeries, QValueAxis

class ScatterPlot(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("多类别散点图")
        self.setGeometry(100, 100, 800, 600)

        # 创建主窗口和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # 创建图表
        self.chart = QChart()
        self.chart.setTitle("多类别散点图")

        # 创建多个散点系列
        categories = ['类别 A', '类别 B', '类别 C']
        colors = ['red', 'green', 'blue']

        for i, category in enumerate(categories):
            series = QScatterSeries()
            series.setName(category)
            series.setMarkerSize(10)

            # 添加随机数据点
            for j in range(10):
                x = j + i * 10
                y = j + (i * 5)
                series.append(x, y)

            series.setColor(QColor(colors[i]))
            self.chart.addSeries(series)

        # 设置坐标轴
        self.chart.createDefaultAxes()
        # self.chart.setAxisX(QValueAxis(), series)
        # self.chart.setAxisY(QValueAxis(), series)

        # 创建图表视图
        chart_view = QChartView(self.chart)
        layout.addWidget(chart_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScatterPlot()
    window.show()
    sys.exit(app.exec_())
