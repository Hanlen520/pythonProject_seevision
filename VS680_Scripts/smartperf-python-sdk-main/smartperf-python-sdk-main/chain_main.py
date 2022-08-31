"""
调式调用
"""
import time
from pprint import pprint

from start_up import SmartPerfSdk

"""
app_key和app_secret 获取方式
提供你的账号名称，就可以获得以上数据，请平时注意保管
"""


class ChainCall:

    def 初始化鉴权(self, app_key, app_secret, app_text):
        """
        用户鉴权
        """
        self.sdk = SmartPerfSdk(app_key=app_key, app_secret=app_secret, app_text=app_text)
        return self

    def 启动App并且完成录屏使用ADB(self):
        """
        启动录屏
        """
        start_app()
        return self

    def 上传录制好视频并且创建任务(self, video_path, algorithm_id):
        """
        算法id查询请看readme.md 图片
        如果要调整修改可以支持产品工作人员
        """
        self.task_id = self.sdk.add_task(video_path, algorithm_id)
        print(f"平台创建任务id成功{self.task_id}")
        return self

    def 查询平台结果返回等待任务完成(self):
        """
        查询平台结果返回等待任务完成
        """
        task_state, success = 'taskState', 2
        state = False
        while not state:
            for status in self.sdk._query_task_id(self.task_id):
                time.sleep(1)
                if status[task_state] == success:
                    state = True
                    break
        detail = self.sdk._query_report_detail(self.task_id)
        if detail[task_state] == success:
            result = self.sdk._get_task_frame_list_report(self.task_id)
            pprint(result)
            time.sleep(2)
        else:
            print(f"平台任务状态失败")


if __name__ == '__main__':
    # sdk = SmartPerfSdk(app_key="o7oVfy1c", app_secret="4b82840cfe138c44d80f527eba6e17c2", app_text="叮当快药")
    # start_record_and_upload_oss(algorithm_id='41')

    call = ChainCall()  # 链式调用的
    """
    (如需要可以把方法名称自行换成英文)完整的如下，初始化鉴权是一定需要的，调得是平台接口
    """
    video_path = "录好视频位置"
    call.初始化鉴权("o7oVfy1c", "4b82840cfe138c44d80f527eba6e17c2", "叮当快药").启动App并且完成录屏使用ADB(). \
        上传录制好视频并且创建任务(video_path, "41").查询平台结果返回等待任务完成()
    """
    如果录屏好，自己未上传视频的可以用下面的
    """
    # call.初始化鉴权("你的ak", "你的as", "app icon下面文本"). \
    #     上传录制好视频并且创建任务(video_path, "平台上查询的算法ID").查询平台结果返回等待任务完成()
