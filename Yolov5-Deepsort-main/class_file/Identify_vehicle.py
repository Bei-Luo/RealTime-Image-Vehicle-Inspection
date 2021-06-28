import logging
import time
from threading import Thread

from AIDetector_pytorch import Detector


class Identify_vehicle(Thread):
    def __init__(self, img_data, img, img_view, vehicle):
        super(Identify_vehicle, self).__init__()
        self.img_data = img_data
        self.det = Detector()
        self.img = img
        self.img_view = img_view
        self.vehicle = vehicle

    def run(self):
        logging.info("开始线程-识别图像")
        while (True):
            im = self.img_data.get()
            amounts = self.vehicle['amounts']
            amount = [0, 0]
            t0 = time.time()
            result = self.det.feedCap(im, amount)
            t1 = time.time()
            print('经过车辆{}、{}'.format(amount[0], amount[1]) + '，识别时间{:.2f}'.format((t1 - t0) * 1000) + 'ms')
            amounts.append(amount)
            while len(amounts) > 1200:
                amounts = amounts[1:]
            # print(amount)
            self.vehicle['amounts'] = amounts
            self.vehicle['car'] += amount[0]
            self.vehicle['truck'] += amount[1]
            self.img[1] = result['frame']
            self.img_view.emit()
