# coding = utf8
import os

from PIL import Image

os.path.abspath("..")
import imagehash


def compare2Image():
    hash_cute = imagehash.average_hash(Image.open("./Cute.jpg"))
    hash_compare = imagehash.average_hash(Image.open("./Cute_DPI1000.jpg"))
    if hash_cute == hash_compare:
        print("2 images has no different!")
    else:
        print("2 images has different!")


if __name__ == '__main__':
    compare2Image()
