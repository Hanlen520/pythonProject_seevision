import re
from record.adb import AdbUtils
from record.licence import Licence
from loguru import logger
import time
from pprint import pprint


class SmartPerfSdk(AdbUtils, Licence):
    """
    平台上需要获取 ak
    """

    def __init__(self, app_key, app_secret, app_text):
        super().__init__()
        self.app_key = app_key
        self.app_secret = app_secret
        self.app_text = app_text
        self.vip = self._get_user_privilege()
        logger.info(self.vip)
        self.video_path = self.get_video_path()

    def start_app(self):
        """
        start_app()下面是启动app后面的逻辑，@record装饰器添加后会负责录屏
        offset第二个元素会负责录屏的总时间
        :return:
        """
        root = sdk.xml_root()
        logger.info(f"请确保当前{sdk.app_text}不在后台并且没有被启动")
        for node in root.iter("node"):
            logger.info(
                f'\n===== SCREEN INFO ====='
                f'\nText: {node.attrib["text"]}'
                f'\n===================='
            )
            if node.attrib["text"] == sdk.app_text:
                bounds = node.attrib["bounds"]
                pattern = re.compile(r"\d+")
                coord = pattern.findall(bounds)
                x_pos = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                y_pos = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                sdk.click_pos(x_pos, y_pos, sdk.video_path, sdk.vip['videoDuration'])

    def start_record_and_upload_oss(self, algorithm_id: str):
        """
        (用户自己完成的)1.先自己安装手机app
        (用户自己完成的)2.屏幕划动到手机界面分页的界面，!这里需要记录app_text(同app icon下方的名称)。比如飞书 app_text就是叫飞书
        3.调用该方法会完成以下步骤：
          自动化识别当前手机界面启动app-->启动录屏-->保存视频-->上传平台-->创建任务-->查询任务状态-->判断任务状态-->完成任务
        :param algorithm_id: 从平台上面查询支持算法id，算法Id会关联项目id(具体见readme.MD)
        :return:
        """
        # start_app()
        logger.info(f"录屏文件保存在{sdk.video_path}")
        sdk.create_task_callback_result(sdk.video_path, algorithm_id)

    def crate_task(self, video_path, algorithm_id):
        """
        算法id查询请看readme.md 图片
        如果要调整修改可以支持产品工作人员
        """
        self.task_id = self.add_task(video_path, algorithm_id)
        print(f"平台创建任务id成功{self.task_id}")
        return self

    def get_task_report(self):
        """
        查询平台结果返回等待任务完成
        """
        task_state, success = 'taskState', 2
        state = False
        print("task_id = ", self.task_id)
        while not state:
            for status in self._query_task_id(self.task_id):
                time.sleep(1)
                if status[task_state] == success:
                    state = True
                    break
        detail = self._query_report_detail(self.task_id)
        if detail[task_state] == success:
            result = self._get_task_frame_list_report(self.task_id)
            pprint(result)
            time.sleep(2)
        else:
            print(f"平台任务状态失败")


if __name__ == '__main__':
    # test03 app_key="l5iivi1c", app_secret="9e7f521bdd8c5c9eb5cb498631bb1a7e"
    # # 标准调用试例
    # sdk = SmartPerfSdk(app_key="l5iivi1c", app_secret="9e7f521bdd8c5c9eb5cb498631bb1a7e", app_text="飞书")
    # sdk.crate_task()
    # sdk.start_app()
    # sdk.start_record_and_upload_oss(algorithm_id='50')

    # 自定义调用示例
    # 初始化鉴权，app_text用于指定点击的文本元素
    sdk = SmartPerfSdk(app_key="l5iivi1c", app_secret="9e7f521bdd8c5c9eb5cb498631bb1a7e", app_text="QQ")
    # 根据当前窗口xml，查找app_text内容，并进行点击
    # sdk.start_app()
    # sdk.start_app 这里会自根据默认路径，自生成视频文件,
    # 如果想使用自己录制的视频，可以跳过sdk.start_app()定义视频文件路径
    video_path = "D://test/A.mp4"
    sdk.crate_task(video_path, 50)
    sdk.get_task_report()
