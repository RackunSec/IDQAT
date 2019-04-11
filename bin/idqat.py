#!/usr/bin/python
# 2019 (c) GNU, WeakNet Labs
# This product should come with the GNU License
# Douglas Berdeaux
# weaknetlabs@gmail.com
#
# OS Independent PII/SysPII Search and
import os # for opening files (OS independent)
import re # for regular expressions
import sys # for args

if len(sys.argv)>1:
	if re.search("-?-h(elp)?",sys.argv[1]):
		print "\nIDQAT [Help]:\n\tUsage:\n\t\t./idqat.py <directory>\n"
		sys.exit(1)

fileList = list() # all files found
positivePiiFilesList = list()
resultCount = 0

# NO FALSE POSITIVES. OR ELSE!:
reSSN = "[0-9]{3}[^0-9][0-9]{2}[^0-9][0-9]{4}"
reDoB = "(0[0-9]|1[012])[^0-9][0-3][0-9][^0-9]([19|20][0-9]{2})"
rePhone = "\+?1?[^0-9]?\(?[0-9]{3}\)?[^0-9]+[0-9]{3}[^0-9]+[0-9]{4}"

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
		line = line.rstrip()
		if re.search(reSSN,line):
			print "[!] SSN found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
		if re.search(reDoB,line):
			print "[!] DoB found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
		if re.search(rePhone,line):
			print "[!] Phone number found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
	file += 1

# 3. Log it in database

# 4. Clean up and Exit
print "[*] "+str(resultCount)+" results found.\n\n"
