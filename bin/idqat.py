#!/usr/bin/python
# 2019 (c) GNU, WeakNet Labs
# This product should come with the GNU License
# Douglas Berdeaux
# weaknetlabs@gmail.com
#
# OS Independent PII/SysPII Query and Alert Tool
#
##
import os # for opening files (OS independent)
import re # for regular expressions
import sys # for args
import hashlib # Hashing file content

##
# Help Me!
##
argpath = ''
if len(sys.argv)>1:
	if re.search("-?-h(elp)?",sys.argv[1]):
		print "\nIDQAT [Help]:\n\tUsage:\n\t\t./idqat.py <directory>\n"
		sys.exit(1)
	else: # must have been a path:
		argpath = sys.argv[1]
if argpath  == '':
	argpath = '.'
##
# Objects:
##
# PII methods and values:
class Pii:
	def __init__(self):
			self.piiRegex = {
			"ssn":{"re":"[0-9]{3}[^0-9a-zA-Z][0-9]{2}[^0-9a-zA-Z][0-9]{4}","name":"Social Security Number","type":"PII"},
			"dob":{"re":"(0[0-9]|1[012])[^0-9a-zA-Z][0-3][0-9][^0-9a-zA-Z]([19|20][0-9]{2})","name":"Date of Birth","type":"PII"},
			"phone":{"re":"\+?1?[^0-9a-zA-Z]?\(?[0-9]{3}\)?[^0-9a-zA-Z]+[0-9]{3}[^0-9a-zA-Z]+[0-9]{4}","name":"Phone Number","type":"PII"},
			# Financial Data:
			"cc":{"re":"[54][0-9]{3}[^0-9]([0-9]{4}[^0-9a-zA-Z]){2}[0-9]{4}","name":"Credit Card","type":"Financial"},
			# SysPII:
			"serialNo":{"re":"([0-9]{5}-){4}[0-9]{5}","name":"Serial Number","type":"System PII"}
			}
		#self.piiCSVRegex = {} # for any CSV Files that may contain PII
		#self.piiCSVRegex["csvSSN"] = ",\s?" + self.piiRegex["reSSN"] + "\s?,"

# File methods and values:
class File:
	def __init__(self):
		# Globals values in Object:
		self.fileList = list()
		self.positivePiiFilesList = {} # Associate Object:
			# filename: {
				# "path": "/path/to/filename",
				# "hash":"hashed value",
				# "piiTypes": piiTypes() # TODO
			# }
		self.fileResultCount = 0
	# Hashing method:
	def fileHash(self,fh): # requires a file handle
		#return hashlib.md5(fh.read().hexdigest())
		hash = hashlib.md5() # create a hash object
		with fh: # iterate through file with a buffer, buf:
			buf = fh.read()
			hash.update(buf)
		return hash.hexdigest() # return the final md5sum
		# check with md5sum < filename

pii = Pii() # instantiate object from class
files = File() # instantiate oibject from class

##
# Workflow of the App:
##
print "\nIDQAT - \n"
print "[*] Recursively searching directory "+argpath+" ... "

# 1. Get the file list
for root,directories, filenames in os.walk(argpath):
	for filename in filenames:
		files.fileList.append(os.path.join(root,filename))

# 2. Search each found file for PII
file = 0
while file < len(files.fileList):
	# print (fileList[file])
	fh = open(files.fileList[file]) # open the file with a file handler
	fileFoundPIIBool = 0 # if PII found, == 1
	filePiiCount = 0 # how many instances found per file?
	for line in fh:
		line = line.rstrip() # chomp off any additional white spaces
		# Loop through the PII regex objects and re.search() the line from the file:
		for item in pii.piiRegex:
			if re.search(pii.piiRegex[item]["re"],line): # if match found:
				filePiiCount+=1 # increment token
				print "[!] Possible PII Match on line: "+line+" of type: "+pii.piiRegex[item]["type"]
				if not files.fileList[file] in files.positivePiiFilesList: # is this file in the list yet?
					files.fileResultCount+=1 # increment found token
					files.positivePiiFilesList[files.fileList[file]] = {
						"type":[] # create an array and append the type if not already there later
					}
				# Append the type
				if not pii.piiRegex[item]["type"] in files.positivePiiFilesList[files.fileList[file]]["type"]:
					files.positivePiiFilesList[files.fileList[file]]["type"].append(pii.piiRegex[item]["type"])
				fileFoundPIIBool=1

	# rewind file and hash it if a positive was found:
	if fileFoundPIIBool == 1:
		# rewind read and pass fh to fileHash(fh) method.
		fh.seek(0,0) # rewind
		files.positivePiiFilesList[files.fileList[file]]["hash"] = files.fileHash(fh) # create a JSON-like structure
		files.positivePiiFilesList[files.fileList[file]]["path"] = argpath
		files.positivePiiFilesList[files.fileList[file]]["instances"] = filePiiCount
	file += 1

# 3. Log it in database

# 4. Clean up and Exit
print "\n[*] "+str(files.fileResultCount)+" files found containing PII.\n"
print files.positivePiiFilesList # DEBUG
