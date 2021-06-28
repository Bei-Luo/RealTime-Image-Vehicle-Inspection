import io
import json
import logging
import queue
import shlex
import time
from functools import partial
from threading import Thread

import numpy as np
import subprocess as sp


class play_video(Thread):
    """
    播放视频
    """

    def __init__(self, video_data, img, img_view1):
        """

        Args:
            img (list]):
            video_data (queue.Queue):
        """
        super(play_video, self).__init__()
        self.img_cache = queue.Queue(100)
        self.video_data = video_data
        self.img = img
        self.fps = 30
        self.img_view1 = img_view1
        # 启动播放线程
        play_t = Thread(target=self.update, daemon=True)
        play_t.start()

    def update(self, ):
        logging.debug('刷新图片线程启动')
        while True:
            self.img[0] = self.img_cache.get()
            self.img_view1.emit()
            time.sleep(1 / self.fps)

    def run(self):
        def writer():
            """
            将字节流以1024kb块的格式写入标准输入
            """
            for chunk in iter(partial(stream.read, 1024), b''):
                process.stdin.write(chunk)
            try:
                process.stdin.close()
            except BrokenPipeError:
                pass

        logging.info('开始线程-解析视频')
        while (True):
            # 使用 ffprobe 解析视频参数
            stream = io.BytesIO(self.video_data.get())
            process = sp.Popen(
                shlex.split('ffprobe -v error -i pipe: -select_streams v -print_format json -show_streams'),
                stdin=sp.PIPE, stdout=sp.PIPE, bufsize=10 ** 8)
            pthread = Thread(target=writer)
            pthread.start()
            pthread.join()
            in_bytes = process.stdout.read()
            process.wait()
            p = json.loads(in_bytes)
            try:
                width = (p['streams'][0])['width']
                height = (p['streams'][0])['height']
                self.fps = int((p['streams'][0])['r_frame_rate'].split('/')[0])
            except:
                width = 640
                height = 360
                self.fps = 50
            stream.seek(0)
            # 解析视频数据
            process = sp.Popen(shlex.split('ffmpeg -v quiet -i pipe: -f rawvideo -pix_fmt bgr24 -an -sn pipe:'),
                               stdin=sp.PIPE,
                               stdout=sp.PIPE, bufsize=10 ** 8)
            thread = Thread(target=writer)
            thread.start()
            while True:
                in_bytes = process.stdout.read(width * height * 3)
                if not in_bytes:
                    break
                in_frame = (np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3]))
                self.img_cache.put(in_frame)
            if not in_bytes:
                thread.join()
            try:
                process.wait(1)
            except (sp.TimeoutExpired):
                process.kill()
