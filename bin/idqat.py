#!/usr/bin/python
# 2019 (c) GNU, WeakNet Labs
# This product should come with the GNU License
# Douglas Berdeaux
# weaknetlabs@gmail.com
#
import os
import re
fileList = list() # all files found
piiFilesList = list()
reSSN = "[0-9]{3}[^0-9][0-9]{2}[^0-9][0-9]{4}"

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
			print "[!] SSN Found in file: "+fileList[file]+" -> "+line
	file += 1
