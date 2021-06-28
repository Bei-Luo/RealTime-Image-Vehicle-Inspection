import logging
import queue
import time
import warnings
from threading import Thread
import requests
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)
"""
http://streaming.macaudsat.com/traffic/15a.m3u8
http://streaming.macaudsat.com/traffic/
http://202.175.183.27/cam/live/4001.m3u8
http://202.175.183.27/cam/live/
"""
class get_url_video(Thread):
    """
    获取视频数据
    """

    def __init__(self, video_data):
        """

        Args:
            video_data (queue.Queue):
        """
        super(get_url_video, self).__init__()
        self.video_data = video_data

    def run(self):
        logging.info("开始线程-获取视频数据")
        video_url_queue = queue.Queue()
        self.video_data.maxsize = 3
        mark = ''
        url = 'http://202.175.183.27/cam/live/4001.m3u8'
        video_url = 'http://202.175.183.27/cam/live/'
        fresh_index = 0
        used_index = 0
        while (True):
            all_content = requests.get(url).text
            file_line = all_content.split("\n")
            for line in file_line:
                if 'EXT-X-MEDIA-SEQUENCE' in line:
                    fresh_index = line[22:]
                    break
            # 维护视频地址队列
            if used_index != fresh_index:
                used_index = fresh_index
                lines = []
                for index, line in enumerate(file_line):
                    if "EXTINF" in line:
                        lines.append(video_url + file_line[index + 1])
                if mark != '':
                    lines = lines[lines.index(mark) + 1:]
                for line in lines:
                    logging.debug('获取的视频地址:' + line)
                    video_url_queue.put(line.replace('\r',''))
                mark = lines[-1]
            if video_url_queue.qsize() > 20:
                logging.warning("地址数超标 " + str(video_url_queue.qsize()))
            # 维持视频数据队列

            while not self.video_data.full():
                res = requests.get(video_url_queue.get())
                self.video_data.put(res.content)
            time.sleep(0.5)
