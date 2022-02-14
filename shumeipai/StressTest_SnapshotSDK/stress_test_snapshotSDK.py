# coding = utf8

import os
os.path.abspath(".")
import subprocess
from time import sleep
from PIL import Image
import imagehash
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class StressTest:
	
	def __init__(self, snapshotSDKPath, test_count, original_image):
		self.snapshotSDKPath = snapshotSDKPath
		self.test_count = test_count
		self.original_image = original_image
		self.resultList = []
	
	def stress_test_area(self):
		print("=====================Begin test=====================")
		for i in range(test_count):
			print("=====================Current is {} snapshot!=====================".format(str(i+1)))
			subprocess.Popen(self.snapshotSDKPath, shell=True).communicate()
			sleep(3)
			pictureName = "renamedImage{}.jpg".format(str(i+1))
			self.fixedPicture(pictureName)
			self.picture_compare(pictureName)
			print("=====================Test {} snapshot done, enter next circle!=====================".format(str(i+1)))
	
		
	def picture_compare(self, compare_image):
		original = imagehash.average_hash(Image.open(self.original_image))
		compare = imagehash.average_hash(Image.open(compare_image))
		result = ""
		if compare == original:
			result = "{} is PASS".format(compare_image)
			self.resultList.append(result)
		else:
			result = "{} is FAIL".format(compare_image)
			self.resultList.append(result)
		self.toTxt(result)
		
	def fixedPicture(self, pictureName):
		all_files = os.listdir("./")
		for i in all_files:
			if "-" in i and "jpg" in i:
				os.rename(i, pictureName)
		all_files = os.listdir("./")
		print(all_files)
	
	def toTxt(self, result):
		with open("./Result.txt", "a+") as f:
			f.write(result + "\n")
			
if __name__ == "__main__":
	test_count = 100
	snapshotSDKPath = "./snapshot_sdk/build/test"
	original_image = "./originalImage.jpg"
	resultList = []
	stressTest = StressTest(snapshotSDKPath, test_count, original_image)
	stressTest.stress_test_area()
	print(stressTest.resultList)

