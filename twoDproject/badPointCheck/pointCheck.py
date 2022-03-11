# coding = utf8
import multiprocessing
import os

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:pointCheck.py
    @Author:十二点前要睡觉
    @Date:2022/3/10 10:49
"""

"""
    Description:
    图片坏点检测：
    1、0 - 纯白图片检测：判断每个像素点Y亮度大于60即为坏点
    2、1 - 纯黑图片检测：判断每个像素点Y亮度小于-5即为坏点
    
    换算公式：
    Y(亮度)=(0.299*R)+(0.587*G)+(0.114*B)
    
    判断单张图片是否PASS：坏点数不超过0.002%
    
"""

from PIL import Image


class PointCheck:

    def __init__(self, picture_path, check_type, picture_name):
        self.picture_path = picture_path
        self.check_type = check_type
        self.img_src = Image.open(self.picture_path)
        self.picture_name = picture_name

    def getPictureSize(self):
        return self.img_src.size

    def getPicturePixels(self):
        img_src = self.img_src.convert("RGBA")
        pixel_list = img_src.load()
        return pixel_list

    def getAll_pixelsCoordinate(self, picture_size):
        point_coordinate = []
        for x in range(0, picture_size[0]):
            for y in range(0, picture_size[1]):
                point_coordinate.append((x, y))
        return point_coordinate

    def pixel_1(self, pixel_list, point):
        print(pixel_list[point])

    def analysis_point_info(self, pixel_list, point_coordinate, check_type):
        # 每个像素点一个进程去分析
        bad_point_list = []
        for point in point_coordinate:
            # (215, 186, 154, 255)
            point_info = pixel_list[point]
            point_r = point_info[0]
            point_g = point_info[1]
            point_b = point_info[2]
            # print("R is：{}".format(point_r))
            # print("G is：{}".format(point_g))
            # print("B is：{}".format(point_b))
            """
            换算公式：
            Y(亮度)=(0.299*R)+(0.587*G)+(0.114*B)
            """
            point_Y = 0.299 * point_r + 0.587 * point_g + 0.114 * point_b
            # print(point_Y)
            """
            图片坏点检测：
            1、0 - 纯白图片检测：判断每个像素点Y亮度大于60即为坏点
            2、1 - 纯黑图片检测：判断每个像素点Y亮度小于-5即为坏点
            
            判断单张图片是否PASS：坏点数不超过0.002%
            """
            if check_type == 0:
                if point_Y > 60:
                    bad_point_list.append({"coordinate": point, "Y": point_Y})
            elif check_type == 1:
                if point_Y < -5:
                    bad_point_list.append({"coordinate": point, "Y": point_Y})
        if bad_point_list:
            print("当前图片【{}】总像素点【{}】，坏点数【{}】".format(self.picture_name, len(point_coordinate), len(bad_point_list)))
            if len(bad_point_list) / len(point_coordinate) <= 0.00002:
                picture_infos = {"bad_point_list": bad_point_list, "result": "PASS",
                                 "wholePointCount": len(point_coordinate)}
            else:
                picture_infos = {"bad_point_list": bad_point_list, "result": "FALSE",
                                 "wholePointCount": len(point_coordinate)}
            # 返回每张图片的检测结果和坏点列表（包含每个坏点的坐标和亮度值）再对每张图片进行坏点突出绘制一张新的图片
            return picture_infos

    def rebuild_picture_forBADPoint(self, picture_infos):
        # 图片命名 原图片名+总像素点数+坏点数.jpg
        # print(picture_infos)
        bad_point_list = picture_infos["bad_point_list"]
        for one_point in bad_point_list:
            self.img_src.putpixel((one_point["coordinate"][0], one_point["coordinate"][1]), (234, 53, 57, 255))
        self.img_src = self.img_src.convert("RGB")
        if not os.path.exists("./convertPicture/"):
            os.mkdir("./convertPicture/")
        self.img_src.save(
            "./convertPicture/总点数{}有{}个坏点_{}".format(picture_infos["wholePointCount"], len(bad_point_list),
                                                     self.picture_name))


def bad_check_area(picture_path, check_type, picture):
    pc = PointCheck(picture_path, check_type, picture)
    point_coordinate = pc.getAll_pixelsCoordinate(pc.getPictureSize())
    picture_infos = pc.analysis_point_info(pc.getPicturePixels(), point_coordinate, check_type)
    pc.rebuild_picture_forBADPoint(picture_infos)


if __name__ == '__main__':
    pictureFile = os.listdir("./pictures/")
    pool = multiprocessing.Pool(len(pictureFile))
    check_type = 0
    # 每张图片独立一个进程去操作
    for picture in pictureFile:
        picture_path = "./pictures/{}".format(picture)
        pool.apply_async(func=bad_check_area, args=(picture_path, check_type, picture,))
    pool.close()
    pool.join()
