#!/usr/bin/python
# 2019 (c) GNU, WeakNet Labs
# This product should come with the GNU License
# Douglas Berdeaux
# weaknetlabs@gmail.com
#
# OS Independent PII/SysPII Search and 
import os
import re

fileList = list() # all files found
positivePiiFilesList = list()

# NO FALSE POSITIVES. OR ELSE!:
reSSN = "[0-9]{3}[^0-9][0-9]{2}[^0-9][0-9]{4}"
reDoB = "(0[0-9]|1[012])[^0-9][0-3][0-9][^0-9]([19|20][0-9]{2})"

print "\nIDQAT - \n\n"
print "[*] Recursively searching current directory ... "

# 1. Get the file list
for root,directories, filenames in os.walk('.'):
	for filename in filenames:
		fileList.append(os.path.join(root,filename))

# 2. Search each found file for PII
file = 0
while file < len(fileList):
	# print (fileList[file])
	fh = open(fileList[file]) # open the file with a file handler
	for line in fh:
		if re.search(reSSN,line):
			print "[!] SSN Found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
		if re.search(reDoB,line):
			print "[!] DoB Found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
	file += 1

# 3. Log it in database

