from os import listdir
from bs4 import BeautifulSoup
import re

data = 'man7.org/linux/man-pages/man0/'

for f in listdir(data):
	print('Reading file ' + f)
	contents = ''
	with open(data+f) as f:
		contents = f.read()
	soup = BeautifulSoup(contents, "html.parser")
	title = soup.find('title').text
	section = ''
	all_i = []
	all_b = []
	all_href = []
	for i in soup.findAll('i'):
		if 'Section' in i.text:
			section = i.text
		else:
			i = i.text.split()
			all_i.append(' '.join(i))
	for b in soup.findAll('b'):
		b = b.text.split()
		all_b.append(' '.join(b))
	for href in soup.findAll('href'):
		all_href.append(href.text)	
	
	all_caps_single = filter(None, [x for x in re.findall(r"([A-Z]+[\s_][A-Z]*)", contents)])
	all_mentions = filter(None, [x.strip() for x in re.findall(r"[^ ]+\([0-9]+\)", contents)])
	all_sys_files = filter(None, [x.strip() for x in re.findall(r"(/?[A-Za-z0-9.]+/[A-Za-z0-9.]+)+", contents)])
	all_first_caps = filter(None, [x.strip() for x in re.findall(r"([A-Z][A-Za-z0-9.]+[ ]+)+", contents)])
	all_entities = set(all_i) | set(all_b) | set(all_href) | set(all_caps_single) | set(all_first_caps)

	with open('out.txt', 'w') as f:
		f.write(title + '\t' + section + '\n')
		for entity in all_entities:
			f.write(entity + '\n')

	break
