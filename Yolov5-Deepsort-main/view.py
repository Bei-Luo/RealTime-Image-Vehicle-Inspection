import logging
import queue
import sys

import cv2
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow

from class_file.Identify_vehicle import Identify_vehicle
from class_file.get_url_video import get_url_video
from class_file.play_video import play_video
from untitled import Ui_Form


# logging.getLogger("requests").setLevel(logging.INFO)
class Signal(QObject):
    # 原视频信号
    img_view_1 = pyqtSignal()
    img_view_2 = pyqtSignal()


class MyWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # 图片窗口自适应
        # self.label_1.setScaledContents(True)
        self.label_2.setScaledContents(True)
        # 全局变量
        self.video_data = queue.Queue()
        self.img_data = queue.Queue()
        self.img = [0, 1]
        self.Signal = Signal()
        self.vehicle = {'amounts': [], 'car': 0, 'truck': 0}
        # 启动视频线程
        c = Identify_vehicle(self.img_data, self.img, self.Signal.img_view_2, self.vehicle)
        c.start()
        a = get_url_video(self.video_data)
        b = play_video(self.video_data, self.img, self.Signal.img_view_1)
        a.start()
        b.start()
        # 绑定信号
        self.Signal.img_view_1.connect(self.img_show1)
        self.Signal.img_view_2.connect(self.img_show2)
        ft=QFont()
        ft.setPointSize(20)
        self.label_4.setFont(ft)

    def img_show1(self):
        frame = self.img[0]
        if self.img_data.qsize()<1:
            self.img_data.put(frame)
        # image_height, image_width, image_depth = frame.shape  # 获取图像的高，宽以及深度。
        # QIm = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        # QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
        #              image_width * image_depth,
        #              QImage.Format_RGB888)
        # self.label_2.setPixmap(QPixmap.fromImage(QIm))  # 将QImage显示在之前创建的QLabel控件中

    def img_show2(self):
        frame = self.img[1]
        image_height, image_width, image_depth = frame.shape  # 获取图像的高，宽以及深度。
        QIm = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                     image_width * image_depth,
                     QImage.Format_RGB888)
        self.label_2.setPixmap(QPixmap.fromImage(QIm))  # 将QImage显示在之前创建的QLabel控件中


        ft=QFont()
        ft.setPointSize(20)
        ft1=QFont()
        ft1.setPointSize(20)

        amounts = self.vehicle['amounts']
        amount_1 = 0
        amount_3 = 0
        amount_5 = 0
        for i, val in enumerate(amounts):
            if i < 600:
                amount_1 += val[0]
            if i < 1800:
                amount_3 += val[0]
            if i < 3000:
                amount_5 += val[0]
        amount_3 /=3
        amount_5 /=2
        self.label.setText('累计小型车：' + str(self.vehicle['car']))
        self.label.setFont(ft)
        # self.label_4.setText('1min内经过：' + str(amount_1))
        # self.label_5.setText('3min内经过：' + str(amount_3))
        self.label_6.setText('车辆密度（辆/每分钟）：' + str(amount_5))
        self.label_6.setFont(ft1)
        amount_1 = 0
        amount_3 = 0
        amount_5 = 0
        for i, val in enumerate(amounts):
            if i < 600:
                amount_1 += val[1]
            if i < 1800:
                amount_3 += val[1]
            if i < 3000:
                amount_5 += val[1]
        amount_3 /= 3
        amount_5 /= 2
        self.label_3.setText('累计大型车：' + str(self.vehicle['truck']))
        self.label_3.setFont(ft)
        # self.label_7.setText('1min内经过：' + str(amount_1))
        # self.label_8.setText('3min内经过：' + str(amount_3))
        self.label_9.setText('车辆密度（辆/每分钟）：' + str(amount_5))
        self.label_9.setFont(ft1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
