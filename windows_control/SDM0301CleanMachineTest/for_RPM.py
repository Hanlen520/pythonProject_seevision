# coding = utf8
import os
os.path.abspath(".")
import re
import json

def math_cal():
    string = ""
    rpm_json = r"C:\Users\CHENGUANGTAO\Desktop\SMD0301扫地机\扫地机测试用例 (1)\扫地机测试用例 (1)\temp\rpm_20211019142426.json"
    with open(rpm_json,"r") as file:
        string = file.read()
        file.close()

    string_array = re.findall("(\d{3}),", string)
    sum = 0
    for item in string_array:
        # print(item)
        sum += int(item)
    print("RPM总计得：{}，RPM平均值为：{}".format(str(sum), str(sum / len(string_array))))

def json_cal():
    string = ""
    rpm_json = r"C:\Users\CHENGUANGTAO\Desktop\SMD0301扫地机\扫地机测试用例 (1)\扫地机测试用例 (1)\temp\rpm_20211019142426.json"
    with open(rpm_json,"r") as file:
        file_dict = json.load(file)
        # print(file_dict)
        array = file_dict["rpm"]  
        sum = 0
        for i in array:
            sum += i
        print("RPM总计得：{}，RPM平均值为：{}".format(str(sum), str(sum / len(array))))
        
        

if __name__ == "__main__":
    math_cal()
    # json_cal()