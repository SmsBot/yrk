#!/bin/python
import codecs, os, glob, subprocess, requests
import xml.dom.minidom

language = "yrk"

def pretty_xml(input_file, output_file):
	in_f = open(input_file, "r")
	xml_in = in_f.read()
	in_f.close()

	xml_data = xml.dom.minidom.parseString(xml_in)
	xml_text = xml_data.toprettyxml()
	xml_text = "".join([s for s in xml_text.strip().splitlines(True) if s.strip()])

	f = codecs.open(output_file, "w", encoding="UTF-8")
	f.write(xml_text)
	f.close()

def is_ok_dir(directory):
	if directory.startswith("."):
		return False
	return os.path.isdir(directory)

def list_folders():
	folders = filter(is_ok_dir, os.listdir(os.getcwd()))
	if len(folders) == 0:
		folders = ["."]
	return folders

def list_xmls():
	file_list = {}
	folders = list_folders()
	for folder in folders:
		file_list[folder] = []
		files = glob.glob(folder +"/*.xml")
		for file in files:
			head, tail = os.path.split(file)
			file_list[folder].append(tail)
	return file_list

def download_xmls():
	files = list_xmls()
	for folder in files.keys():
		for file in files[folder]:
			print "Downloading: " + folder + ", " + file
			payload = {'language': language, 'file': file, "type": folder}
			r = requests.get('http://sanat.csc.fi:8000/smsxml/xml_out/', params=payload)
			if r.status_code != requests.codes.ok:
				r.raise_for_status()
			f = codecs.open(folder + "/" + file, "w", encoding="UTF-8")
			f.write(r.text)
			f.close()

def pretty_xmls():
	files = list_xmls()
	for folder in files.keys():
		for file in files[folder]:
			print "Format XML: " + folder + ", " + file
			pretty_xml(folder + "/" + file, folder + "/" + file)

def change_branch():
	print subprocess.check_output("git checkout -B wiki_branch" , shell=True, stderr=subprocess.STDOUT)



print "Changing branch"
change_branch()
print "Downloading XMLs from sanat"
download_xmls()
pretty_xmls()
print "\n\nAll done!\n\nMerge wiki_branch to master. Push and go to http://sanat.csc.fi:8000/smsxml/git_postmerge/?language=" + language


	 