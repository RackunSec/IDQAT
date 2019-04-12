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

# PII methods and values:
class piiObject:
	def __init__(self):
		self.piiRegex = {} # associative array for readability, extensibility
		self.piiRegex["reSSN"] = "[0-9]{3}[^0-9][0-9]{2}[^0-9][0-9]{4}"
		self.piiRegex["reDoB"] = "(0[0-9]|1[012])[^0-9][0-3][0-9][^0-9]([19|20][0-9]{2})"
		self.piiRegex["rePhone"] = "\+?1?[^0-9]?\(?[0-9]{3}\)?[^0-9]+[0-9]{3}[^0-9]+[0-9]{4}"
		# Financial Data:
		self.piiRegex["reCC"] = "[54][0-9]{3}[^0-9]([0-9]{4}[^0-9]){2}[0-9]{4}"
		# SysPII:
		self.piiRegex["reSerialNo"] = "([0-9]{5}-){4}[0-9]{5}"
# File methods and values:
class FileObject: # OOP!
	def __init__(self):
		# Globals values in Object:
		self.fileList = list()
		self.positivePiiFilesList = list()
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

pii = piiObject() # instantiate object from class
files = FileObject() # instantiate oibject from class

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
	for line in fh:
		line = line.rstrip()
		if re.search(pii.piiRegex["reSSN"],line):
			print "[!] SSN found in file: "+files.fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			files.positivePiiFilesList.append(files.fileList[file])
			files.fileResultCount+=1
			fileFoundPIIBool=1
		if re.search(pii.piiRegex["reDoB"],line):
			print "[!] DoB found in file: "+files.fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			files.positivePiiFilesList.append(files.fileList[file])
			files.fileResultCount+=1
			fileFoundPIIBool=1
		if re.search(pii.piiRegex["rePhone"],line):
			print "[!] Phone number found in file: "+files.fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			files.positivePiiFilesList.append(files.fileList[file])
			files.fileResultCount+=1
			fileFoundPIIBool=1
		if re.search(pii.piiRegex["reSerialNo"],line):
			print "[!] Possible serial number found in file: "+files.fileList[file]+" -> "+line # TODO remove
			files.positivePiiFilesList.append(files.fileList[file])
			files.fileResultCount+=1
			fileFoundPIIBool=1
		if re.search(pii.piiRegex["reCC"],line):
			print "[!] Possible credit card number found in file: "+files.fileList[file]+" -> "+line # TODO remove
			files.positivePiiFilesList.append(files.fileList[file])
			files.fileResultCount+=1
			fileFoundPIIBool=1
	# rewind file and hash it if a positive was found:
	if fileFoundPIIBool == 1:
		# rewind read and pass fh to fileHash(fh) method.
		fh.seek(0,0) # rewind
		print files.fileHash(fh)
	file += 1

# 3. Log it in database

# 4. Clean up and Exit
print "\n[*] "+str(files.fileResultCount)+" results found.\n"
