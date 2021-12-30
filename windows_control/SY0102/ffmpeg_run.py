# coding = utf8
import os

if __name__ == "__main__":
    path = r"D:\testData\COLDBOOT"
    videoCount = 10
    # videoCount = 1
    for i in range(videoCount):
        i += 1
        print(i)
        command = r"ffmpeg -i {}\{}.mp4 -q:v 1 -f image2 {}\{}\xxx_%05d.jpg".format(path, i, path, i)
        os.system(command)
