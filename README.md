# RealTime-Image-Vehicle-Inspection

整体项目是专业实训的课设。

## 项目说明

实时车辆检测和车流监测

实时数据的来源于：澳门交通事务局(DSAT)的[即时路面](http://www.dsat.gov.mo/dsat/realtime.aspx)，
其实国内也有这样的实时路况，但是情况惨不忍睹，真是差距。

车辆识别采取YOLOV5、目标跟踪采用DeepSort。

首先解析直播源的m3u8文件，获取ts文件，将视频流转化成图片流，进yolov5识别，然后deepsort跟踪，对于跟踪失踪的就计数（车流检测），
然后拿pyqt随便做了个界面展示出来。  
yolov5的模型直接拿的官方的，因为是个课设我也懒得去训练了，官方的够用了。

演示：  
![](assets/1.gif)

## 使用说明

### 环境配置

搭建环境，执行命令`pip install -r requirements.txt`  
注意：torch要根据自己的设备来安装，我的是cuda11.1,
如果不符合的话，删除清单中的torch项，自行安装。  

目标追踪的模型文件：[Google Drive](https://drive.google.com/file/d/1-GUVg9vvbB8cMsCTOGZoFQiHhXWRVsLx/view?usp=sharing)  
yolo的模型文件在启动时会自动下载，在AIDetector_pytorch.py中自行指定使用那个模型。  
或者前往[yolov5](https://github.com/ultralytics/yolov5)下载也行。

下载好的模型文件放入weights文件夹中

### 使用

运行 `view.py` 即可

## 文件结构

├─class_file 封装了一些子线程类，实时视频、解析数据、识别  
├─deep_sort 目标追踪  
├─models yolo  
├─utils 一些工具类  
└─weights 存放模型  
AIDetector_pytorch.py 识别的核心类  
tracker.py 绘制bbox、识别图像的函数  
untitled.py ui基类  
view.py 界面

## 存在的问题
车流检测时候的计数存在问题，问题出现在从左往右数的第3、4车道，因为摄像角度、视频帧数、
车速等原因会导致跟踪丢失，导致重复计数，4车道偶尔出现，3车道一直都会出现，所以3车道的计数是2倍的。
因为是课设，至少整体效果没问题，我就懒得调了

## ！！！！

遵循 GNU General Public License v3.0 协议  
标明目标检测部分来源：https://github.com/ultralytics/yolov5  
标明目标跟踪来源：https://github.com/Sharpiless/yolov5-deepsort
