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
import hashlib # Hashing file content

if len(sys.argv)>1:
	if re.search("-?-h(elp)?",sys.argv[1]):
		print "\nIDQAT [Help]:\n\tUsage:\n\t\t./idqat.py <directory>\n"
		sys.exit(1)

fileList = list() # all files found
positivePiiFilesList = list()
resultCount = 0

# PII:
reSSN = "[0-9]{3}[^0-9][0-9]{2}[^0-9][0-9]{4}"
reDoB = "(0[0-9]|1[012])[^0-9][0-3][0-9][^0-9]([19|20][0-9]{2})"
rePhone = "\+?1?[^0-9]?\(?[0-9]{3}\)?[^0-9]+[0-9]{3}[^0-9]+[0-9]{4}"
# Financial Data:
reCC = "[54][0-9]{3}[^0-9]([0-9]{4}[^0-9]){2}[0-9]{4}"
# SysPII:
reSerialNo = "([0-9]{5}-){4}[0-9]{5}"
# my Functions:
def fileHash(fh): # requires a file handle
	return hashlib.md5(fh.read().hexdigest())

print "\nIDQAT - \n"
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
	fileFoundPIIBool = 0 # if PII found, == 1
	for line in fh:
		line = line.rstrip()
		if re.search(reSSN,line):
			print "[!] SSN found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
			fileFoundPIIBool=1
		if re.search(reDoB,line):
			print "[!] DoB found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
			fileFoundPIIBool=1
		if re.search(rePhone,line):
			print "[!] Phone number found in file: "+fileList[file]+" -> "+line # TODO remove printing of PII to stdout
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
			fileFoundPIIBool=1
		if re.search(reSerialNo,line):
			print "[!] Possible serial number found in file: "+fileList[file]+" -> "+line # TODO remove
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
			fileFoundPIIBool=1
		if re.search(reCC,line):
			print "[!] Possible credit card number found in file: "+fileList[file]+" -> "+line # TODO remove
			positivePiiFilesList.append(fileList[file])
			resultCount+=1
			fileFoundPIIBool=1
	# rewind file and hash it if a positive was found:
	if fileFoundPIIBool == 1:
		# rewind read and pass fh to fileHash(fh) method.
		pass
	file += 1

# 3. Log it in database

# 4. Clean up and Exit
print "\n[*] "+str(resultCount)+" results found.\n"
