# import modules
import shutil
import random
import os
from os import path
import tkinter as tk
from tkinter import filedialog

# format a text file for appending
# src is source of file, num is number of lines
def formatText(src, num):
	with open(src ,"w") as f:
		for i in range(num):
			f.write("L\n")

# get randomized seed, where num is number of files to be randomized
def getSeed(num):

	seed = []
	# go through each number
	for i in range(num):

		# add number, as string, to seed
		seed.append(str(i + 1))

	# randomize seed and return
	random.shuffle(seed)
	return seed

# get file exension (type) from the name of a file

def getExtension(file):
	place = file.rfind('.')
	if place < 0:
		return ""
	return file[place:]

# randomizes files from src
# set "deep" to true if you want inside directories to be randomized as well

def randomizeFiles(src, deep=False):

	# set and format directories
	originalDirectory = str(src)
	newDirectory = originalDirectory + "/randomized"
	if not (os.path.isdir(newDirectory)):
		os.mkdir(newDirectory)
	textFile = newDirectory + "/answerKey.txt"

	# get elemets in directory and convert to strings
	filesTemp = os.listdir(originalDirectory)
	files = []
	for file in filesTemp:
		if str(file) != '.DS_Store' and str(file) != 'randomized' and not os.path.isdir(originalDirectory + "/" + str(file)):
			files.append(str(file))
		# if its a directory and deep is true, keep going
		if os.path.isdir(originalDirectory + "/" + str(file)) and deep:
			randomizeFiles(originalDirectory + "/" + str(file), True)

	# get number of files and format textFile
	numFiles = len(files)
	formatText(textFile, numFiles)

	# get seed
	seed = getSeed(numFiles)

	# move and rename files to new directory with seed
	for i in range(numFiles):

		# copy file to new destination
		shutil.copy(originalDirectory + "/" + files[i], newDirectory + "/" + files[i])

		# rename file according to seed
		os.rename(newDirectory + "/" + files[i], newDirectory + "/" + seed[i] + getExtension(files[i]))

		# add to answer key
		key = open(textFile, "r")
		lines = key.readlines()
		lines[int(seed[i]) - 1] = seed[i] + " : " + files[i] + "\n"

		key = open(textFile, "w")
		key.writelines(lines)
		key.close()


# tkinter window

def main():
	root = tk.Tk()
	root.withdraw()

	file_path = filedialog.askdirectory()

	randomizeFiles(file_path)

	root.destroy()


if __name__ == "__main__":
	main()