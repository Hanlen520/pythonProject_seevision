# coding = utf8
import os


def create_10_folder():
    # path = r"D:\音视频一体机\GM1_48M_114\testData\PART2\\"
    path = r"D:\音视频一体机\GM1_48M_114\testData\PART1\1COLDBOOT\\"
    parFolder = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    for i in range(10):
        i += 1
        print(path + "{}".format(i))
        os.mkdir(path + "{}".format(i))

    # for i in parFolder:
    #     print(path + "{}".format(i))
    #     os.mkdir(path + "{}".format(i))

    # for j in parFolder:
    #     for i in range(10):
    #         i += 1
    #         print(path + "{}\\".format(j) + "{}".format(i))
    #         os.mkdir(path + "{}\\".format(j) + "{}".format(i))
    #     i = 0


if __name__ == "__main__":
    path = r"D:\音视频一体机\IMX581_48M_114\testData\PART2\N"
    # videoCount = 10
    videoCount = 1
    for i in range(videoCount):
        i += 1
        print(i)
        command = r"ffmpeg -i {}\{}.mp4 -q:v 1 -f image2 {}\{}\xxx_%05d.jpg".format(path, i, path, i)
        print(command)
        os.system(command)
    # create_10_folder()
