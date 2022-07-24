# coding = utf8

import os
import subprocess
from time import sleep

os.path.abspath(".")


def read_modeule_from_txt(fail_list_path=r"./Camera_Need_ReRun_Module_List.txt"):
    module_list = []
    with open(fail_list_path, "r") as temp_file:
        cur_lines = temp_file.readlines()
        for cur_line in cur_lines:
            temp_line = cur_line.strip().replace(" ", "")
            # print(temp_line)
            if temp_line:
                module_list.append(temp_line)
        if module_list:
            return module_list


def run_singleSpecific_module(number=0, module_name="armeabi-v7a CtsAppOpsTestCases"):
    print("【No.{}】 Begin Module \n【{}】 \nFailed Case Rerun, please wait……".format(number, module_name))
    """
        打开命令行进入/android11/android-cts-11_r8-linux_x86-arm/android-cts/tools
        输入：./cts-tradefed，激活cts测试程序
        再输入：run cts --plan CTS开始执行整个CTS的测试
    """
    # step1: enter cts-tradefed
    # step2: run cts -m <module_name>
    # step3: exit current test case
    # Run whole cycle till all module run out

    # os.system("./cts-tradefed run cts -m {}".format(module_name))
    subprocess.Popen("./cts-tradefed run cts -m {}".format(module_name))
    print("【{}】 Module rerun finished, please wait others module done and check all result.".format(module_name),
          end="\n\n")
    sleep(5)


if __name__ == "__main__":
    # print("OK")
    fail_list_path = r"./Camera_Need_ReRun_Module_List.txt"
    module_list = read_modeule_from_txt(fail_list_path)
    # print(module_list)
    for i in range(1, len(module_list)):
        current_rerun_module = module_list[i]
        # print(current_rerun_module)
        run_singleSpecific_module(i, current_rerun_module)
