from multiprocessing import Event
import time
import os
from uuid import uuid4
from constants import pro_path_new
import xml.etree.cElementTree as et
from constants import Config


class AdbUtils(Config):
    queries = 0
    video_path = ""
    event = Event()

    def __init__(self):
        """
        Args:
        adb_path (str): 指定adb路径
        """
        self.processes = None
        self.device_id = self.get_device_id()
        print(self.device_id)
        # self.load_path()
        if self.check_adb_device():
            self.dump_file = os.path.join(pro_path_new(), "dump", self.xml_file)

    def get_video_path(self):
        mp4_dir = os.path.join(pro_path_new(), 'mp4')
        if not os.path.exists(mp4_dir):
            os.mkdir(mp4_dir)
        return os.path.join(mp4_dir, f"{uuid4()}.mp4")

    def load_path(self):
        """
        使用adb地址
        Returns:
        adb executable path
        """
        os.environ['path'] += f'{os.path.join(pro_path_new(), "res")};'
        print(os.environ['path'])

    def get_device_id(self):
        """
        获取设备id
        :return:
        """
        device = os.popen("adb devices").readlines()
        if len(device) > 1:
            device_id = device[1]
            return device_id.split()[0]

    def check_adb_device(self):
        """
        检查adb状态
        :return:
        """
        state = os.popen("adb get-state").readlines()
        if state and "device" in state[0]:
            return True
        else:
            os.popen("adb kill-server")
            os.popen("adb start-server")
            return self.check_adb_device()

    def click_pos(self, x_pos, y_pos, video_path: str, duration: int):
        """
        单击地址
        :param x_pos:x坐标
        :param y_pos:y坐标
        :param video_path:视频地址
        :param duration:限制时间
        :return:
        """
        try:
            #subprocess.Popen(f"adb shell screenrecord /sdcard/{self.device_id}.mp4 --time-limit {duration}", shell=True, stdout=subprocess.PIPE).communicate()[0]
            os.popen(f"adb shell screenrecord /sdcard/{self.device_id}.mp4 --time-limit {duration}")
            #os.system(f"adb shell screenrecord /sdcard/{self.device_id}.mp4 --time-limit {duration}")
            time.sleep(0.5)
            os.popen(f'adb -s {self.device_id} shell input tap {x_pos} {y_pos}')
            #os.popen(f'adb -s {self.device_id} shell input tap {x_pos} {y_pos}')
            #os.system(f"adb shell screenrecord /sdcard/{self.device_id}.mp4 --time-limit {duration}")
        except Exception as e:
            print(f"{e}")
            raise Exception("adb录制不支持，请联系smartperf产品方")
        time.sleep(duration+1)
        os.system(f"adb pull /sdcard/{self.device_id}.mp4 {video_path}")

    def xml_root(self):
        """
        获取页面布局后进行操作
        attrib_name
        text_name
        :return:
        """
        time.sleep(5)
        os.popen(f'adb -s {self.device_id} shell uiautomator dump --compressed /{self.xml_path}')
        os.popen(f'adb -s {self.device_id} pull {self.xml_path} {self.dump_file}')
        if not os.path.exists(self.dump_file):
            raise Exception(f"dump文件不存在{self.dump_file}")
        source = et.parse(self.dump_file)
        return source.getroot()

    def is_video(self, input_path: str) -> bool:
        """
        判断是视频
        :return:
        """
        if input_path.rsplit(".", 1):
            suffix = input_path.rsplit(".", 1)[-1].upper()
            return suffix in self.suffix_set
