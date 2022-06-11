import MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui
from qt_material import apply_stylesheet
import qtawesome as qta
import cv2
import time
import os


class Main(QMainWindow):
    def __init__(self):
        # 窗口移动
        self._startPos = None
        self._endPos = None
        self._isTracking = None

        self.app = QApplication(sys.argv)
        super().__init__()
        self.Window = self.window()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self.Window)

        self.set_window_style()
        self.set_icon()
        self.button_connect()

        self.Window.show()
        sys.exit(self.app.exec_())

    def set_window_style(self):
        apply_stylesheet(self.app, theme='dark_teal.xml')
        self.Window.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def set_icon(self):
        self.ui.close.setIcon(qta.icon('fa.close', color="white"))
        self.ui.max.setIcon(qta.icon('fa.window-maximize', color="white"))
        self.ui.min.setIcon(qta.icon('fa.window-minimize', color='white'))

    def button_connect(self):
        self.ui.close.clicked.connect(lambda: self.exit_window())
        self.ui.max.clicked.connect(lambda: self.max_windows())
        self.ui.min.clicked.connect(lambda: self.min_window())
        self.ui.save_path_button.clicked.connect(lambda: self.save_file())
        self.ui.rec_begin_button.clicked.connect(lambda: self.begin_rec())

    # ————————————————
    # 版权声明：本文为CSDN博主「幸福的达哥」的原创文章，遵循CC
    # 4.0
    # BY - SA版权协议，转载请附上原文出处链接及本声明。
    # 原文链接：https: // blog.csdn.net / zh6526157 / article / details / 121632182
    def save_file(self):
        path = QFileDialog.getSaveFileName(self, '请选择保存位置', './', "视频文件 (*.{});;All Files (*)".format('mp4'))
        if path[0]:
            self.ui.file_path_input.setText(path[0])
            print('选择的保存位置为：{}'.format(path[0]))

    def begin_rec(self):
        if self.ui.file_path_input.text():
            my_camera = cv2.VideoCapture(0)
            my_camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.ui.width_input.value())
            my_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.ui.height_input.value())

            frame_size = (int(my_camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(my_camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            frame_fps = self.ui.FPS_input.value()
            video_format = cv2.VideoWriter_fourcc(*'mpeg')

            video_file_fp = cv2.VideoWriter()
            video_file_fp.open(self.ui.file_path_input.text(), video_format, frame_fps, frame_size, True)

            print('Start to record video')

        else:
            # https://blog.csdn.net/weixin_47406082/article/details/122803143
            QMessageBox.information(self, "提示", "需要填写文件路径",
                                    QMessageBox.Yes)  # 最后的Yes表示弹框的按钮显示为Yes，默认按钮显示为OK,不填QMessageBox.Yes即为默认

        while True:
            success, video_frame = my_camera.read()
            video_file_fp.write(video_frame)
            cv2.imshow('frame', video_frame)

            if cv2.waitKey(1) & 0xff == 27:  # esc key
                break

        video_file_fp.release()
        my_camera.release()
        cv2.destroyAllWindows()

    def exit_window(self):
        sys.exit(self.app.exec_())

    def max_windows(self):
        if self.Window.isMaximized():
            self.Window.showNormal()
        else:
            self.Window.showMaximized()

    def min_window(self):
        self.Window.showMinimized()

    # https://www.yumefx.com/?p=2019 移动窗口
    # 鼠标移动事件
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            # 移动窗口
            self.move(self.pos() + self._endPos)

    # 鼠标按下事件
    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        # 根据鼠标按下时的位置判断是否在QFrame范围内
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "centralwidget":
            # 判断鼠标按下的是左键
            if a0.button() == QtCore.Qt.LeftButton:
                self._isTracking = True
                # 记录初始位置
                self._startPos = QtCore.QPoint(a0.x(), a0.y())

    # 鼠标松开事件
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "centralwidget":
            if a0.button() == QtCore.Qt.LeftButton:
                self.max_windows()


if __name__ == '__main__':
    main = Main()
