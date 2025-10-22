import sys
import asyncio
from typing import Callable, Awaitable, Any
from PySide6.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QWidget, QProgressBar
)
from PySide6.QtCore import QObject, Signal, Slot, QTimer
from qasync import QEventLoop
from enum import Enum

class FutureRunner(QObject):
    finished = Signal(object, object)  # (result, error)

    def __init__(self, future_func: Callable[[], Awaitable[Any]]):
        super().__init__()
        self.future_func = future_func

    def run(self):
        # ✅ 此时事件循环已启动
        asyncio.create_task(self._execute())

    async def _execute(self):
        try:
            result = await self.future_func()
            self.finished.emit(result, None)
        except Exception as e:
            self.finished.emit(None, e)

class FutureSnapshot(Enum):
    waiting = 0x1
    done = 0x2
    error = 0x3

class FutureBuilder(QWidget):
    """
    类似 Flutter 的 FutureBuilder：
      - 参数：future_func（异步函数）
      - 参数：builder(state, data, error)
        state: FutureSnapshot 'waiting' | 'done' | 'error'
    """

    def __init__(
        self,
        future_func: Callable[[], Awaitable[Any]],
        builder: Callable[[FutureSnapshot, Any, Exception | None], QWidget],
        parent=None
    ):
        super().__init__(parent)
        self.future_func = future_func
        self.builder = builder

        self._layout = QVBoxLayout(self)
        self._content_widget = None
        self._set_state(FutureSnapshot.waiting)

        # ✅ 延迟启动，确保事件循环已运行
        QTimer.singleShot(0, self._run_future)

    def _set_state(self, state: FutureSnapshot, data=None, error=None):
        """刷新 UI"""
        if self._content_widget:
            self._layout.removeWidget(self._content_widget)
            self._content_widget.deleteLater()

        self._content_widget = self.builder(state, data, error)
        self._layout.addWidget(self._content_widget)

    def _run_future(self):
        runner = FutureRunner(self.future_func)
        runner.finished.connect(self._on_finished)
        runner.run()

    @Slot(object, object)
    def _on_finished(self, result, error):
        if error:
            self._set_state(FutureSnapshot.error, None, error)
        else:
            self._set_state(FutureSnapshot.done, result, None)


# =============== 示例使用 ===============
class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FutureBuilder 示例")

        async def fetch_data():
            await asyncio.sleep(2)
            # raise ValueError("出错了")
            return "✅ 数据加载成功！"

        def builder(state: FutureSnapshot, data: Any, error: Exception | None) -> QWidget:
            """根据状态构建不同 UI"""
            w = QWidget()
            vbox = QVBoxLayout(w)
            label = QLabel()

            if state == FutureSnapshot.waiting:
                label.setText("⏳ 加载中...")
                bar = QProgressBar()
                bar.setRange(0, 0)
                vbox.addWidget(label)
                vbox.addWidget(bar)
            elif state == FutureSnapshot.done:
                label.setText(str(data))
                vbox.addWidget(label)
            else:
                label.setText(f"❌ 错误：{error}")
                vbox.addWidget(label)

            return w

        layout = QVBoxLayout(self)
        fb = FutureBuilder(fetch_data, builder)
        layout.addWidget(fb)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    win = DemoWindow()
    win.resize(300, 150)
    win.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
