import time
from os.path import basename
from pprint import pprint
from requests import post


class Licence:
    url = "http://console.smart-perf.com:7001/api/sdk"

    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret

    def _get_user_privilege(self):
        """
        获取使用权限
        uploadMp4?ak=""&as=""
        :return:
        """
        path = "/getVipPrivilege"
        body = {
            "appKey": self.app_key,
            "appSecret": self.app_secret,
        }
        res = post(self.url + path, json=body)
        if res.status_code == 200:
            result = res.json()
            data = result["data"]
            if result['success'] and data:
                return data
            else:
                raise Exception(f"接口返回数据{data}不全，需要检查{self.url + path}接口")

    def add_task(self, video_path: str, algorithm_id: str):
        """
        新增任务 project_id
        """
        file_name = basename(video_path)
        body = {
            "algorithmId": algorithm_id,
            "appKey": self.app_key,
            "appSecret": self.app_secret,
        }
        files = [('file', (file_name, open(video_path, 'rb'), 'application/octet-stream'))]
        res = post(f"{self.url}/addTask", data=body, files=files)
        if res.status_code == 200:
            result = res.json()
            # print(result)
            if result["success"]:
                # print(result["data"])
                task_id = result["data"]
                if task_id: return task_id

    def _query_task_id(self, task_id):
        """
        查询任务
        """
        body = {
            "taskId": task_id, "appKey": self.app_key, "appSecret": self.app_secret,
        }
        res = post(f"{self.url}/getTask", json=body)
        if res.status_code == 200:
            result = res.json()
            if result["success"]:
                pprint("-------检索任务状态中-------")
                task_status = result["data"]
                if task_status: return task_status

    def _query_report_detail(self, task_id):
        """
        报告详情基本信息接口
        """
        body = {
            "taskId": task_id, "appKey": self.app_key, "appSecret": self.app_secret,
        }
        res = post(f"{self.url}/getTaskReport", json=body)
        if res.status_code == 200:
            result = res.json()
            if result["success"]:
                data = result["data"]
                if data: return data

    def _get_task_frame_list_report(self, task_id):
        """
        报告详情目标帧接口
        """
        body = {
            "taskId": task_id, "appKey": self.app_key, "appSecret": self.app_secret,
        }
        res = post(f"{self.url}/getTaskFrameListReport", json=body)
        if res.status_code == 200:
            result = res.json()
            if result["success"]:
                result_data = result["data"]
                print("get_task_frame_list_report:", result_data)
                return result_data
                # if result_data:
                #     data = []
                #     for r in result_data:
                #         data.append({r["frameName"]: r["frameIndex"]})
                #     return data

    def create_task_callback_result(self, video_path: str, algorithm_id: str):
        """
        创建任务和回调结果
        1.add_task创建任务，获取任务id
        2._query_task_id轮询等待success等于2
        3._query_report_detail查询结果detail的结论
        4.
        """
        task_state, success = 'taskState', 2
        task_id = self.add_task(video_path, algorithm_id)
        print(f"平台创建任务id成功{task_id}")
        state = False
        while not state:
            for status in self._query_task_id(task_id):
                time.sleep(1)
                if status[task_state] == success:
                    state = True
                    break
        detail = self._query_report_detail(task_id)
        if detail[task_state] == success:
            result = self._get_task_frame_list_report(task_id)
            pprint(result)
            time.sleep(2)
        else:
            print(f"平台创建任务id失败")


if __name__ == '__main__':
    lic = Licence(app_key="0k3A8eLA", app_secret="cf42240987b7b1a9729b58df3aa9a41e")
    lic.create_task_callback_result(r"E:\video\A.mp4", algorithm_id='56')
