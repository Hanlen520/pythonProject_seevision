# coding = utf8
import os


def create_10_folder():
    # path = r"D:\音视频一体机\GM1_48M_114\testData\PART2\\"
    path = r"D:\For_Work\PandaOs性能测试_study\temp\\"
    # parFolder = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "H265"]
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
    path = r"D:\For_Work\PandaOs性能测试_study\temp"
    videoCount = 10
    # videoCount = 1
    # videoCount = 5
    create_10_folder()
    for i in range(videoCount):
        i += 1
        print(i)
        command = r"ffmpeg -i {}\{}.mp4 -q:v 1 -f image2 {}\{}\xxx_%05d.jpg".format(path, i, path, i)
        print(command)
        os.system(command)


    # ffmpeg -i D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\2.mp4 -q:v 1 -f image2 D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\2\xxx_%05d.jpg
